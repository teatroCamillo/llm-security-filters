# confidential_and_sensitive_data_filter.py
import re
from dataprofiler import Profiler, ProfilerOptions
from dataprofiler.labelers.data_labelers import DataLabeler
from llm_sf.filters.base_filter import BaseFilter
from llm_sf.filter_manager.context import Context
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.utils.constants import Constants

class ConfidentialAndSensitiveDataFilter(BaseFilter):

    def __init__(
        self, 
        weight: float = 1.0
    ):
        super().__init__(weight=weight)
        self.labeler = DataLabeler(labeler_type='unstructured')

    def run_filter(self, context):

        text = context.current_text
        sensitive_labels = {
            'PAD',
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
            'PHONE_NUMBER',
            'SSN',
            'URL',
            'US_STATE',
            'FLOAT',
            'QUANTITY',
            'ORDINAL'
        }

        try:
            metadata = {"original_text": context.original_text, "risk_score": 0.0, "weight": self.weight} 
            prediction = self.labeler.predict([text], predict_options={"show_confidences": True})
            label_indices = prediction['pred'][0]
            
            label_map_reverse = {v: k for k, v in self.labeler.label_mapping.items()}
            label_names_seq = [label_map_reverse[int(idx)] for idx in label_indices]

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
                risk_score = self.compute_risk_score(entities)
                metadata = {"original_text": context.original_text, "risk_score": risk_score, "weight": self.weight}
                return FilterResult(
                    verdict=Constants.BLOCKED,
                    reason=f"Detected sensitive data: {[e['label'] for e in entities]}. Blocked due to policy.",
                    metadata=metadata
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

        SENSITIVITY_WEIGHTS = {
            'PAD': 0.0, # Padding Token
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
            'PHONE_NUMBER': 0.3,
            'SSN': 1.0, # Social Security Number
            'URL': 0.2,
            'US_STATE': 0.1,
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
