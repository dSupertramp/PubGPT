# AItrika

![AItrika](images/logo.png)

[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub forks](https://img.shields.io/github/forks/dSupertramp/AItrika)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/dSupertramp/AItrika/main)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/dSupertramp/AItrika/main)

![Static Badge](https://img.shields.io/badge/medical-content?logo=syringe&logoColor=cyan&color=cyan)

Enhance your knowledge in medical research.

AItrika (formerly **PubGPT**) is a tool that can extract lots of relevant informations inside medical papers in an easy way:

- Abstract
- Full text (when available)
- Genes
- Diseases
- Mutations
- Associations between genes and diseases
- MeSH terms
- Other terms
- Results
- Bibliography

And so on!

## 🚀 Run the demo app

You can try AItrika with the Streamlit app by running:

```
streamlit run app.py
```

Or you can use it a script by running:

```
python main.py
```

## 📦 Install

To install everything, you need `poetry`.

First of all, create a virtual environment with the command `python3 -m venv venv_name` and activate it with `source venv_name\bin\activate`.

After that, you can install poetry with the command `pip install poetry` and then run `poetry install`.

## 🔑 Set API Keys

In order to set API keys, insert your keys into the `env.example` file and rename it to `.env`.

## 🔍 Usage

You can easily get informations of a paper by passing a PubMed ID:

```python
from aitrika.engine.aitrika import OnlineAItrika
aitrika_engine = OnlineAItrika(pubmed_id=pubmed_id)
title = aitrika_engine.get_title()
print(title)
```

Or you can parse a local pdf:

```python
from aitrika.engine.aitrika import LocalAItrika
aitrika_engine = LocalAItrika(pdf_path = pdf_path)
title = aitrika_engine.get_title()
print(title)
```

```
Breast cancer genes: beyond BRCA1 and BRCA2.
```

You can get other informations, like the associations between genes and diseases:

```python
associations = aitrika_engine.get_associations()
```

```
[
  {
    "gene": "BRIP1",
    "disease": "Breast Neoplasms"
  },
  {
    "gene": "PTEN",
    "disease": "Breast Neoplasms"
  },
  {
    "gene": "CHEK2",
    "disease": "Breast Neoplasms"
  },
]
...
```

Or you can get a nice formatted DataFrame:

```python
associations = aitrika_engine.associations(dataframe = True)
```

```
      gene                          disease
0    BRIP1                 Breast Neoplasms
1     PTEN                 Breast Neoplasms
2    CHEK2                 Breast Neoplasms
...
```

With the power of RAG, you can query your document:

```python
## Prepare the documents
documents = generate_documents(content=abstract)

## Set the LLM
llm = GroqLLM(documents=documents, api_key=os.getenv("GROQ_API_KEY"))

## Query your document
query = "Is BRCA1 associated with breast cancer?"
print(llm.query(query=query))
```

```
The provided text suggests that BRCA1 is associated with breast cancer, as it is listed among the high-penetrance genes identified in family linkage studies as responsible for inherited syndromes of breast cancer.
```

Or you can extract other informations:

```python
results = engine.extract_results(llm=llm)
print(results)
```

```
** RESULTS **

- High-penetrance genes - BRCA1, BRCA2, PTEN, TP53 - responsible for inherited syndromes
- Moderate-penetrance genes - CHEK2, ATM, BRIP1, PALB2, RAD51C - associated with moderate BC risk
- Low-penetrance alleles - common alleles - associated with slightly increased or decreased risk of BC
- Current clinical practice - high-penetrance genes - widely used
- Future prospect - all familial breast cancer genes - to be included in genetic test
- Research need - clinical management - of moderate and low-risk variants
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=dSupertramp/AItrika&type=Date)](https://star-history.com/#dSupertramp/AItrika&Date)

## License

AItrika is licensed under the Apache 2.0 License. See the LICENSE file for more details.

## TODO

- [ ] Add docstrings
- [ ] Create Python package

```

```
