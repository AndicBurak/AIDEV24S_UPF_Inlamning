from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import logging


# Avancerad databashantering, Automatisering eller multitrådning, API-integrationer,
# Enhetstestning och felsökning, SQL med python, Filhantering

logging.basicConfig(filename="app.log", level=logging.INFO, format='%(asctime)s - %(message)s')

def log_process(message):
    logging.info(message)
    print(message)

def fetch_page(url): #Hämta från hemsida
    log_process(f"Fetching data from {url}") # LOGGNING/Filhantering
    url =  "https://alphaspel.se/" # Hemsidan alphaspel används, HTML baserat. Skriv URL
    response = requests.get(url)
    response.raise_for_status() #kollar förfrågningen
    return response.text


def parse_products(html):    #Parsning med beautifulsoup & felsök
    soup = BeautifulSoup(html, "html.parser")
    product_blocks = soup.find_all("div", class_="content-bubble ribbon-wrapper")
                            
    if not product_blocks: 
        return []
    
    products = [] #lista för produkter

    for product in product_blocks:
        try:                                                                        
            #Produktnamn
            name = product.find("div", class_= "product-name").text.strip().replace('\n','') 
            #Produktpris
            price = product.find("div", class_="price text-success").text.strip()

            products.append({

                "Product name": name if name else "No name found", 
                "Price": price if price else "No price found"
            })
        except Exception as e:
            print(f"Error parsing product: {e}")
            continue
    return products


def save_to_csv(products, filename="alphaspel_products.csv"): #Konverterar lista till pandas dataframe & sparar
    df = pd.DataFrame(products)  
    df.to_csv(filename, index=False)
    log_process(f"Saved data to {filename}") # Filhantering/Loggning

def save_to_sqlite(products, db_name="alphaspel.db"):
    connection = sqlite3.connect(db_name) #Till databasen
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   price TEXT
        )           
                   
    """)

    for product in products:
        cursor.execute("INSERT INTO products (name, price) VALUES(?, ?)", 
                       (product["Product name"], product["Price"]))
    connection.commit()
    connection.close()
    log_process(f"Data saved to SQLite database: {db_name}")  # Filhantering/LOGGNING

if __name__ == "__main__":
    url = "https://alphaspel.se"
    html = fetch_page(url)
    products = parse_products(html)
    print(products)
    save_to_csv(products)
    save_to_sqlite(products)