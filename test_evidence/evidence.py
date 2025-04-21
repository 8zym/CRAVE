from args import *
import os
import json
from tqdm import tqdm
import pandas as pd
from prompts import *
import requests
from bs4 import BeautifulSoup
from rank_bm25 import BM25Okapi
import string
import nltk


def preprocess_text(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

def fetch_wikipedia_page(entity):
    url = f"http://127.0.0.1:9454/{entity}"
    content_list = []
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content,'html.parser')

            paragraphs = soup.find_all('p')
            for i,para in enumerate(paragraphs,start=1):
                if(len(para) > 10):
                    content_list.append(para.get_text())

        else:
            print(f"Cant find {entity}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return content_list

def retrieve_bm25_relevant_content(claim, evidence_corpus):
    # Preprocess claim and evidence corpus
    if evidence_corpus == []:
        return []

    claim_processed = preprocess_text(claim)
    evidence_processed = [preprocess_text(text) for text in evidence_corpus]

    # Initialize BM25
    bm25 = BM25Okapi(evidence_processed)

    # Get BM25 scores for the claim
    claim_tokens = claim_processed.split()
    scores = bm25.get_scores(claim_tokens)

    # Sort evidence based on BM25 scores (relevant content will have higher scores)
    sorted_evidence = [evidence_corpus[i] for i in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)]

    return sorted_evidence[:3]  # Return top 5 most relevant pieces of evidence

def main():
    if args.dataset == 'hover':
        out = []
        if not os.path.exists("./HOVER/evidence"):
            os.makedirs("./HOVER/evidence")

        with open(f"./HOVER/execution/{args.model}_execution_{args.num_eval_samples}_{args.version}_dev.json", 'r') as f:
            df = pd.read_json(f)

        for uid,claim,label,evidence,num_hop,entities in tqdm(zip(df.id,df.claim,df.label,df.evidence,df.num_hops,df.entity),total = len(df)):
            all_evidence = []  # List to store evidence pieces related to the claim

            for entity in entities:
                entity = entity.replace(" ", "_")
                wikipedia_content = fetch_wikipedia_page(entity)

                if wikipedia_content and isinstance(wikipedia_content, list):  # 确保返回值是非空列表

                    intro_lines = wikipedia_content[:2]  # 前两段
                    for line in intro_lines:
                        if line.strip():  # 确保非空
                            all_evidence.append(line.strip())

                    remaining_content = wikipedia_content[2:] 
                    if remaining_content:
                        relevant_evidence = retrieve_bm25_relevant_content(claim, remaining_content)
                        all_evidence.extend(relevant_evidence)
                else:
                    print(f"Error: Unexpected content format for {entity}")


            out.append({"id": uid, "label": label, "claim": claim,"evidence": evidence,"num_hops": num_hop,"entity":entities,"retrived_evidence":all_evidence})

        with open(f"./HOVER/evidence/{args.model}_evidence_{args.num_eval_samples}_{args.version}_dev.json", 'w') as f:
            json.dump(out, f,indent=4)

        print("Done!")

    elif args.dataset == 'feverous':
        out = []
        if not os.path.exists("./FEVEROUS/evidence"):
            os.makedirs("./FEVEROUS/evidence")

        with open(f"./FEVEROUS/execution/{args.model}_execution_{args.num_eval_samples}_{args.version}_dev.json", 'r') as f:
            df = pd.read_json(f)

        for uid,claim,label,evidence,challenge,entities in tqdm(zip(df.id,df.claim,df.label,df.evidence,df.challenge,df.entity),total = len(df)):
            all_evidence = []  # List to store evidence pieces related to the claim

            for entity in entities:
                entity = entity.replace(" ", "_")
                wikipedia_content = fetch_wikipedia_page(entity)

                if wikipedia_content and isinstance(wikipedia_content, list):  # 确保返回值是非空列表

                    intro_lines = wikipedia_content[:2]  # 前两段
                    for line in intro_lines:
                        if line.strip():  # 确保非空
                            all_evidence.append(line.strip())

                    remaining_content = wikipedia_content[2:] 
                    if remaining_content:
                        relevant_evidence = retrieve_bm25_relevant_content(claim, remaining_content)
                        all_evidence.extend(relevant_evidence)
                else:
                    print(f"Error: Unexpected content format for {entity}")


            out.append({"id": uid, "label": label, "claim": claim,"evidence": evidence,"challenge": challenge,"entity":entities,"retrived_evidence":all_evidence})

        with open(f"./FEVEROUS/evidence/{args.model}_evidence_{args.num_eval_samples}_{args.version}_dev.json", 'w') as f:
            json.dump(out, f,indent=4)

        print("Done!")

if __name__ == "__main__":
    print(args)

    main()

    