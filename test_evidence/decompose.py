from args import *
import os
import json
from tqdm import tqdm
import pandas as pd
import openai
from prompts import *
from multiprocessing import Pool, cpu_count

openai.api_key = "your-openai-api-key"

def process_hover_item(item):
    uid, claim, label, evidence, num_hop = item
    full_prompt = PROGRAM_FC % (claim)
    if args.model == "gpt-3.5-turbo":
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        response = completion.choices[0].message.content
        return {"id": uid, "label": label, "claim": claim, "program": response, "evidence": evidence, "num_hops": num_hop}

def process_feverous_item(item):
    uid, claim, label, evidence, challenge = item
    full_prompt = PROGRAM_FC % (claim)
    if args.model == "gpt-3.5-turbo":
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        response = completion.choices[0].message.content
        return {"id": uid, "label": label, "claim": claim, "program": response, "evidence": evidence, "challenge": challenge}

def batch_generate_programs(dataset, output_dir, process_func):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load dataset
    with open(dataset, 'r') as f:
        raw_dataset = pd.read_json(f)

    raw_dataset = raw_dataset if args.num_eval_samples < 0 else raw_dataset.sample(args.num_eval_samples)
    print(f"Loaded {len(raw_dataset)} examples from dataset.")

    items = list(zip(raw_dataset.id, raw_dataset.claim, raw_dataset.label, raw_dataset.evidence, raw_dataset.get('num_hops', raw_dataset.get('challenge'))))
    
    # Use multiprocessing to process items in parallel
    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_func, items), total=len(items)))

    output_file = os.path.join(output_dir, f"{args.model}_programs_{args.num_eval_samples}_{args.version}_dev.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Programs saved to {output_file}")
    print("Done!")

if __name__ == "__main__":
    print(args)

    if args.dataset == 'hover':
        batch_generate_programs(
            dataset="../HOVER/claims/dev.json",
            output_dir="./HOVER/programs",
            process_func=process_hover_item
        )
    elif args.dataset == 'feverous':
        batch_generate_programs(
            dataset="../FEVEROUS/claims/dev.json",
            output_dir="./FEVEROUS/programs",
            process_func=process_feverous_item
        )
