from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceHub
from typing import List, Tuple
from dotenv import load_dotenv
import os
from .pre_prompt import pre_prompt

load_dotenv()


def create_embeddings(splitted_text: List) -> HuggingFaceHubEmbeddings:
    """
    Create embeddings from chunks for Zephyr.

    Args:
        splitted_text (List): List of chunks

    Returns:
        Any: Embeddings
    """
    embeddings = HuggingFaceHubEmbeddings(
        repo_id="sentence-transformers/all-mpnet-base-v2",
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    )
    vectorstore = FAISS.from_texts(texts=splitted_text, embedding=embeddings)
    vectorstore.save_local("vector_db")
    persisted_vectorstore = FAISS.load_local("vector_db", embeddings)
    return persisted_vectorstore


def retriever(query: str, embeddings: HuggingFaceHubEmbeddings) -> str:
    """
    Create retriever for Zephyr.

    Args:
        query (str): Query
        embeddings (HuggingFaceHubEmbeddings): Embeddings

    Returns:
        str: Result of retriever
    """
    retriever = embeddings.as_retriever(search_type="similarity")
    result = RetrievalQA.from_chain_type(
        llm=HuggingFaceHub(
            repo_id="HuggingFaceH4/zephyr-7b-alpha",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        ),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return result(query)["result"]


def get_associations(
    pairs: List[Tuple[str, str]], embeddings: HuggingFaceHubEmbeddings
) -> str:
    pre_prompt_pairs: list = []
    for index, item in enumerate(pairs, 1):
        pre_prompt_pairs.append(
            f"{index}) {item[0][0].strip()} associated with {item[1][0].strip()}?"
        )
    pre_prompt_pairs = "\n".join(pre_prompt_pairs)
    query = f"""
According to the text provided, can you tell me if:
{pre_prompt_pairs.strip()}\n
As result, provide me a CSV with:
- Boolean result (only 'Yes' or 'No')
- The entire part before the sentence "is associated with"
- The entire part after the sentence "is associated with"
For instance:
'Yes,X,Y'
Also, remove the numbers list (like 1)) from the CSV.
    """.strip()
    prompt = pre_prompt.format(query=query)
    retriever = embeddings.as_retriever(search_type="similarity")
    result = RetrievalQA.from_chain_type(
        llm=HuggingFaceHub(
            repo_id="HuggingFaceH4/zephyr-7b-alpha",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        ),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return result(prompt)["result"]
