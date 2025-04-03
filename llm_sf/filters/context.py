# context.py
class Context:
    """
    Prosty kontener na dane, które mogą być współdzielone między filtrami.
    """
    def __init__(self, original_text: str):
        # Tekst oryginalny (nigdy nie modyfikujemy, trzymamy do wglądu)
        self.original_text = original_text
        
        # Tekst, na którym faktycznie pracują filtry; 
        # w trybie serial może być wielokrotnie modyfikowany.
        self.current_text = original_text
        
        # Metadane – dowolne dodatkowe informacje
        self.metadata = {}
