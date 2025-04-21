from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer,HfArgumentParser,AutoConfig
from transformers import HfArgumentParser
from dataclasses import dataclass
from typing import Optional
import torch
from transformers.trainer_callback import TrainerCallback
import os
import logging
from ft_dataset import DecisionDataset
import glob
import json
import math
from safetensors.torch import load_file 

torch.cuda.empty_cache()
class LoggingCallback(TrainerCallback):
    def __init__(self, logger):
        self.logger = logger

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            if 'eval_loss' in logs:
                self.logger.info(f"Eval loss: {logs['eval_loss']}")
            self.logger.info(logs)

    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        if metrics is not None:
            self.logger.info(f"Evaluate loss: {metrics['eval_loss']}")

@dataclass
class ModelArguments:
    model_path: Optional[str] = None
    checkpoint_path: Optional[str] = None
    torch_dtype: Optional[str] = None
    num_heads: Optional[int] = None

@dataclass
class DataTrainingArguments:
    train_dataset_file: Optional[str] = None
    eval_dataset_file: Optional[str] = None
    overwrite_cache: bool = False
    preprocessing_num_workers: Optional[int] = None
    block_size: Optional[int] = None
    

@dataclass
class MyTrainingArguments(TrainingArguments):
    modules_to_save: Optional[str] = None
    
    # 模型初始化方式
    init_from: Optional[str] = "scratch"
    use_device: Optional[str] = 'cuda'
    use_compile: Optional[bool] = False
    log_file: Optional[str] = None
    nnodes: Optional[int] = None
    nproc_per_node: Optional[int] = None
    eval_strategy: Optional[str] = None
    eval_steps: Optional[int] = None


class MultiWindowClassification(torch.nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model
        self.segment_weights = torch.nn.Parameter(torch.ones(2))
        self.softmax = torch.nn.Softmax(dim=0)
        
    def forward(self, segment_1, segment_2, labels=None):
        # 检查输入维度是否匹配
        if segment_1['input_ids'].size(0) != segment_2['input_ids'].size(0):
            raise ValueError("输入的段落长度不匹配。")
        
        # 获取两个segment的输出
        outputs_1 = self.base_model(
            input_ids=segment_1['input_ids'],
            attention_mask=segment_1['attention_mask']
        )
        
        outputs_2 = self.base_model(
            input_ids=segment_2['input_ids'],
            attention_mask=segment_2['attention_mask']
        )
  
        weights = self.softmax(self.segment_weights)

        final_logits = weights[0] * outputs_1.logits + weights[1] * outputs_2.logits
        
        if labels is not None:
            if labels.max() >= 2 or labels.min() < 0:
                raise ValueError("标签超出范围，应该在 [0, 1] 之间。")
            
            loss_fct = torch.nn.CrossEntropyLoss()
            loss = loss_fct(final_logits.view(-1, 2), labels.view(-1))
            return {'loss': loss, 'logits': final_logits}
        
        return {'logits': final_logits}

def collate_fn(batch):
    segment_1_input_ids = []
    segment_1_attention_mask = []
    segment_2_input_ids = []
    segment_2_attention_mask = []
    labels = []

    for item in batch:
        segment_1_input_ids.append(item['segment_1']['input_ids'])
        segment_1_attention_mask.append(item['segment_1']['attention_mask'])
        segment_2_input_ids.append(item['segment_2']['input_ids'])
        segment_2_attention_mask.append(item['segment_2']['attention_mask'])
        labels.append(item['labels'])
    
    return {
        'segment_1': {
            'input_ids': torch.tensor(segment_1_input_ids),
            'attention_mask': torch.tensor(segment_1_attention_mask)
        },
        'segment_2': {
            'input_ids': torch.tensor(segment_2_input_ids),
            'attention_mask': torch.tensor(segment_2_attention_mask)
        },
        'labels': torch.tensor(labels, dtype=torch.long)
    }

class WeightLoggingCallback(TrainerCallback):
    def __init__(self, logger):
        self.logger = logger

    def on_evaluate(self, args, state, control, model=None, **kwargs):
        if model is not None:
            weights = torch.nn.functional.softmax(model.segment_weights, dim=0)
            
            weights_float = weights.detach().cpu().float()
            self.logger.info(f"Segment weights: {weights_float.numpy()}")

def init_model(model_args):
    # 初始化tokenizer和模型
    tokenizer = AutoTokenizer.from_pretrained(model_args.model_path, trust_remote_code=True)

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = 'right'  # 确保padding添加在右侧
    
    config = AutoConfig.from_pretrained(
        model_args.model_path, 
        trust_remote_code=True, 
        num_labels=2,
        pad_token_id=tokenizer.eos_token_id
    )
    
    # 确定数据类型
    dtype = torch.bfloat16 if model_args.torch_dtype == 'bfloat16' else torch.float32
    print(f"Using dtype: {dtype}")
    
    base_model = AutoModelForSequenceClassification.from_pretrained(
        model_args.model_path,
        trust_remote_code=True,
        config=config,
        torch_dtype=dtype
    )
    
    # 确保pad_token_id设置正确
    if base_model.config.pad_token_id is None:
        base_model.config.pad_token_id = base_model.config.eos_token_id
    
    model = MultiWindowClassification(base_model)

    # 使用safetensors加载训练好的权重,对于训练好的模型再微调
#    if model_args.checkpoint_path.endswith('.safetensors'):
#        state_dict = load_file(model_args.checkpoint_path)
#    else:
#        state_dict = torch.load(model_args.checkpoint_path, map_location='cpu')
    
#    model.load_state_dict(state_dict)
    model = model.to(dtype=dtype)
    
    return tokenizer, model

def main():
    parser = HfArgumentParser((ModelArguments, DataTrainingArguments, MyTrainingArguments))
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()

    # 设置日志记录器
    logging.basicConfig(filename=training_args.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    # 创建文件处理器，并设置写模式
    file_handler = logging.FileHandler(training_args.log_file, mode='w')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    # 输出日志到控制台（可选）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    tokenizer, model =init_model(model_args)
    model.to(training_args.use_device)

    if training_args.use_compile:
        model = torch.compile(model)

    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    logger.info(f"总参数: {total_params}")
    logger.info(f"可训练参数: {trainable_params}")

    logger.info(f"torch_dtype:{model_args.torch_dtype}")
    logger.info(f"training_args.bf16: {training_args.bf16}")
    

    # 加载数据集并划分成训练和验证集
    train_dataset = DecisionDataset(
        data_path=data_args.train_dataset_file,
        tokenizer=tokenizer,
        max_length=data_args.block_size
    )
    eval_dataset = DecisionDataset(
        data_path=data_args.eval_dataset_file,
        tokenizer=tokenizer,
        max_length=data_args.block_size
    )

    logger.info(f"Train dataset size: {len(train_dataset)}")
    logger.info(f"Eval dataset size: {len(eval_dataset)}")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=collate_fn,
        callbacks=[
            LoggingCallback(logger),
            WeightLoggingCallback(logger)
        ],
    )

    trainer.train()

if __name__ == "__main__":
    main()
