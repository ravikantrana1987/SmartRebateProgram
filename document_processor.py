from langchain_community.document_loaders import PyPDFLoader
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
        self.temp_file_name = "temp_file.pdf"   
    
    
    def load_pdf_file(self, file):
        """ Load the PDF file using PyPDFLoader"""
        with open(self.temp_file_name,"wb") as f:
            f.write(file.getbuffer())
        
        loader = PyPDFLoader(self.temp_file_name)
        document = loader.load()
        os.remove(self.temp_file_name)
        return document

    def read_file(self, filePath):
        """ Read PDF file and load the content. """
        if filePath is not None:
            loader = PyPDFLoader(file_path=filePath)
            return loader
    
    def document_chunks(self, document):
        """Apply chunking to the PDF document using RecursiveCharacterTextSplitter."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        return text_splitter.split_documents(document)

