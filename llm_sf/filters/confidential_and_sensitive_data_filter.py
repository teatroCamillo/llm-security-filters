# confidential_and_sensitive_data_filter.py
import re
from dataprofiler import Profiler, ProfilerOptions
from dataprofiler.labelers.data_labelers import DataLabeler
from llm_sf.filters.base_filter import BaseFilter, FilterResult

class ConfidentialAndSensitiveDataFilter(BaseFilter):
    """
    A filter for detecting confidential or sensitive information in text.

    Detects data such as phone numbers, email addresses, and credit card numbers.
    Depending on configuration, the filter may either block such content or suggest
    sanitization by redacting the sensitive parts.
    """

    def __init__(self, block_on_detect: bool = True):
        """
        Initializes the filter with an optional blocking behavior.

        Args:
            block_on_detect (bool): If True, any detected sensitive data results in 'block'.
                                    If False, the filter returns 'sanitize' with redacted text.
        """
        self.block_on_detect = block_on_detect
        self.labeler = DataLabeler(labeler_type='unstructured')



    def run_filter(self, context):
        """
        Scans the input text for sensitive information using DataProfiler.

        If any sensitive data is detected, the result is either 'block' or 'sanitize',
        depending on the configuration. Sanitized output replaces sensitive spans
        with placeholder tags like [PII].

        Args:
            context: The Context object containing the current text to evaluate.

        Returns:
            FilterResult: A result indicating whether the text is allowed, needs sanitization, or should be blocked.
        """
        text = context.current_text

        try:
            prediction = self.labeler.predict(text)
            entities = prediction['entities']

            if entities:
                if self.block_on_detect:
                    return FilterResult(
                        verdict="block",
                        reason="Detected confidential/sensitive data. 'block_on_detect' is True."
                    )
                else:
                    # Redact sensitive spans in reverse order to preserve indices
                    redacted_text = text
                    for entity in sorted(entities, key=lambda x: x['start'], reverse=True):
                        label = entity['entity_type']
                        redacted_text = (
                            redacted_text[:entity['start']] +
                            f"[{label}]" +
                            redacted_text[entity['end']:]
                        )

                    return FilterResult(
                        verdict="sanitize",
                        reason="Detected confidential/sensitive data. Suggesting sanitization.",
                        metadata={"sanitized_text": redacted_text}
                    )

        except Exception as e:
            return FilterResult(
                verdict="allow",
                reason=f"DataProfiler labeler failed: {e}"
            )

        return FilterResult(
            verdict="allow",
            reason="No confidential/sensitive data detected."
        )