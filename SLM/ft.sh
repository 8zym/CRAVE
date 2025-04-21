

lr=5e-5
block_size=512

per_device_train_batch_size=12
gradient_accumulation_steps=1
model_path=../roberta-base
checkpoint_path=./output/output2/checkpoint-1128/model.safetensors
train_dataset_file=../data/train/gold/ft_data_train.json
eval_dataset_file=../data/train/gold/ft_data_eval.json
log_file=./log/ft16.log
output_dir=./output/output14
deepspeed_config_file=./ds_config.json
CUDA_LAUNCH_BLOCKING=1 torchrun --nnodes 1 --nproc_per_node 4 --master_port=29502 SLM.py \
    --deepspeed ${deepspeed_config_file} \
    --model_path ${model_path} \
    --train_dataset_file ${train_dataset_file} \
    --per_device_train_batch_size ${per_device_train_batch_size} \
    --checkpoint_path ${checkpoint_path} \
    --do_train \
    --bf16 True\
    --torch_dtype bfloat16 \
    --num_train_epochs 5 \
    --logging_strategy steps \
    --logging_steps 100 \
    --log_file ${log_file} \
    --logging_first_step True \
    --adam_beta1 0.9 \
    --adam_beta2 0.999  \
    --lr_scheduler_type cosine \
    --learning_rate ${lr} \
    --warmup_ratio 0.1 \
    --weight_decay 0.01 \
    --save_strategy epoch \
    --save_total_limit 5 \
    --save_steps 1000 \
    --gradient_accumulation_steps ${gradient_accumulation_steps} \
    --block_size ${block_size} \
    --output_dir ${output_dir} \
    --overwrite_output_dir \
    --ddp_timeout 30000 \
    --use_device cuda \
    --use_compile False \
    --eval_strategy steps \
    --eval_steps 200 \
    --eval_dataset_file ${eval_dataset_file} \
    --num_heads 8 \
    
