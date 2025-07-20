# confidential_and_sensitive_data_filter.py
import re
from dataprofiler import Profiler, ProfilerOptions
from dataprofiler.labelers.data_labelers import DataLabeler
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.filters.context import Context
from llm_sf.utils.constants import Constants

class ConfidentialAndSensitiveDataFilter(BaseFilter):
    """
    A filter for detecting confidential or sensitive information in text.

    Detects data such as phone numbers, email addresses, and credit card numbers.
    Depending on configuration, the filter may either block such content or suggest
    sanitization by redacting the sensitive parts.
    """

    def __init__(
        self,
        block_on_detect: bool = True, 
        weight: float = 1.0
    ):
        super().__init__(block_on_detect=block_on_detect, weight=weight)
        """
        Initializes the filter with an optional blocking behavior.

        Args:
            block_on_detect (bool): If True, any detected sensitive data results in 'block'.
                                    If False, the filter returns 'sanitize' with redacted text.
        """
        self.labeler = DataLabeler(labeler_type='unstructured')

    def run_filter(self, context):
        """
        Scans the input text for sensitive information using DataProfiler.

        Returns a FilterResult indicating whether the text should be allowed, sanitized, or blocked,
        based on detection of high-risk PII.
        """
        text = context.current_text
    #     lable_map:  
    #     {'PAD': 0, 'UNKNOWN': 1, 'ADDRESS': 2, 'BAN': 3, 'CREDIT_CARD': 4, 'DATE': 5, 
    #     'TIME': 6, 'DATETIME': 7, 'DRIVERS_LICENSE': 8, 'EMAIL_ADDRESS': 9, 'UUID': 10, 
    #     'HASH_OR_KEY': 11, 'IPV4': 12, 'IPV6': 13, 'MAC_ADDRESS': 14, 'PERSON': 15, 
    #     'PHONE_NUMBER': 16, 'SSN': 17, 'URL': 18, 'US_STATE': 19, 'INTEGER': 20, 'FLOAT': 21, 'QUANTITY': 22, 'ORDINAL': 23}
    #     """
        # Labels we consider sensitive
        sensitive_labels = {
            'PAD',
            #'UNKNOWN',
            'ADDRESS',
            'BAN',
            'CREDIT_CARD',
            'DATE',
            'TIME',
            'DATETIME',
            'DRIVERS_LICENSE',
            'EMAIL_ADDRESS',
            'UUID',
            'HASH_OR_KEY',
            'IPV4',
            'IPV6',
            'MAC_ADDRESS',
            #'PERSON',
            'PHONE_NUMBER',
            'SSN',
            'URL',
            'US_STATE',
            #'INTEGER',
            'FLOAT',
            'QUANTITY',
            'ORDINAL'
        }

        try:
            metadata = {"risk_score": 0.0, "weight": self.weight} 
            prediction = self.labeler.predict([text], predict_options={"show_confidences": True})
            label_indices = prediction['pred'][0]
            
            # Manually map label indices to names
            label_map_reverse = {v: k for k, v in self.labeler.label_mapping.items()}
            label_names_seq = [label_map_reverse[int(idx)] for idx in label_indices]
            print("label names: ", label_names_seq)

            # Extract spans of sensitive entities
            entities = []
            current = None
            for i, label in enumerate(label_names_seq):
                if label in sensitive_labels:
                    if current and current["label"] == label:
                        current["end"] = i + 1
                    else:
                        if current:
                            entities.append(current)
                        current = {"label": label, "start": i, "end": i + 1}
                else:
                    if current:
                        entities.append(current)
                        current = None
            if current:
                entities.append(current)
                
            print("entities: ", entities)
            print("IF before entities")
            if entities:
                risk_score = self.compute_risk_score(entities)
                metadata = {"risk_score": risk_score, "weight": self.weight}
                print("risk_score: ", risk_score)
                print("weight: ", self.weight)

                if self.block_on_detect:
                    return FilterResult(
                        verdict=Constants.BLOCKED,
                        reason=f"Detected sensitive data: {[e['label'] for e in entities]}. Blocked due to policy.",
                        metadata=metadata
                    )
                else:
                    # Redact in reverse order to preserve positions
                    redacted_text = text
                    for entity in sorted(entities, key=lambda x: x["start"], reverse=True):
                        redacted_text = (
                            redacted_text[:entity["start"]] +
                            f"[{entity['label']}]" +
                            redacted_text[entity["end"]:]
                        )
                    return FilterResult(
                        verdict="sanitized",
                        reason="Sensitive data detected and redacted.",
                        metadata={"sanitized_text": redacted_text, "risk_score": risk_score, "weight": self.weight}
                    )
                
            return FilterResult(
                    verdict=Constants.ALLOWED,
                    reason=f"No threat detected.",
                    metadata=metadata
                )

        except Exception as e:
            return FilterResult(
                verdict=Constants.ALLOWED,
                reason=f"DataProfiler labeler failed: {e}",
                metadata=metadata
            )

    def compute_risk_score(self, entities: list) -> float:
        """
        Computes a normalized risk score based on the detected sensitive entities.

        Args:
            entities (list): A list of dictionaries with 'label' keys for sensitive matches.

        Returns:
            float: A normalized risk score in the range [0.0, 1.0].
        """
        SENSITIVITY_WEIGHTS = {
            'PAD': 0.0, # Padding Token
            #'UNKNOWN': 0.1,
            'ADDRESS': 0.4,
            'BAN': 0.5,  # Bank Account Number
            'CREDIT_CARD': 0.9,
            'DATE': 0.2,
            'TIME': 0.1,
            'DATETIME': 0.2,
            'DRIVERS_LICENSE': 0.8,
            'EMAIL_ADDRESS': 0.2,
            'UUID': 0.3,
            'HASH_OR_KEY': 0.6,
            'IPV4': 0.4,
            'IPV6': 0.4,
            'MAC_ADDRESS': 0.3,
            #'PERSON': 0.5,
            'PHONE_NUMBER': 0.3,
            'SSN': 1.0, # Social Security Number
            'URL': 0.2,
            'US_STATE': 0.1,
            #'INTEGER': 0.1,
            'FLOAT': 0.1,
            'QUANTITY': 0.1,
            'ORDINAL': 0.0
        }

        MAX_TOTAL_SEVERITY = 3.0  # Tune this based on how strict you want it to be

        total_severity = sum(
            SENSITIVITY_WEIGHTS.get(entity["label"], 0.1)
            for entity in entities
        )

        risk_score = round(min(total_severity / MAX_TOTAL_SEVERITY, 1.0), 2)

        print("entities:", [e["label"] for e in entities])
        print("total_severity:", total_severity)
        print("risk_score:", risk_score)

        return risk_score

# if __name__ == "__main__":
#     sample_text = "Contact me at john.doe@example.com or call 555-123-4567. My SSN is 123-45-6789."

#     # Create context with the sample text
#     context = Context(sample_text)

#     # Instantiate the filter (block_on_detect=True to block on detection)
#     filter_instance = ConfidentialAndSensitiveDataFilter()

#     # Run the filter
#     result = filter_instance.run_filter(context)

#     # Print the result
#     print(f"Verdict: {result.verdict}")
#     print(f"Reason: {result.reason}")
#     if hasattr(result, "metadata") and result.metadata:
#         print(f"Metadata: {result.metadata}")