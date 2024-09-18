import streamlit as st
import requests
from urllib.parse import quote_plus
import io
from main import search_pdfs  # We'll modify this function in main.py

def main():
    st.set_page_config(page_title="PDF Downloader", page_icon="📚")
    
    st.title("📚 PDF Downloader")
    st.write("Search and download PDFs on any topic!")

    query = st.text_input("Enter the topic to search for PDFs:")
    num_pdfs = st.number_input("Number of PDFs to search (max 10):", min_value=1, max_value=10, value=1)

    if st.button("Search PDFs"):
        if query:
            with st.spinner("Searching for PDFs..."):
                pdf_results = search_pdfs(query, num_pdfs)
            
            if pdf_results:
                st.success(f"Found {len(pdf_results)} PDFs.")
                for i, pdf_info in enumerate(pdf_results, 1):
                    title = pdf_info['title']
                    url = pdf_info['link']
                    
                    st.write(f"{i}. {title}")
                    
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

    st.sidebar.header("About")
    st.sidebar.info("This app allows you to search for and download PDFs on any topic using the Google Custom Search API.")

if __name__ == "__main__":
    main()