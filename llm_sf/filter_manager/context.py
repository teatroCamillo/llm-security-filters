# context.py
class Context:

    def __init__(self, original_text: str):
        self.original_text = original_text
        self.current_text = original_text.lower()
        self.metadata = {}

    def __repr__(self):
        return (
            f"Context("
            f"original_text={self.original_text!r}, "
            f"current_text={self.current_text!r}, "
            f"metadata={self.metadata!r})"
        )