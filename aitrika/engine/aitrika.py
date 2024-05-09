from Bio import Entrez, Medline
import pandas as pd
import requests
import json
from io import StringIO
from PyPDF2 import PdfReader
import re
import spacy
from prompts.prompts import results_prompt
from llm.base_llm import BaseLLM


class AItrikaBase:
    """
    Base AItrika class.
    """

    def __init__(self):
        self.record = None
        self.data = None

    def _paper_knowledge(self):
        """
        Extract the knowledge of the paper (title, abstract etc.).
        """
        Entrez.email = "mail@mail.com"
        handle = Entrez.efetch(
            db="pubmed", id=self.pubmed_id, rettype="medline", retmode="text"
        )
        self.record = Medline.read(handle)

    def _data_knowledge(self):
        """
        Extract knowledge of the content of the paper (genes, diseases etc.).
        """
        url = f"https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson?pmids={self.pubmed_id}&full=true"
        response = requests.get(url).json()
        annotations, informations = [], []
        for item in response["PubTator3"]:
            for passage in item["passages"]:
                annotations.extend(passage["annotations"])
            for annotation in annotations:
                new_annotation = {
                    "identifier": annotation["infons"]["identifier"],
                    "text": annotation["text"],
                    "type": annotation["infons"]["type"],
                    "database": annotation["infons"]["database"],
                    "normalized_id": annotation["infons"]["normalized_id"],
                    "name": annotation["infons"]["name"],
                    "biotype": annotation["infons"]["biotype"],
                }
                informations.append(new_annotation)
            data = [dict(t) for t in {tuple(d.items()) for d in informations}]
            data = json.dumps(data)
        self.data = data

    def _extract_full_response(self) -> json:
        """
        Extract full response from PubTator API.

        Returns:
            json: JSON Response
        """
        url = f"https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson?pmids={self.pubmed_id}&full=true"
        response = requests.get(url).json()
        return response

    def get_pubmed_id(self) -> str:
        """
        Extract PubMed ID.

        Returns:
            str: PubMed ID
        """
        return self.record.get("PMID", "")

    def get_title(self) -> str:
        """
        Extract title.

        Returns:
            str: Title
        """
        return self.record.get("TI", "")

    def abstract(self) -> str:
        """
        Extract abstract.

        Returns:
            str: Abstract
        """
        return self.record.get("AB", "")

    def other_abstract(self) -> str:
        """
        Extract other abstract (if available).

        Returns:
            str: Other abstract
        """
        return self.record.get("OAB", "")

    def genes(self, dataframe: bool = False):
        """
        Extract genes.

        Args:
            dataframe (bool, optional): Format into DataFrame. Defaults to False.

        Returns:
            pd.DataFrame | json: Genes
        """
        df = pd.read_json(StringIO(self.data))
        df = df[df["type"] == "Gene"]
        df = df.drop_duplicates()
        if dataframe:
            return df
        else:
            return df.to_json()

    def diseases(self, dataframe: bool = False):
        """
        Extract diseases.

        Args:
            dataframe (bool, optional): Format into DataFrame. Defaults to False.

        Returns:
            pd.DataFrame | json: Genes
        """
        df = pd.read_json(StringIO(self.data))
        df = df[df["type"] == "Disease"]
        df = df.drop_duplicates()
        if dataframe:
            return df
        else:
            return df.to_json()

    def species(self, dataframe: bool = False):
        """
        Extract species.

        Args:
            dataframe (bool, optional): Format into DataFrame. Defaults to False.

        Returns:
            pd.DataFrame | json: Genes
        """
        df = pd.read_json(StringIO(self.data))
        df = df[df["type"] == "Species"]
        df = df.drop_duplicates()
        if dataframe:
            return df
        else:
            return df.to_json()

    def chemicals(self, dataframe: bool = False):
        """
        Extract chemicals.

        Args:
            dataframe (bool, optional): Format into DataFrame. Defaults to False.

        Returns:
            pd.DataFrame | json: Genes
        """
        df = pd.read_json(StringIO(self.data))
        df = df[df["type"] == "Chemical"]
        df = df.drop_duplicates()
        if dataframe:
            return df
        else:
            return df.to_json()

    def mutations(self, dataframe: bool = False):
        """
        Extract mutations.

        Args:
            dataframe (bool, optional): Format into DataFrame. Defaults to False.

        Returns:
            pd.DataFrame | json: Genes
        """
        df = pd.read_json(StringIO(self.data))
        df = df[df["type"] == "Mutation"]
        df = df.drop_duplicates()
        if dataframe:
            return df
        else:
            return df.to_json()

    def associations(self, dataframe: bool = False):
        """
        Extract associations between genes and diseases.

        Args:
            dataframe (bool, optional): Format into DataFrame. Defaults to False.

        Returns:
            pd.DataFrame | json: Genes
        """
        relations, associations = [], []
        data = self._extract_full_response()
        for item in data["PubTator3"]:
            relations.extend(item["relations_display"])
        for item in relations:
            name = item["name"]
            parts = name.split("|")
            disease = parts[1].replace("@DISEASE_", "").replace("_", " ")
            gene = parts[2].replace("@GENE_", "")
            associations.append({"gene": gene, "disease": disease})
        if dataframe:
            return pd.DataFrame(associations)
        else:
            return associations

    def results(self, llm: BaseLLM) -> str:
        """
        Extract results.

        Args:
            llm (BaseLLM): Provided LLM

        Returns:
            str: Results
        """
        return llm.query(query=results_prompt)


class OnlineAItrika(AItrikaBase):
    """
    AItrika engine for online search.

    Args:
        AItrikaBase (_type_): Base AItrika
    """

    def __init__(self, pubmed_id: str) -> None:
        super().__init__()
        self.pubmed_id = pubmed_id
        self._paper_knowledge()
        self._data_knowledge()

    def full_text(self) -> str:
        """
        Extract full text (if available):

        Returns:
            str: Full text
        """
        pmc_id = self.record.get("PMC", "")
        if pmc_id != "":
            handle = Entrez.efetch(db="pmc", id=pmc_id, rettype="full", retmode="text")
            full_text = handle.read()
            return full_text
        else:
            return ""


class LocalAItrika(AItrikaBase):
    """
    Local AItrika engine for local search.

    Args:
        AItrikaBase (_type_): Base AItrika
    """

    def __init__(self, pdf_path: str) -> None:
        super().__init__()
        self.pdf_path = pdf_path
        self.title = None
        self.authors = None
        self.pubmed_id = None
        self._extract_title_and_authors()
        self._retrieve_pubmed_id()
        self._paper_knowledge()
        self._data_knowledge()

    def _extract_title_and_authors(self):
        """
        Extract title and authors from PDF.
        """

        def _detect_authors(strings):
            nlp = spacy.load("en_core_web_sm")
            for s in strings:
                doc = nlp(s)
                names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
                if names:
                    return s
            return None

        def _detect_title(strings):
            author_string = _detect_authors(strings)
            abstract_string = next(
                (s for s in strings if s.lower().startswith("abstract")), None
            )
            special_strings = [s for s in strings if s.startswith(("[", "{", "("))]
            title_strings = [
                s
                for s in strings
                if s not in [author_string, abstract_string] + special_strings
            ]
            return title_strings[0] if title_strings else None

        with open(self.pdf_path, "rb") as f:
            reader = PdfReader(f)
            first_page = reader.pages[0].extract_text()
            lines = first_page.split("\n")
            pre_header = [line.strip() for line in lines if line.strip()]
            original_header = pre_header[:]  ## Copy of pre_header
            pre_header = [re.sub(r"\d+", "", s) for s in pre_header]  ## Remove numbers

            # Perform author and title detection on pre_header
            authors = _detect_authors(pre_header)
            title = _detect_title(pre_header)

            # Extract the actual title and authors from the original list
            original_title = original_header[pre_header.index(title)]
            original_authors = original_header[pre_header.index(authors)]

            ## Title
            title = re.sub(r"\b\d+\b", "", original_title)  ## Remove numbers and strip
            title = title.strip()

            ## Authors
            authors = (
                re.sub(r"\d+", "", original_authors).strip().split(",")
            )  ## Remove numbers
            authors = [author.replace("*", "") for author in authors]  ## Remove *
            authors = ", ".join(authors)
            authors = re.sub(r"\b(and)\b", "", authors)  ## Remove 'and word'
            authors = re.sub(r",\s+", ", ", authors)  ## Remove extra spaces after 'and'
            authors = authors.strip()
            self.title = title
            self.authors = authors

    def _retrieve_pubmed_id(self):
        """
        Retrieve PubMed ID from PDF.
        """
        query = f"({self.title}) AND ({self.authors})[Author]"
        Entrez.email = "mail@mail.com"
        handle = Entrez.esearch(
            db="pubmed", rettype="medline", retmode="text", term=query
        )
        record = Entrez.read(handle)
        id_paper = record["IdList"][0]
        handle = Entrez.efetch(
            db="pubmed", id=id_paper, rettype="medline", retmode="text"
        )
        records = Medline.read(handle)
        self.pubmed_id = records["PMID"]

    def full_text(self) -> str:
        """
        Extract full text parsed from PDF.

        Returns:
            str: Full text
        """
        with open(self.pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
