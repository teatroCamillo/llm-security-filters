from pathlib import Path

class Constants:
    
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    RESOURCES_DIR = ROOT_DIR / "resources"
    PROFANITIES_CSV = RESOURCES_DIR / "profanities_en.csv"
    PROFANITY_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "profanity_sentences.csv"
    CLEAN_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "clean_sentences.csv"


    