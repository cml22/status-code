import requests
from bs4 import BeautifulSoup
import csv

def get_status_code_and_canonical(url):
    """
    Récupère le code de statut HTTP et l'URL canonique d'une page.
    :param url: URL à vérifier
    :return: tuple (status_code, canonical_url)
    """
    try:
        response = requests.get(url, timeout=10)
        status_code = response.status_code

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            canonical_tag = soup.find("link", rel="canonical")
            canonical_url = canonical_tag['href'] if canonical_tag else "Non défini"
        else:
            canonical_url = "N/A"
        
        return status_code, canonical_url

    except requests.RequestException as e:
        return "Erreur", str(e)

def process_url_file(input_file, output_file):
    """
    Lit un fichier d'URLs, obtient les informations pour chaque URL, et enregistre les résultats.
    :param input_file: Chemin du fichier contenant les URLs (une URL par ligne)
    :param output_file: Chemin du fichier CSV de sortie avec les résultats
    """
    results = []

    with open(input_file, 'r') as file:
        urls = file.readlines()

    print("Traitement des URLs...")
    for url in urls:
        url = url.strip()  # Supprime les espaces inutiles
        if url:
            print(f"Vérification de : {url}")
            status_code, canonical = get_status_code_and_canonical(url)
            results.append([url, status_code, canonical])

    # Écrire les résultats dans un fichier CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Status Code", "Canonical URL"])
        writer.writerows(results)
    
    print(f"Résultats enregistrés dans {output_file}")

# Exemple d'utilisation
if __name__ == "__main__":
    input_file = "urls.txt"  # Remplacez par le chemin de votre fichier d'URLs
    output_file = "results.csv"  # Fichier de sortie
    process_url_file(input_file, output_file)
