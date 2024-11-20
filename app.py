import requests
from bs4 import BeautifulSoup
import streamlit as st

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

def process_urls(url_list):
    """
    Traite une liste d'URLs et retourne leurs informations.
    :param url_list: Liste d'URLs
    :return: Liste des résultats contenant [URL, Status Code, Canonical URL]
    """
    results = []
    for url in url_list:
        url = url.strip()  # Supprime les espaces inutiles
        if url:
            status_code, canonical = get_status_code_and_canonical(url)
            results.append([url, status_code, canonical])
    return results

# Interface Streamlit
st.title("Vérification des Status Codes et URLs Canoniques")

# Entrée de l'utilisateur
urls_input = st.text_area(
    "Entrez les URLs (une par ligne) :", 
    placeholder="https://www.example.com\nhttps://www.google.com"
)

if st.button("Vérifier les URLs"):
    # Diviser les URLs en lignes et les traiter
    url_list = urls_input.strip().split("\n")
    
    if url_list:
        st.info("Traitement des URLs en cours...")
        results = process_urls(url_list)
        
        # Afficher les résultats dans un tableau
        st.success("Traitement terminé ! Voici les résultats :")
        st.table(results)
    else:
        st.warning("Veuillez entrer au moins une URL.")
