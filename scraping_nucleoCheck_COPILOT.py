import requests
import re
from bs4 import BeautifulSoup
import time

# Función para realizar la búsqueda con SerpAPI
def search_google(query, api_key, num_results=100):
    search_url = "https://serpapi.com/search"
    params = {
        'q': query,
        'engine': 'google',
        'api_key': api_key,
        'num': num_results,
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code != 200:
        print(f"Error en la búsqueda: {response.status_code}")
        return []
    
    results = response.json().get("organic_results", [])
    urls = [result["link"] for result in results]
    return urls

# Función para extraer correos electrónicos de una página web
def extract_emails_from_html(html):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_regex, html)
    return set(emails)

# Función para obtener los emails de una lista de URLs
def get_emails_from_urls(urls):
    emails_found = set()
    
    for url in urls:
        try:
            print(f"Accediendo a {url}...")
            response = requests.get(url, timeout=10)
            time.sleep(0.5)  # Reducir el tiempo de espera
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                page_html = str(soup)
                emails = extract_emails_from_html(page_html)
                emails_found.update(emails)
            else:
                print(f"No se pudo acceder a {url}. Status code: {response.status_code}")
        
        except Exception as e:
            print(f"Error al acceder a {url}: {e}")
        
    return emails_found

# Función principal para buscar y extraer correos electrónicos
def main():
    query = "contact email gasista plomero Ensenada"
    api_key = "40f26a44ac94a42d338c50c2634481f872937b13355521c37b24ca55530ad05a"
    
    print("Realizando la búsqueda en Google...")
    urls = search_google(query, api_key)
    
    if not urls:
        print("No se encontraron resultados.")
        return
    
    print(f"Se encontraron {len(urls)} URLs. Extrayendo correos electrónicos...")
    emails = get_emails_from_urls(urls)
    
    print(f"Correos electrónicos encontrados: {len(emails)}")
    for email in emails:
        print(email)

if __name__ == "__main__":
    main()
