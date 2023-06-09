from typing import List, Tuple
from dotenv import load_dotenv
import requests
import os


load_dotenv()


def get_associations(document: str, pubmed_id: str, pairs: List[Tuple[str, str]]):
    """
    Get associations using Falcon LLM.

    Args:
        document (str): Text (abstract or full text)
        pubmed_id (str): PubMed ID
        pairs (List[Tuple[str, str]]): Gene-disease pairs

    Returns:
        str: Response
    """
    gene_id, disease_id, disease_umls = ([] for _ in range(3))
    pre_prompt: list = []
    for index, item in enumerate(pairs, 1):
        pre_prompt.append(
            f"{index}) {item[0][0].strip()} associated with {item[1][0].strip()}?"
        )
    pre_prompt = "\n".join(pre_prompt)
    prompt = f"""
    According to this abstract:\n
{document.strip()}\n
Can you tell me if:\n
{pre_prompt.strip()}\n
As result, provide me only CSV with:
- Boolean result (only 'Yes' or 'No')
- The entire part before the sentence "is associated with"
- The entire part after the sentence "is associated with"
For instance:
'Yes,X,Y'
Also, remove the numbers list (like 1)) from the CSV
    """.strip()
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
    api_url: str = (
        "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    )
    response = requests.post(
        api_url, headers=headers, json={"inputs": f"{prompt}"}, timeout=60
    )
    result = response.json()[0]["generated_text"]
    with open(f"output/{pubmed_id}/falcon_results.csv", "w") as f:
        f.write("result,gene,disease")
        f.write(result)
    return result


def summarize(document: str, pubmed_id: str) -> str:
    """
    Summarize the paper.

    Args:
        document (str): Text (abstract or full text)
        pubmed_id (str): PubMed ID

    Returns:
        str: Digest
    """
    prompt = f"""
Summarize this text, trying to keep all relevant informations:
{document.strip()}
    """
    headers: dict = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
    api_url: str = (
        "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    )
    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": f"{prompt}", "max_tokens": 1024},
        timeout=60,
    )
    result: str = response.json()[0]["generated_text"]
    with open(f"output/{pubmed_id}/falcon_digest.txt", "w") as f:
        f.write(result)
    return result
