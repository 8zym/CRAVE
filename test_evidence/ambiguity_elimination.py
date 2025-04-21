from args import *
import random
from tqdm import tqdm
import re
import pandas as pd
import os
import json
from retriever import PyseriniRetriever
import openai
from prompts import *
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

openai.api_key = "your-openai-api-key"

def extract_part(response):
    try:
        prediction = re.search("\[(.*?)\]", response).group(1)
        return prediction
    except:
        return None

def parse_command(command, variable_map, pattern, command_type):
    return_var, _ = command.split(f'= {command_type}')
    return_var = return_var.strip()
    
    matching = re.findall(pattern, command)
    content = matching[0] if matching else _
    
    # Replace variables
    for variable_name, variable_value in variable_map.items():
        replace_var = "{" + str(variable_name) + "}"
        if replace_var in content:
            content = content.replace(replace_var, str(variable_value))
            
    return return_var, content

def parse_verify_command(command, variable_map):
    pattern = r'Verify\([f]?\"(.*)\"\)'
    return parse_command(command, variable_map, pattern, "Verify")

def parse_question_command(command, variable_map):
    pattern = r'Question\([f]?\"(.*)\"\)'
    return parse_command(command, variable_map, pattern, "Question")

def retrieve_evidence(query):
    index_paths = {
        'hover': "../HOVER/corpus/index",
        'feverous': "../FEVEROUS/corpus/index",
    }
    
    searcher = PyseriniRetriever(index_paths[args.dataset], use_bm25=True, k1=0.9, b=0.4)
    hits = searcher.retrieve(query, args.num_retrieved)
    
    evidence = '\n'.join([hit['text'].strip() for hit in hits])
    
    # Cut overlong evidence
    if len(evidence.split()) > args.max_evidence_length:
        print('Evidence is too long, cutting to max_evidence_length')
        evidence = ' '.join(evidence.split()[:args.max_evidence_length])
    
    # Save retrieval results
    retrieved_results = [
        {'id': hit['doc_id'], 'score': hit['score'], 'query': query}
        for hit in hits
    ]
    
    return evidence, retrieved_results

def answer_question(question, evidence):
    full_prompt = answer_question_gpt % (question, evidence)
    if args.model == "gpt-3.5-turbo":
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": full_prompt}],
                max_tokens=args.max_token,
                temperature=args.temperature,
            )
            response = completion.choices[0].message.content
            answer = extract_part(response)
            return answer or " "
        except Exception as e:
            print(f"Error in answer_question: {e}")
            return " "
        
def entity_finding(claim, entity):
    full_prompt = entity_program % (claim)
    if args.model == "gpt-3.5-turbo":
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": full_prompt}],
                max_tokens=args.max_token,
                temperature=args.temperature,
            )
            response = completion.choices[0].message.content
            entities = extract_part(response)            
            if entities:
                entity_list = [e.strip() for e in entities.split(',')]
                entity_set = set(entity)
                entity_set.update(entity_list)
                entity = list(entity_set)
            return entity
        except Exception as e:
            print(f"Error in entity_finding: {e}")
            return entity
        
def process_single_item_hover(item):
    uid,claim,label,evidence,program,num_hops = item

    variable_map = {}
    entity = []

    questions = re.findall(r'^\s*answer_\d\s*=\s*Question\(".*?"\)', program, re.MULTILINE)

    for q in questions:
        return_var,question = parse_question_command(q,variable_map)

        retrieved_evidence,_ = retrieve_evidence(question)

        answer = answer_question(question,retrieved_evidence)

        variable_map[return_var] = answer

        if(answer!=" "):
            entity.append(answer)

    entity = entity_finding(claim,entity)
    print(entity)

    return{ "id": uid,
            "label": label,
            "claim": claim,
            "program": program,
            "evidence": evidence,
            "num_hops": num_hops,
            "entity": entity}

def process_single_item_feverous(item):
    uid,claim,label,evidence,program,challenge = item

    variable_map = {}
    entity = []

    questions = re.findall(r'^\s*answer_\d\s*=\s*Question\(".*?"\)', program, re.MULTILINE)

    for q in questions:
        return_var,question = parse_question_command(q,variable_map)

        retrieved_evidence,_ = retrieve_evidence(question)

        answer = answer_question(question,retrieved_evidence)

        variable_map[return_var] = answer

        if(answer!=" "):
            entity.append(answer)

    entity = entity_finding(claim,entity)
    print(entity)

    return{ "id": uid,
            "label": label,
            "claim": claim,
            "program": program,
            "evidence": evidence,
            "challenge": challenge,
            "entity": entity}

def process_dataset(dataset_name):

    if dataset_name == "hover":
        input_file = f"./HOVER/programs/{args.model}_programs_{args.num_eval_samples}_{args.version}_dev.json"
        output_dir = f"./HOVER/execution"
        os.makedirs(output_dir, exist_ok=True)

    elif dataset_name == "feverous":
        input_file = f"./FEVEROUS/programs/{args.model}_programs_{args.num_eval_samples}_{args.version}_dev.json"
        output_dir = f"./FEVEROUS/execution"
        os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/{args.model}_execution_{args.num_eval_samples}_{args.version}_dev.json"
    
    with open(input_file, 'r') as f:
        dataset = pd.read_json(f)
    
    out = []
    if args.dataset == "hover":
        data_items = list(zip(dataset.id, dataset.claim, dataset.label, dataset.evidence, dataset.program,dataset.num_hops))

        with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
            results = list(tqdm(executor.map(process_single_item_hover,data_items),total=len(data_items),desc="Processing items"))

        with open(output_file,'w') as f:
            json.dump(results,f,indent=4)

        print("Done!")

    elif args.dataset == "feverous":
        data_items = list(zip(dataset.id, dataset.claim, dataset.label, dataset.evidence, dataset.program,dataset.challenge))

        with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
            results = list(tqdm(executor.map(process_single_item_feverous,data_items),total=len(data_items),desc="Processing items"))

        with open(output_file,'w') as f:
            json.dump(results,f,indent=4)

        print("Done!")

def execute_on_dataset():
    process_dataset(args.dataset)

if __name__ == "__main__":
    print(args)
    execute_on_dataset()