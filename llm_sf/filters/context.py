# context.py
class Context:
    """
    A simple data container shared across filters during content processing.

    Stores both the original and working versions of the text, along with metadata,
    allowing filters to access and modify input consistently across serial or parallel flows.
    """

    def __init__(self, original_text: str):
        """
        Initializes a Context object with the provided input text.

        The original text is preserved for reference, while a mutable copy is
        used by filters for transformations. Arbitrary metadata can also be attached.

        Args:
            original_text (str): The initial, unmodified text input to be processed.
        """
        self.original_text = original_text
        self.current_text = original_text
        self.metadata = {}

