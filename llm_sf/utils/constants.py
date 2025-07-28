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
    SENTIMENT_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" /"sentiment_sentences_PART.csv"

    CONFIDENTIAL_AND_SENSITIVE_CSV = ROOT_DIR / "tests" / "resources" / "conf_and_sensitive_sentences.csv"

    DISABLINGS_SENTENCES_CSV = ROOT_DIR / "tests" / "resources" / "disablings.csv"

    MUTATED_WORDS_CSV = RESOURCES_DIR / "mutated_words.csv"

    JAILBREAK_PROMPTS_CSV = ROOT_DIR / "tests" / "resources" / "jailbreak_prompts.csv"
    JAILBREAK_PROMPTS_FULL_CSV = ROOT_DIR / "tests" / "resources" / "jailbreak_prompts_FULL.csv"

    JAILBREAK_PATTERNS_CSV = RESOURCES_DIR / "jailbreak_patterns.csv"

    HIGH_RISK_WORDS_CSV = RESOURCES_DIR / "high_risk_words.csv"
    
    # names
    ALLOWED = "allowed"
    BLOCKED = "blocked"

    OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

    @staticmethod
    def load_csv(source):
        try:
            with open(source, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                return [row[0].strip() for row in reader if row]
        except Exception as e:
            print(f"Warning: Failed to load data from CSV: {e}")
            return []
            