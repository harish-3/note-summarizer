"""
File Upload Module for Note Summarizer Application

This module handles the file upload functionality using Streamlit.
"""

import streamlit as st
import os
import tempfile
from typing import Optional, Tuple

def setup_upload_section() -> Optional[Tuple[str, str]]:
    """
    Set up the file upload section in the Streamlit app.
    
    Returns:
        Tuple containing the temporary file path and filename if a file is uploaded,
        None otherwise.
    """
    st.header("Upload Your Notes")
    st.write("Upload your academic notes in PDF or DOCX format to generate summaries and flashcards.")
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )
    
    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        
        st.write("File Information:")
        for key, value in file_details.items():
            st.write(f"- **{key}:** {value}")
        
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        st.success(f"File '{uploaded_file.name}' successfully uploaded!")
        
        # Return the path to the temporary file and the original filename
        return tmp_file_path, uploaded_file.name
    
    return None

def display_processing_status(status: str) -> None:
    """
    Display the current processing status.
    
    Args:
        status: Status message to display
    """
    status_container = st.empty()
    status_container.info(status)
    return status_container

def clear_status(status_container) -> None:
    """
    Clear the status message.
    
    Args:
        status_container: Container displaying the status message
    """
    status_container.empty()
