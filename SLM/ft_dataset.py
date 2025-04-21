import numpy as np
from torch.utils.data import Dataset,DataLoader
import torch
from datasets import load_dataset,Features, Value

class DecisionDataset(Dataset):
    def __init__(self, data_path, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.data_path = data_path
        self.max_length = max_length
        self.labels = []
        self.examples = []


        features = Features({
            'claim': Value('string'),
            'rationale_true': Value('string'),
            'rationale_false': Value('string'),
            'label': Value('string'),
            'predicted_label': Value('string'),
        })

        self.dataset = load_dataset('json', data_files=data_path, features=features)

        for entry in self.dataset['train']:
            claim = entry['claim']
            rationale_true = entry['rationale_true']
            rationale_false = entry['rationale_false']
            label = entry['label']
            predicted_label = entry['predicted_label']

            if predicted_label == 'true':
                text_1 = f"{claim} [SEP] {rationale_true}"
                text_2 = f"{claim} [SEP] {rationale_false}"
            elif predicted_label == 'false':
                text_1 = f"{claim} [SEP] {rationale_false}"
                text_2 = f"{claim} [SEP] {rationale_true}"
            else:
                continue

            self.examples.append((text_1, text_2))
            self.labels.append(0 if label == 'refutes' else 1)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        text_1, text_2 = self.examples[idx]
        label = self.labels[idx]
        
        encoding_1 = self.tokenizer(
            text_1,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors=None
        )
        
        encoding_2 = self.tokenizer(
            text_2,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors=None
        )
        
        return {
            'segment_1': {
                'input_ids': encoding_1['input_ids'],
                'attention_mask': encoding_1['attention_mask'],
            },
            'segment_2': {
                'input_ids': encoding_2['input_ids'],
                'attention_mask': encoding_2['attention_mask'],
            },
            'labels': label
        }