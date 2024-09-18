import requests
from urllib.parse import quote_plus
import streamlit as st
import os

API_KEY = "AIzaSyDaXEX0eIcjpqAdUWmIibpNMFbcSkFtbWk"
SEARCH_ENGINE_ID = "93d530360d9474515"

def search_and_download_pdfs(query, num_pdfs, downloads_path):
    search_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={quote_plus(query)}+filetype:pdf&num={min(num_pdfs, 10)}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        search_results = response.json()

        if 'items' not in search_results:
            st.error("No PDFs found for the given topic.")
            return []

        downloaded_pdfs = []
        for i, item in enumerate(search_results['items'][:num_pdfs], 1):
            pdf_url = item['link']
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()

            filename = f"{query.replace(' ', '_')}_{i}.pdf"
            filepath = os.path.join(downloads_path, filename)
            with open(filepath, 'wb') as f:
                f.write(pdf_response.content)
            
            downloaded_pdfs.append(filepath)
            st.success(f"Downloaded: {filename}")

        return downloaded_pdfs

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []