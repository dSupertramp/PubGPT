# PubGPT 💉📄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PubGPT is a tool that can extract lots of relevant informations inside PubMed papers in a very simple way:

- Abstract
- Full text (when available)
- Genes
- Diseases
- Associations between genes and diseases (powered by LLMs and LangChain)
- MeSH terms
- Other terms

## Local PDF parsing architecture

![68747470733a2f2f62656e6e79636865756e672e6769746875622e696f2f696d616765732f61736b2d612d626f6f6b2d7175657374696f6e732d776974682d6c616e67636861696e2d6f70656e61692f41736b5f426f6f6b5f5175657374696f6e735f576f726b666c6f772e6a7067](https://github.com/dSupertramp/PubGPT/assets/48620457/64ef87f0-4953-42c0-a96f-fe93046f98b9)

## Install

To install everything, you need `poetry`.
First of all, create a virtual environment with the command `python3 -m venv venv_name` and activate it with `source venv_name\bin\activate`.

After that, you can install poetry with the command `pip install poetry` and then run `poetry install`.

## Run the app

To run the webapp, use the command:

```
cd pubgpt/
streamlit run app.py
```

## License

PubGPT is licensed under the MIT License. See the LICENSE file for more details.

### Todo

- [ ] Improve code
- [ ] Add sidebar where you can select the LLM and define credentials
- [ ] Add the extraction of more informations
- [ ] Create Python package
- [ ] Create documentation
- [ ] Add a fine-tuned model
- [ ] Improve web interface
- [x] Add docstrings
- [x] Add more LLMs for associations extraction
- [x] Add webapp
- [x] Add LangChain for PDFs
