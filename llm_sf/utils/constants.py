from pathlib import Path
import csv

class Constants:
    
    # paths
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    RESOURCES_DIR = ROOT_DIR / "resources"

    PROFANITIES_CSV = RESOURCES_DIR / "profanities_en.csv"
    PROFANITIES_FULL_CSV = RESOURCES_DIR / "profanities_en_FULL.csv"

    PROFANITY_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "profanity_sentences.csv"
    PROFANITY_SENTENCES_FULL_CSV = ROOT_DIR / "tests" / "resources" / "profanity_sentences_FULL.csv"

    CLEAN_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "clean_sentences.csv"
    CLEAN_SENTENCES_FULL_CSV = ROOT_DIR / "tests" / "resources" / "clean_sentences_FULL.csv"

    CONFIDENTIAL_AND_SENSITIVE_CSV = ROOT_DIR / "tests" / "resources" / "conf_and_sensitive_sentences.csv"

    DISABLINGS_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "disablings.csv"

    MUTATED_WORDS_CSV = RESOURCES_DIR / "mutated_words.csv"
    
    # names
    ALLOWED = "allowed"
    BLOCKED = "blocked"

    OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

    @staticmethod
    def load_profanity_words(profanity):
        try:
            # MUTATED_WORDS_CSV also with row[1] - large set, problems with performance 
            with open(Constants.PROFANITIES_FULL_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                csv_badwords = [row[0].strip() for row in reader if row]
                profanity.add_censor_words(csv_badwords)
        except Exception as e:
            print(f"Warning: Failed to load profanity words from CSV: {e}")

    @staticmethod
    def load_profanity_sentences():
        with open(Constants.PROFANITY_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            return [row[1] for row in reader if len(row) >= 1]
    
    @staticmethod
    def load_clean_sentences():
        with open(Constants.CLEAN_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            return [row[0] for row in reader if len(row) >= 1]

    @staticmethod
    def load_disablings():
        with open(Constants.DISABLINGS_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            return [row[0] for row in reader if len(row) >= 1]

    @staticmethod
    def load_conf_and_sensitive_data():
        with open(Constants.CONFIDENTIAL_AND_SENSITIVE_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            return [row[0] for row in reader]