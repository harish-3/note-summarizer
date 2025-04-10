"""
Updated main application file for Note Summarizer with enhanced LLM configuration

This module implements the Streamlit user interface with theme switching functionality
and flexible LLM provider selection.
"""

import streamlit as st
import os
import tempfile
from utils.file_upload import setup_upload_section, display_processing_status, clear_status
from utils.file_parser import FileParser, is_supported_file
from utils.llm_config import setup_llm_configuration, display_llm_status, save_llm_config_to_session_state, get_llm_config_from_session_state, initialize_llm_processor
from models.enhanced_llm_processor import EnhancedLLMProcessor

# Set page configuration
st.set_page_config(
    page_title="Note Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Upload"

def toggle_theme():
    """Toggle between light and dark theme."""
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

def next_flashcard():
    """Move to the next flashcard."""
    if st.session_state.flashcards:
        st.session_state.current_flashcard = (st.session_state.current_flashcard + 1) % len(st.session_state.flashcards)
        st.session_state.show_answer = False

def prev_flashcard():
    """Move to the previous flashcard."""
    if st.session_state.flashcards:
        st.session_state.current_flashcard = (st.session_state.current_flashcard - 1) % len(st.session_state.flashcards)
        st.session_state.show_answer = False

def toggle_answer():
    """Toggle showing the answer for the current flashcard."""
    st.session_state.show_answer = not st.session_state.show_answer

def set_active_tab(tab_name):
    """Set the active tab."""
    st.session_state.active_tab = tab_name

def apply_theme():
    """Apply the current theme to the application."""
    if st.session_state.theme == 'dark':
        # Dark theme CSS
        st.markdown("""
        <style>
        .main {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #333333;
            color: white;
        }
        .stMarkdown {
            color: #FFFFFF;
        }
        .css-145kmo2 {
            color: #FFFFFF;
        }
        .css-1d391kg {
            background-color: #333333;
        }
        .flashcard {
            background-color: #333333;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        .summary-box {
            background-color: #333333;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        .tab-button {
            background-color: #333333;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
        }
        .tab-button.active {
            background-color: #4CAF50;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme CSS
        st.markdown("""
        <style>
        .main {
            background-color: #FFFFFF;
            color: #000000;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #F0F2F6;
            color: black;
        }
        .stMarkdown {
            color: #000000;
        }
        .flashcard {
            background-color: #F0F2F6;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .summary-box {
            background-color: #F0F2F6;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .tab-button {
            background-color: #F0F2F6;
            color: black;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
        }
        .tab-button.active {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit application."""
    # Apply the current theme
    apply_theme()
    
    # Create sidebar
    with st.sidebar:
        st.title("Note Summarizer")
        st.write("Transform your academic notes into concise summaries and flashcards.")
        
        # Theme toggle
        theme_label = "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"
        st.button(theme_label, on_click=toggle_theme)
        
        # Display current LLM status if configured
        provider_id, model_id, _, _, _, configured = get_llm_config_from_session_state()
        if configured:
            display_llm_status(provider_id, model_id)
        
        st.markdown("---")
        st.markdown("### About")
        st.write("""
        This application helps students summarize their academic notes and create 
        flashcards for effective studying. Upload your notes in PDF or DOCX format 
        and let AI do the work for you!
        """)
        
        st.markdown("---")
        st.markdown("### How to Use")
        st.write("""
        1. Configure your preferred LLM provider
        2. Upload your notes file (PDF or DOCX)
        3. Wait for the processing to complete
        4. View your summary and flashcards
        5. Use the flashcard navigation to study
        """)
    
    # Main content
    st.title("📚 Note Summarizer")
    
    # Create tabs using buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        upload_class = "active" if st.session_state.active_tab == "Upload" else ""
        st.markdown(f'<button class="tab-button {upload_class}" onclick="document.querySelector(\'[data-testid="stFormSubmitButton"]\').click()">Upload & Process</button>', unsafe_allow_html=True)
        if st.button("Upload & Process", key="tab_upload", help="Upload and process notes"):
            set_active_tab("Upload")
            st.experimental_rerun()
    
    with col2:
        config_class = "active" if st.session_state.active_tab == "Config" else ""
        st.markdown(f'<button class="tab-button {config_class}" onclick="document.querySelector(\'[data-testid="stFormSubmitButton"]\').click()">LLM Configuration</button>', unsafe_allow_html=True)
        if st.button("LLM Configuration", key="tab_config", help="Configure LLM settings"):
            set_active_tab("Config")
            st.experimental_rerun()
    
    with col3:
        results_class = "active" if st.session_state.active_tab == "Results" else ""
        st.markdown(f'<button class="tab-button {results_class}" onclick="document.querySelector(\'[data-testid="stFormSubmitButton"]\').click()">Results</button>', unsafe_allow_html=True)
        if st.button("Results", key="tab_results", help="View processing results"):
            set_active_tab("Results")
            st.experimental_rerun()
    
    st.markdown("---")
    
    # Display content based on active tab
    if st.session_state.active_tab == "Upload":
        display_upload_tab()
    elif st.session_state.active_tab == "Config":
        display_config_tab()
    elif st.session_state.active_tab == "Results":
        display_results_tab()

def display_upload_tab():
    """Display the upload and processing tab."""
    st.header("📤 Upload & Process Notes")
    
    # Check if LLM is configured
    _, _, _, _, _, configured = get_llm_config_from_session_state()
    
    if not configured:
        st.warning("⚠️ Please configure your LLM settings in the 'LLM Configuration' tab before uploading files.")
        if st.button("Go to LLM Configuration"):
            set_active_tab("Config")
            st.experimental_rerun()
        return
    
    # File upload section
    upload_result = setup_upload_section()
    
    if upload_result:
        tmp_file_path, original_filename = upload_result
        
        # Process button
        if st.button("Process Notes"):
            # Display processing status
            status_container = display_processing_status("Processing your notes... This may take a moment.")
            
            try:
                # Parse the file
                parsed_data = FileParser.parse_file(tmp_file_path)
                
                # Initialize LLM processor from session state
                llm_processor = initialize_llm_processor()
                
                if not llm_processor:
                    st.error("Failed to initialize LLM processor. Please check your configuration.")
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)
                    return
                
                # Process the notes
                results = llm_processor.process_notes(parsed_data['text'])
                
                # Store results in session state
                st.session_state.summary = results['summary']
                st.session_state.flashcards = results['flashcards']
                st.session_state.current_flashcard = 0
                st.session_state.show_answer = False
                
                # Clear the status message
                clear_status(status_container)
                
                # Clean up the temporary file
                os.unlink(tmp_file_path)
                
                # Switch to results tab
                set_active_tab("Results")
                
                # Force a rerun to display the results
                st.experimental_rerun()
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                # Clean up the temporary file
                os.unlink(tmp_file_path)

def display_config_tab():
    """Display the LLM configuration tab."""
    # LLM configuration section
    provider_id, model_id, api_key, temperature, max_tokens = setup_llm_configuration()
    
    # Save configuration button
    if st.button("Save Configuration"):
        save_llm_config_to_session_state(
            provider_id=provider_id,
            model_id=model_id,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        st.success("✅ LLM configuration saved successfully!")
        
        # Test the configuration
        try:
            llm_processor = EnhancedLLMProcessor(
                provider_id=provider_id,
                model_id=model_id,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens
            )
            st.success("✅ LLM connection test successful!")
            
            # Offer to go to upload tab
            if st.button("Go to Upload & Process"):
                set_active_tab("Upload")
                st.experimental_rerun()
                
        except Exception as e:
            st.error(f"❌ LLM connection test failed: {str(e)}")
            st.session_state.llm_configured = False

def display_results_tab():
    """Display the results tab with summary and flashcards."""
    if not st.session_state.summary and not st.session_state.flashcards:
        st.info("No results to display yet. Please upload and process your notes first.")
        if st.button("Go to Upload & Process"):
            set_active_tab("Upload")
            st.experimental_rerun()
        return
    
    # Display summary if available
    if st.session_state.summary:
        st.header("📝 Summary")
        st.markdown(f'<div class="summary-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
    
    # Display flashcards if available
    if st.session_state.flashcards:
        st.markdown("---")
        st.header("🔍 Flashcards")
        
        # Flashcard navigation
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.button("⬅️ Previous", on_click=prev_flashcard)
        with col2:
            current_card = st.session_state.flashcards[st.session_state.current_flashcard]
            st.markdown(f'<div class="flashcard"><h3>Question:</h3><p>{current_card["question"]}</p></div>', unsafe_allow_html=True)
            
            if st.session_state.show_answer:
                st.markdown(f'<div class="flashcard"><h3>Answer:</h3><p>{current_card["answer"]}</p></div>', unsafe_allow_html=True)
            
            show_hide_label = "Hide Answer" if st.session_state.show_answer else "Show Answer"
            st.button(show_hide_label, on_click=toggle_answer)
            
            # Display flashcard counter
            st.write(f"Card {st.session_state.current_flashcard + 1} of {len(st.session_state.flashcards)}")
        with col3:
            st.button("Next ➡️", on_click=next_flashcard)

if __name__ == "__main__":
    main()
