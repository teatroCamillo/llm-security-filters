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

    SENTIMENT_SENTENCES_FULL_CSV = ROOT_DIR / "tests" / "resources" / "sentiment_sentences.csv"

    CONFIDENTIAL_AND_SENSITIVE_CSV = ROOT_DIR / "tests" / "resources" / "conf_and_sensitive_sentences.csv"

    DISABLINGS_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "disablings.csv"

    MUTATED_WORDS_CSV = RESOURCES_DIR / "mutated_words.csv"

    JAILBREAK_PROMPTS_CSV = ROOT_DIR / "tests" / "resources" / "jailbreak_prompts.csv"
    JAILBREAK_PROMPTS_FULL_CSV = ROOT_DIR / "tests" / "resources" / "jailbreak_prompts_FULL.csv"
    
    # names
    ALLOWED = "allowed"
    BLOCKED = "blocked"

    OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

    @staticmethod
    def load_profanity_words():
        try:
            # MUTATED_WORDS_CSV also with row[1] - large set, problems with performance 
            with open(Constants.PROFANITIES_FULL_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0].strip() for row in reader if row]
        except Exception as e:
            print(f"Warning: Failed to load profanity words from CSV: {e}")
            return []

    @staticmethod
    def load_profanity_sentences():
        try:
            with open(Constants.PROFANITY_SENTENCES_FULL_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0] for row in reader if len(row) >= 1]
        except Exception as e:
            print(f"Warning: Failed to load profanity sentences: {e}")
            return []
    
    @staticmethod
    def load_clean_sentences():
        try:
            with open(Constants.CLEAN_SENTENCES_FULL_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0] for row in reader if len(row) >= 1]
        except Exception as e:
            print(f"Warning: Failed to load clean sentences: {e}")
            return []

    @staticmethod
    def load_disablings():
        try:
            with open(Constants.DISABLINGS_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0] for row in reader if len(row) >= 1]
        except Exception as e:
            print(f"Warning: Failed to load disabling sentences: {e}")
            return []

    @staticmethod
    def load_conf_and_sensitive_data():
        try:
            with open(Constants.CONFIDENTIAL_AND_SENSITIVE_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0] for row in reader if row]
        except Exception as e:
            print(f"Warning: Failed to load confidential and sensitive data: {e}")
            return []

    @staticmethod
    def load_sentiment_sentences():
        try:
            with open(Constants.SENTIMENT_SENTENCES_FULL_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0] for row in reader if len(row) >= 1]
        except Exception as e:
            print(f"Warning: Failed to load profanity sentences: {e}")
            return []

    @staticmethod
    def load_jailbreak_prompts():
        try:
            #JAILBREAK_PROMPTS_FULL_CSV or JAILBREAK_PROMPTS_CSV
            with open(Constants.JAILBREAK_PROMPTS_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0].strip() for row in reader if row]
        except Exception as e:
            print(f"Warning: Failed to load jailbreak prompts from CSV: {e}")
            return []