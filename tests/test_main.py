import pytest
from Main import fetch_page, parse_products

def test_fetch_page():
    #Testar om url returnerar rätt HTML innehåll
    url = "https://alphaspel.se/"
    html = fetch_page(url)
    assert isinstance(html, str) #kollar om angivet är en sträng, och inte int eller float i det här fallet
    assert "<html" in html.lower() # Kollar html innehåll

def test_parse_products():
    #Testar parsning för produkten
    sample_html = """
    <div class="content-bubble ribbon-wrapper">
        <div class="product-name">Test product</div>
        <div class="price text-success">100 kr</div>
    </div>
    """
    products = parse_products(sample_html)
    assert isinstance(products, list)      # Kollar om angivet produkter är en lista
    assert len(products) == 1    # Kollar om en produkt var hittad i test HTML
    assert products[0]["Product name"] == "Test product"   # Säkerställer att första produkten har korrekt namn
    assert products[0]["Price"] == "100 kr"   # säkerställer att första produkten har korrekt pris