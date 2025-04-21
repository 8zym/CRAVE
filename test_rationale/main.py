from args import *
import random
from tqdm import tqdm
import re
import pandas as pd
import os
import json
import openai
from prompts import *
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

openai.api_key = "your-openai-api-key"

def process_single_item_hover(item):
    uid, claim, label, evidence, num_hops = item
    error_count = 0
    
    try:
        full_prompt = LLM_rationale_true % (claim,evidence)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        response_true = completion.choices[0].message.content

        full_prompt = LLM_rationale_false % (claim,evidence)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        response_false = completion.choices[0].message.content

        full_prompt = LLM_decide % (claim, response_true, response_false)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        gpt_label = completion.choices[0].message.content

        print(gpt_label)
        return {"id": uid, "label": label, "claim": claim, "evidence": evidence,
                "rationale_true": response_true, "rationale_false": response_false, "gpt_label": gpt_label, "num_hops": num_hops}
    
    except openai.InternalServerError:
        error_count += 1
        print(f"Skipping item {uid} due to InternalServerError.")
        return None


def process_single_item_feverous(item):
    uid, claim, label, evidence, challenge = item
    error_count = 0

    try:
        full_prompt = LLM_rationale_true % (claim,evidence)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        response_true = completion.choices[0].message.content

        full_prompt = LLM_rationale_false % (claim,evidence)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        response_false = completion.choices[0].message.content

        full_prompt = LLM_decide % (claim, response_true, response_false)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            max_tokens=args.max_token,
            temperature=args.temperature,
        )
        gpt_label = completion.choices[0].message.content

        print(gpt_label)
        return {"id": uid, "label": label, "claim": claim, "evidence": evidence,
                "rationale_true": response_true, "rationale_false": response_false, "gpt_label": gpt_label, "challenge": challenge}
    
    except openai.InternalServerError:
        error_count += 1
        print(f"Skipping item {uid} due to InternalServerError.")
        return None
    
    except openai.BadRequestError:
        error_count += 1
        print(f"Skipping item {uid} due to BadRequestError.")
        return 
    
    except openai.APITimeoutError:
        error_count += 1
        print(f"Skipping item {uid} due to timeouterror.")
        return 
    
    except openai.APIConnectionError:
        error_count += 1
        print(f"Skipping item {uid} due to APIconnectionError.")
        return 
    
    except Exception as e:
        error_count += 1
        print(f"Skipping item {uid} due to an error: {str(e)}")
        return None

def LLM_rationale():
    error_count = 0
    totol_num = 0

    if args.dataset == 'hover':
        out = []
        if not os.path.exists("./HOVER/rationale"):
            os.makedirs("./HOVER/rationale")

        with open(f"../test_evidence/HOVER/{args.model}_{args.num_eval_samples}_{args.version}.json", 'r') as f:
            dataset = pd.read_json(f)  

        df = dataset
        data_items = list(zip(df.id, df.claim, df.label, df.retrieved_evidence, df.num_hops))

        with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
            results = []
            for result in tqdm(executor.map(process_single_item_hover, data_items), total=len(data_items), desc="Processing items"):
                if result is not None:
                    results.append(result)
                else:
                    error_count += 1

        with open(f"./HOVER/rationale/{args.model}_rationale_{args.num_eval_samples}_{args.version}.json", 'w') as f:
            json.dump(results, f, indent=4)

        print(f"Done! Total InternalServerError skipped: {error_count}")

    if args.dataset == 'feverous':
        out = []
        if not os.path.exists("./FEVEROUS/rationale"):
            os.makedirs("./FEVEROUS/rationale")

        with open(f"../test_evidence/FEVEROUS/{args.model}_{args.num_eval_samples}_{args.version}.json", 'r') as f:
            dataset = pd.read_json(f)  

        df = dataset
        data_items = list(zip(df.id, df.claim, df.label, df.retrieved_evidence, df.challenge))

        with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
            results = []
            for result in tqdm(executor.map(process_single_item_feverous, data_items), total=len(data_items), desc="Processing items"):
                if result is not None:
                    results.append(result)
                    totol_num += 1
                    if totol_num % 1000 == 0:
                        with open(f"./FEVEROUS/rationale/{args.model}_rationale_{args.num_eval_samples}_{args.version}.json", 'w') as f:
                            json.dump(results, f, indent=4)
                else:
                    error_count += 1

        with open(f"./FEVEROUS/rationale/{args.model}_rationale_{args.num_eval_samples}_{args.version}.json", 'w') as f:
            json.dump(results, f, indent=4)

        print(f"Done! Total InternalServerError skipped: {error_count}")

if __name__ == "__main__":
    print(args)
    LLM_rationale()
