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

        # Labels we consider sensitive
        sensitive_labels = {
            'PHONE_NUMBER',
            'EMAIL_ADDRESS',
            'CREDIT_CARD',
            'SSN',
            'IPV4',
            'IPV6',
            'DRIVERS_LICENSE'
        }

        try:
            prediction = self.labeler.predict([text], predict_options={"show_confidences": True})
            label_indices = prediction['pred'][0]

            # Manually map label indices to names
            label_map_reverse = {v: k for k, v in self.labeler.label_mapping.items()}
            label_names_seq = [label_map_reverse[int(idx)] for idx in label_indices]

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

            if entities:
                if self.block_on_detect:
                    return FilterResult(
                        verdict=Constants.BLOCKED,
                        reason=f"Detected sensitive data: {[e['label'] for e in entities]}. Blocked due to policy."
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
                        metadata={"sanitized_text": redacted_text}
                    )

        except Exception as e:
            return FilterResult(
                verdict=Constants.ALLOWED,
                reason=f"DataProfiler labeler failed: {e}"
            )

        return FilterResult(
            verdict=Constants.ALLOWED,
            reason="No sensitive data detected."
        )

#old
    # def run_filter(self, context):
    #     """
    #     Scans the input text for sensitive information using DataProfiler.

    #     If any sensitive data is detected, the result is either 'block' or 'sanitize',
    #     depending on the configuration. Sanitized output replaces sensitive spans
    #     with placeholder tags like [PII].

    #     Args:
    #         context: The Context object containing the current text to evaluate.

    #     Returns:
    #         FilterResult: A result indicating whether the text is allowed, needs sanitization, or should be blocked.
    #     """
    #     text = context.current_text
    #     #label_map = self.labeler.label_mapping
    #     #print("lable_map: ", label_map)
    #     """
    #     lable_map:  
    #     {'PAD': 0, 'UNKNOWN': 1, 'ADDRESS': 2, 'BAN': 3, 'CREDIT_CARD': 4, 'DATE': 5, 
    #     'TIME': 6, 'DATETIME': 7, 'DRIVERS_LICENSE': 8, 'EMAIL_ADDRESS': 9, 'UUID': 10, 
    #     'HASH_OR_KEY': 11, 'IPV4': 12, 'IPV6': 13, 'MAC_ADDRESS': 14, 'PERSON': 15, 
    #     'PHONE_NUMBER': 16, 'SSN': 17, 'URL': 18, 'US_STATE': 19, 'INTEGER': 20, 'FLOAT': 21, 'QUANTITY': 22, 'ORDINAL': 23}
    #     """
    #     try:
    #         prediction = self.labeler.predict([text], predict_options={"show_confidences": True})
    #         entities = prediction
    #         print("entities: ", entities)

    #         if entities:
    #             if self.block_on_detect:
    #                 return FilterResult(
    #                     verdict="block",
    #                     reason="Detected confidential/sensitive data. 'block_on_detect' is True."
    #                 )
    #             else:
    #                 # Redact sensitive spans in reverse order to preserve indices
    #                 redacted_text = text
    #                 for entity in sorted(entities, key=lambda x: x['start'], reverse=True):
    #                     label = entity['entity_type']
    #                     redacted_text = (
    #                         redacted_text[:entity['start']] +
    #                         f"[{label}]" +
    #                         redacted_text[entity['end']:]
    #                     )

    #                 return FilterResult(
    #                     verdict="sanitized",
    #                     reason="Detected confidential/sensitive data. Suggesting sanitization.",
    #                     metadata={"sanitized_text": redacted_text}
    #                 )

    #     except Exception as e:
    #         return FilterResult(
    #             verdict="allow",
    #             reason=f"DataProfiler labeler failed: {e}"
    #         )

    #     return FilterResult(
    #         verdict="allow",
    #         reason="No confidential/sensitive data detected."
    #     )

if __name__ == "__main__":
    # Define a simple context class with a current_text attribute
    

    # Example text containing sensitive data
    sample_text = "Contact me at john.doe@example.com or call 555-123-4567. My SSN is 123-45-6789."

    # Create context with the sample text
    context = Context(sample_text)

    # Instantiate the filter (block_on_detect=True to block on detection)
    filter_instance = ConfidentialAndSensitiveDataFilter()

    # Run the filter
    result = filter_instance.run_filter(context)

    # Print the result
    print(f"Verdict: {result.verdict}")
    print(f"Reason: {result.reason}")
    if hasattr(result, "metadata") and result.metadata:
        print(f"Metadata: {result.metadata}")