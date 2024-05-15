import spacy


def load_spacy_model() -> spacy.lang.en.English:
    """
    Load the spaCy model. Download it if not installed.

    Returns:
        spacy.lang.en.English: en_core_web_sm
    """
    if not spacy.util.is_package("en_core_web_sm"):
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
        print(type(nlp))
        return nlp
    else:
        nlp = spacy.load("en_core_web_sm")
        print(type(nlp))
        return nlp
