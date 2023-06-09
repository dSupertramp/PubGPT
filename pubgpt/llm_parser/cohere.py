from typing import List, Tuple
from dotenv import load_dotenv
import cohere
import os


load_dotenv()


def get_associations(
    document: str, pubmed_id: str, pairs: List[Tuple[str, str]]
) -> str:
    """
    Get associations using Cohere LLM.

    Args:
        document (str): Text (abstract or full text)
        pubmed_id (str): PubMed ID
        pairs (List[Tuple[str, str]]): Gene-disease pairs

    Returns:
        str: Response
    """
    temperature, max_tokens = (0, 500)
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
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = (
        co.generate(
            model="command-xlarge-nightly",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        .generations[0]
        .text
    )
    with open(f"output/{pubmed_id}/cohere_results.csv", "w") as f:
        f.write("result,gene,disease")
        f.write(response)
    return response


def summarize(document: str, pubmed_id: str) -> str:
    prompt = f"""
Summarize this text, trying to keep all relevant informations:
{document.strip()}
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    temperature, max_tokens = (0, 500)
    response = (
        co.generate(
            model="command-xlarge-nightly",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        .generations[0]
        .text
    )
    with open(f"output/{pubmed_id}/cohere_digest.txt", "w") as f:
        f.write(response)
    return response
