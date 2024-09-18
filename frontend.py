import streamlit as st
from main import search_and_download_pdfs
import os
def main():
    st.set_page_config(page_title="PDF Downloader", page_icon="📚")
    
    st.title("📚 PDF Downloader")
    st.write("Search and download PDFs on any topic!")

    query = st.text_input("Enter the topic to search for PDFs:")
    num_pdfs = st.number_input("Number of PDFs to download (max 10):", min_value=1, max_value=10, value=1)

    if st.button("Search and Download"):
        if query:
            with st.spinner("Searching and downloading PDFs..."):
                # Get the path to the Downloads folder
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                downloaded_pdfs = search_and_download_pdfs(query, num_pdfs, downloads_path)
            
            if downloaded_pdfs:
                st.success(f"Downloaded {len(downloaded_pdfs)} PDFs to your Downloads folder.")
                for pdf_path in downloaded_pdfs:
                    st.write(f"Downloaded: {os.path.basename(pdf_path)}")
        else:
            st.warning("Please enter a search query.")

    st.sidebar.header("About")
    st.sidebar.info("This app allows you to search for and download PDFs on any topic using the Google Custom Search API. PDFs are saved directly to your Downloads folder.")

if __name__ == "__main__":
    main()