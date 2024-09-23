import streamlit as st
import requests
from urllib.parse import quote_plus
import io
import os

# Load environment variables

# Get API key and Search Engine ID from environment variables
API_KEY = "AIzaSyDaXEX0eIcjpqAdUWmIibpNMFbcSkFtbWk"
SEARCH_ENGINE_ID = "93d530360d9474515"

# Set page config
st.set_page_config(page_title="PDF Downloader", page_icon="📚", layout="wide")

# Custom CSS


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
        st.error(f"An error occurred during search: {e}")
        return []

st.title("📚 PDF Downloader")
st.write("Search and download PDFs on any topic!")

# Sidebar
st.sidebar.header("About")
st.sidebar.info("This app allows you to search for and download PDFs on any topic using the Google Custom Search API.")

# Main content
col1, col2 = st.columns([2,1])

with col1:
    with st.form(key='search_form'):
        query = st.text_input("Enter the topic to search for PDFs:")
        num_pdfs = st.slider("Number of PDFs to search", 1, 10, 5)
        submit_button = st.form_submit_button(label='Search PDFs')

if submit_button:
    if query:
        with st.spinner("Searching for PDFs..."):
            pdf_results = search_pdfs(query, num_pdfs)
        
        if pdf_results:
            st.success(f"Found {len(pdf_results)} PDFs.")
            for i, pdf_info in enumerate(pdf_results, 1):
                title = pdf_info['title']
                url = pdf_info['link']
                snippet = pdf_info.get('snippet', 'No description available.')
                
                st.markdown(f"""
                <div class="pdf-result">
                    <h3>{i}. {title}</h3>
                    <p>{snippet}</p>
                    <a href="{url}" target="_blank">View PDF</a>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a download button for each PDF
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    pdf_content = response.content
                    
                    st.download_button(
                        label=f"Download PDF",
                        data=pdf_content,
                        file_name=f"{title}.pdf",
                        mime="application/pdf",
                        key=f"download_{i}"
                    )
                except requests.exceptions.RequestException as e:
                    st.error(f"Error downloading PDF: {e}")
        else:
            st.error("No PDFs were found for the given query.")
    else:
        st.warning("Please enter a search query.")

with col2:
    st.subheader("Recent Searches")
    # You can implement a feature to show recent searches here
    # For now, we'll just show a placeholder
    st.write("1. Machine Learning")
    st.write("2. Python Programming")
    st.write("3. Data Science")

# Footer
st.markdown("---")
st.markdown("Created by Shaurya Jain")