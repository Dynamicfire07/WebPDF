import requests
from urllib.parse import quote_plus
import streamlit as st
import os

API_KEY = "AIzaSyDaXEX0eIcjpqAdUWmIibpNMFbcSkFtbWk"
SEARCH_ENGINE_ID = "93d530360d9474515"

def search_pdfs(query, num_pdfs):
    search_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={quote_plus(query)}+filetype:pdf&num={min(num_pdfs, 10)}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        search_results = response.json()

        if 'items' not in search_results:
            return []

        return search_results['items'][:num_pdfs]

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during search: {e}")
        return []