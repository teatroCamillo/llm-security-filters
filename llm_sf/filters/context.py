class Context:
    """
    Prosty kontener na dane, które mogą być współdzielone między filtrami.
    Na razie przechowuje tylko oryginalny tekst, ale można dodać tutaj logi,
    liczniki, statusy itp. 
    """
    def __init__(self, original_text: str):
        self.original_text = original_text
        # Możemy tu dodać np. dictionary na metadane z każdego filtra 
        self.metadata = {}
