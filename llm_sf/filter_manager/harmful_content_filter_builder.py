from filters.hrmful_content_filter import HarmfulContentFilter 

class HarmfulContentFilterBuilder:
    def __init__(self):
        self.mechanisms = []
        self.config = {
            "slur_keywords": None,
            "mild_profanities": None,
            "profanity_replacement": "[censored]",
            "sentiment_threshold": -0.7
        }
        self.engine = HarmfulContentFilter()

    def check_severe_slurs(self, keywords=None):
        self.config["slur_keywords"] = keywords
        self.mechanisms.append("check_severe_slurs")
        return self

    def check_mild_profanity(self, profanities=None, replacement="[censored]"):
        self.config["mild_profanities"] = profanities
        self.config["profanity_replacement"] = replacement
        self.mechanisms.append("check_mild_profanity")
        return self

    def check_sentiment(self, threshold=-0.7):
        self.config["sentiment_threshold"] = threshold
        self.mechanisms.append("check_sentiment")
        return self

    def execute(self, text):
        current_text = text
        final_verdict = "allow"
        reasons = []

        for mech in self.mechanisms:
            if mech == "check_severe_slurs":
                result = self.engine.check_severe_slurs(current_text, self.config["slur_keywords"])
            elif mech == "check_mild_profanity":
                result = self.engine.check_mild_profanity(current_text, self.config["mild_profanities"], self.config["profanity_replacement"])
            elif mech == "check_sentiment":
                result = self.engine.check_sentiment(current_text, self.config["sentiment_threshold"])
            else:
                continue

            verdict = result["verdict"]
            if verdict == "block":
                return result
            elif verdict == "sanitize":
                final_verdict = "sanitize"
                current_text = result["final_text"]
                reasons.append(result["reason"])

        return {
            "verdict": final_verdict,
            "reason": "; ".join(reasons) if reasons else None,
            "final_text": current_text
        }
