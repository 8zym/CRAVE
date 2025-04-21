from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import json
from tqdm import tqdm
from SLM import MultiWindowClassification 
from safetensors.torch import load_file  

def load_model_and_tokenizer(model_path, tokenizer_path, checkpoint_path):
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_path, 
        trust_remote_code=True
    )
    tokenizer.padding_side = 'right'

    base_model = AutoModelForSequenceClassification.from_pretrained(
        model_path,
        trust_remote_code=True,
        num_labels=2
    )
    
    model = MultiWindowClassification(base_model)

    if checkpoint_path.endswith('.safetensors'):
        state_dict = load_file(checkpoint_path)
    else:
        state_dict = torch.load(checkpoint_path, map_location='cpu')
    
    model.load_state_dict(state_dict)
    
    return model, tokenizer

def process_text(text, tokenizer, max_length=512):
    return tokenizer(
        text,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

def predict(model, tokenizer, text1, text2):
    segment_1 = process_text(text1, tokenizer)
    segment_2 = process_text(text2, tokenizer)
    
    device = next(model.parameters()).device
    segment_1 = {k: v.to(device) for k, v in segment_1.items()}
    segment_2 = {k: v.to(device) for k, v in segment_2.items()}
    
    model.eval()
    with torch.no_grad():
        outputs = model(segment_1, segment_2)
        logits = outputs['logits']
        probs = torch.nn.functional.softmax(logits, dim=-1)
        print(probs)
        predicted_label = torch.argmax(probs, dim=-1).item()
    
        weights = torch.nn.functional.softmax(model.segment_weights, dim=0)
        
        return {
            'label': predicted_label,
            'probabilities': probs[0].tolist(),
            'segment_weights': weights.tolist()
        }

def main():
    # replace with your path
    model_path = "../roberta-base"  
    tokenizer_path = "../roberta-base"  
    checkpoint_path = "./output/output6/checkpoint-750/model.safetensors" 
    
    model, tokenizer = load_model_and_tokenizer(model_path, tokenizer_path, checkpoint_path)
    model.to('cuda' if torch.cuda.is_available() else 'cpu')

    test_file = "../data/dev/hover-gpt-3.5-turbo_rationale_-1_V1.0_processed_dev.json" #replace with your data path
    with open(test_file, 'r', encoding='utf-8') as f:
        test_data = [json.loads(line) for line in f]
    
    results = []
    for item in tqdm(test_data):
        # if not any(key in item['challenge'] for key in ['Reasoning','Others']):
        #    continue
        if item['num_hops'] != 3:
           continue
        claim = item['claim']
        rationale_true = item['rationale_true']
        rationale_false = item['rationale_false']
        if item['gpt_label'] == 'true':
            text_1 = f"{claim} [SEP] {rationale_true}"
            text_2 = f"{claim} [SEP] {rationale_false}"
        elif item['gpt_label'] == 'false':
            text_1 = f"{claim} [SEP] {rationale_false}"
            text_2 = f"{claim} [SEP] {rationale_true}"
        else:
            continue

        true_label = item['label']  
        
        prediction = predict(model, tokenizer, text_1, text_2)
        
        print(f"\n预测结果:")
        if true_label == "refutes":
            true_label = 0
        else:
            true_label = 1
        print(f"真实标签: {true_label},预测标签: {prediction['label']}")

        results.append({
            'text1': text_1,
            'text2': text_2,
            'true_label': true_label,
            'predicted_label': prediction['label'],
            'probabilities': prediction['probabilities'],
            'segment_weights': prediction['segment_weights']
        })
    
    correct = sum(1 for r in results if r['true_label'] == r['predicted_label'])
    print(correct)
    print(len(results))
    accuracy = correct / len(results)
    print(f"\n总体准确率: {accuracy:.4f}")
    
if __name__ == "__main__":
    main()