import torch
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Smart Rebate Program",
    page_icon="🌾"
)

from document_processor import DocumentProcessor
from vector_store import VectorStore 
from rebate_program_assistant import RebateProgramAssistant 

# Initialize session state variables
if "saved_vector_embedding" not in st.session_state:
    st.session_state.saved_vector_embedding = False

# Sidebar file upload
with st.sidebar:
    st.title("🌾 Document Upload")
    uploaded_file = st.file_uploader("Upload rebate program PDF document.", type="pdf", key="file_upload")
    
    # Process the file when uploaded
    if uploaded_file is not None and not st.session_state.saved_vector_embedding:
        st.info(f"Processing your file: {uploaded_file.name}")
        
        # Initialize document processor and vector store
        document_processor = DocumentProcessor()
        vector_store = VectorStore()
        
        # Load PDF File 
        pdfDocument = document_processor.load_pdf_file(uploaded_file)
        
        # Create document chunks and save the embeddings
        chunks = document_processor.document_chunks(pdfDocument)
        vector_store.save_embedding(chunks=chunks)
        
        st.success(f"Processing Complete! 🎉 Your file {uploaded_file.name} is ready!")
        st.session_state.saved_vector_embedding = True

# Define the navigation structure
pages = {
    "Smart Rebate": [
        st.Page("rebate_program_assistant.py", title="Rebate Program Assistant"),
        st.Page("configure_rebate_program.py", title="Configure Rebate Program"),
    ],
    "Analytics": [
        st.Page("data_analytics.py", title="Know your data")
    ]
}

# navigation
pg = st.navigation(pages)
pg.run()
 
if __name__ == "__main__":
    torch.classes.__path__ = []