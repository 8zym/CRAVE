import pandas as pd
import re
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from args import *

def normalize_label(label):
    """标准化标签格式"""
    if isinstance(label, str):
        label = label.lower()
        if any(keyword in label for keyword in ['supports', 'true' , 'True','supported']):
            return 'true'           
        elif any(keyword in label for keyword in ['refutes', 'false' , 'False','refuted']):
            return 'false'
    return None

def compute_accuracy(predictions, golds):
    """计算准确率"""
    return sum(p == g for p, g in zip(predictions, golds)) / len(golds)

def get_wrong_predictions(predictions, labels):
    """获取错误预测的索引"""
    return [i for i, (p, l) in enumerate(zip(predictions, labels)) if p != l]

def evaluate_predictions(predictions, golds):
    """评估预测结果"""
    # 标准化标签
    norm_preds = [normalize_label(p) for p in predictions]
    norm_golds = [normalize_label(g) for g in golds]
    
    # 过滤无效预测
    valid_pairs = [(p, g) for p, g in zip(norm_preds, norm_golds) 
                  if p is not None and g is not None]
    if not valid_pairs:
        print("没有有效的预测结果")
        return
        
    final_preds, final_golds = zip(*valid_pairs)
    
    print(f"总预测数: {len(final_preds)}")
    
    # 计算准确率
    acc = compute_accuracy(final_preds, final_golds)
    print(f"准确率: {acc:.4f}")
    
    # 转换为数值标签
    label_map = {"false": 0, "true": 1}
    num_preds = [label_map[p] for p in final_preds]
    num_golds = [label_map[g] for g in final_golds]
    
    # 打印分类报告
    target_names = ["false", "true"]
    print("\n分类报告")
    print("=" * 60)
    print(classification_report(num_golds, num_preds,
                              target_names=target_names, digits=4))
    print("\n混淆矩阵:")                          
    print(confusion_matrix(num_golds, num_preds))
    
    # 获取错误预测
    wrong_indices = get_wrong_predictions(num_preds, num_golds)
    print("\n错误预测的索引:")
    print(wrong_indices)
    
    return acc, wrong_indices

if __name__ == "__main__":
    for dataset in ['hover', 'feverous']:
        if args.dataset == dataset:
            print(f"\n评估数据集: {dataset.upper()}")
            print("=" * 60)
            
            # 读取数据
            rationale_file = f"./{dataset.upper()}/rationale/{args.model}_rationale_{args.num_eval_samples}_{args.version}.json"
            df = pd.read_json(rationale_file)
            
            # 如果是 hover 数据集，过滤指定 hop 数的数据
            # if dataset == 'hover':
            #     df = df[df["num_hops"] == args.hover_num_hop]
            
            filter_condition = ~(
                df["gpt_label"].str.contains("This is a test!", na=False) |
                df["rationale_true"].str.contains("This is a test!", na=False) |
                df["rationale_false"].str.contains("This is a test!", na=False)
            )
            df = df[filter_condition]
            
            # 评估预测
            evaluate_predictions(df["gpt_label"].tolist(), df["label"].tolist())
