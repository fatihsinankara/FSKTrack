from .parsers import ArasKargoParser, YurticiKargoParser

def get_parser(carrier_name, tracking_url):
    """Kargo firmasına göre uygun parser'ı döndür"""
    if not tracking_url:
        raise ValueError("Tracking URL is missing")
        
    parsers = {
        "Aras Kargo": ArasKargoParser,
        "Yurtiçi Kargo": YurticiKargoParser,
        # Diğer kargo firmalarının parser'ları...
    }
    
    parser_class = parsers.get(carrier_name)
    if not parser_class:
        raise ValueError(f"No parser found for carrier: {carrier_name}")
        
    return parser_class(tracking_url)
