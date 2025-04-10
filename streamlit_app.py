"""
Streamlit app entry point for cloud deployment - Simplified version

This file serves as the main entry point for the Note Summarizer application
when deployed to Streamlit Cloud.
"""

import streamlit as st
import os
import tempfile
from utils.file_parser import FileParser, is_supported_file
from models.llm_provider import LLMProviderManager
from models.enhanced_llm_processor import EnhancedLLMProcessor

# Set page configuration
st.set_page_config(
    page_title="Note Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'current_flashcard' not in st.session_state:
    st.session_state.current_flashcard = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'llm_configured' not in st.session_state:
    st.session_state.llm_configured = False

# Create sidebar
with st.sidebar:
    st.title("Note Summarizer")
    st.write("Transform your academic notes into concise summaries and flashcards.")
    
    st.markdown("---")
    st.markdown("### About")
    st.write("""
    This application helps students summarize their academic notes and create 
    flashcards for effective studying. Upload your notes in PDF or DOCX format 
    and let AI do the work for you!
    """)

# Main content
st.title("📚 Note Summarizer")

# LLM Configuration Section
st.header("Step 1: Configure LLM")

# Initialize provider manager
provider_manager = LLMProviderManager()

# Get all providers
providers = provider_manager.get_providers()
provider_names = provider_manager.get_provider_names()

# Provider selection
selected_provider_name = st.selectbox(
    "Select LLM Provider",
    options=provider_names,
    index=0,
    help="Choose the AI provider you want to use"
)

# Get provider ID from name
selected_provider_id = provider_manager.get_provider_id_by_name(selected_provider_name)

# Model selection for the selected provider
models = provider_manager.get_models_for_provider(selected_provider_id)
model_names = [model["name"] for model in models]

selected_model_name = st.selectbox(
    "Select Model",
    options=model_names,
    index=0,
    help="Choose the specific model to use"
)

# Get model ID from name
selected_model_id = provider_manager.get_model_id_by_name(selected_provider_id, selected_model_name)

# API key input if required
api_key = None
if provider_manager.requires_api_key(selected_provider_id):
    api_key = st.text_input(
        f"Enter your {selected_provider_name} API Key",
        type="password",
        help=f"Your API key for {selected_provider_name}"
    )

# Simple temperature slider
temperature = st.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.1,
    help="Higher values make output more random, lower values more deterministic"
)

# Save configuration button
if st.button("Save LLM Configuration", type="primary"):
    # Save to session state
    st.session_state.llm_provider_id = selected_provider_id
    st.session_state.llm_model_id = selected_model_id
    st.session_state.llm_api_key = api_key
    st.session_state.llm_temperature = temperature
    st.session_state.llm_max_tokens = 512  # Default value
    st.session_state.llm_configured = True
    
    st.success("✅ LLM configuration saved successfully!")

st.markdown("---")

# File Upload Section
st.header("Step 2: Upload & Process Notes")

# Check if LLM is configured
if not st.session_state.get("llm_configured", False):
    st.warning("⚠️ Please save your LLM configuration above before uploading files.")
else:
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )
    
    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        st.write("File Information:")
        for key, value in file_details.items():
            st.write(f"- **{key}:** {value}")
        
        # Process button
        if st.button("Process Notes", type="primary"):
            # Create a temporary file to store the uploaded content
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Show processing status
            with st.spinner("Processing your notes... This may take a moment."):
                try:
                    # Parse the file
                    parsed_data = FileParser.parse_file(tmp_file_path)
                    
                    # Initialize LLM processor from session state
                    llm_processor = EnhancedLLMProcessor(
                        provider_id=st.session_state.llm_provider_id,
                        model_id=st.session_state.llm_model_id,
                        api_key=st.session_state.llm_api_key,
                        temperature=st.session_state.llm_temperature,
                        max_tokens=st.session_state.llm_max_tokens
                    )
                    
                    # Process the notes
                    results = llm_processor.process_notes(parsed_data['text'])
                    
                    # Store results in session state
                    st.session_state.summary = results['summary']
                    st.session_state.flashcards = results['flashcards']
                    st.session_state.current_flashcard = 0
                    st.session_state.show_answer = False
                    
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)
                    
                    st.success("Processing complete! View results below.")
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)

st.markdown("---")

# Results Section
st.header("Step 3: View Results")

# Display summary if available
if st.session_state.summary:
    st.subheader("📝 Summary")
    st.write(st.session_state.summary)
    
    # Display flashcards if available
    if st.session_state.flashcards:
        st.markdown("---")
        st.subheader("🔍 Flashcards")
        
        # Flashcard navigation
        current_card = st.session_state.flashcards[st.session_state.current_flashcard]
        
        # Question
        st.markdown("### Question:")
        st.write(current_card["question"])
        
        # Toggle answer visibility
        if st.button("Show/Hide Answer"):
            st.session_state.show_answer = not st.session_state.show_answer
        
        # Answer (if visible)
        if st.session_state.show_answer:
            st.markdown("### Answer:")
            st.write(current_card["answer"])
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Card") and len(st.session_state.flashcards) > 1:
                st.session_state.current_flashcard = (st.session_state.current_flashcard - 1) % len(st.session_state.flashcards)
        
        with col2:
            if st.button("Next Card") and len(st.session_state.flashcards) > 1:
                st.session_state.current_flashcard = (st.session_state.current_flashcard + 1) % len(st.session_state.flashcards)
        
        # Display flashcard counter
        st.write(f"Card {st.session_state.current_flashcard + 1} of {len(st.session_state.flashcards)}")
else:
    st.info("No results to display yet. Please configure your LLM and process your notes first.")
