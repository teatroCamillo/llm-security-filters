from pathlib import Path
import csv

class Constants:
    
    # paths
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    RESOURCES_DIR = ROOT_DIR / "resources"
    PROFANITIES_CSV = RESOURCES_DIR / "profanities_en.csv"
    PROFANITY_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "profanity_sentences.csv"
    PROFANITY_SENTENCES_FULL_CSV = ROOT_DIR / "tests" / "resources" / "profanity_sentences_FULL.csv"
    CLEAN_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "clean_sentences.csv"
    MUTATED_WORDS_CSV = RESOURCES_DIR / "mutated_words.csv"
    CONFIDENTIAL_AND_SENSITIVE_CSV = ROOT_DIR / "tests" / "resources" / "conf_and_sensitive_phrases.csv"
    CLEAN_CONFIDENTIAL_AND_SENSITIVE_CSV = ROOT_DIR / "tests" / "resources" / "clean_conf_and_sensitive_phrases.csv"
    DISABLINGS_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "disablings.csv"
    # names
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    SANITIZED = "sanitized"

    OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

    @staticmethod
    def load_profanity_sentences():
        with open(Constants.PROFANITY_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            return [row[1] for row in reader if len(row) >= 1]
    
    @staticmethod
    def load_disablings():
        with open(Constants.DISABLINGS_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            return [row[0] for row in reader if len(row) >= 1]