"""
LLM Configuration Interface for Note Summarizer Application

This module implements the Streamlit interface for LLM provider and API key configuration.
"""

import streamlit as st
from typing import Dict, Tuple, Optional
from models.llm_provider import LLMProviderManager
from models.enhanced_llm_processor import EnhancedLLMProcessor

def setup_llm_configuration() -> Tuple[str, str, Optional[str], float, int]:
    """
    Set up the LLM configuration interface in the Streamlit app.
    
    Returns:
        Tuple containing the selected provider ID, model ID, API key (if applicable),
        temperature, and max tokens.
    """
    st.header("🤖 LLM Configuration")
    st.write("Configure the Language Model to use for generating summaries and flashcards.")
    
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
    model_descriptions = {model["name"]: model["description"] for model in models}
    
    selected_model_name = st.selectbox(
        "Select Model",
        options=model_names,
        index=0,
        help="Choose the specific model to use"
    )
    
    # Display model description
    if selected_model_name in model_descriptions:
        st.info(model_descriptions[selected_model_name])
    
    # Get model ID from name
    selected_model_id = provider_manager.get_model_id_by_name(selected_provider_id, selected_model_name)
    
    # API key input if required
    api_key = None
    if provider_manager.requires_api_key(selected_provider_id):
        api_key_instruction = provider_manager.get_api_key_instruction(selected_provider_id)
        if api_key_instruction:
            st.markdown(f"**API Key Instructions:** {api_key_instruction}")
        
        api_key = st.text_input(
            f"Enter your {selected_provider_name} API Key",
            type="password",
            help=f"Your API key for {selected_provider_name}"
        )
    
    # Advanced options (collapsible)
    with st.expander("Advanced Options"):
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Higher values make output more random, lower values more deterministic"
        )
        
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=2000,
            value=512,
            step=50,
            help="Maximum length of generated text"
        )
    
    return selected_provider_id, selected_model_id, api_key, temperature, max_tokens

def display_llm_status(provider_id: str, model_id: str) -> None:
    """
    Display the current LLM configuration status.
    
    Args:
        provider_id: Selected provider ID
        model_id: Selected model ID
    """
    provider_manager = LLMProviderManager()
    providers = provider_manager.get_providers()
    
    if provider_id in providers:
        provider_name = providers[provider_id]["name"]
        
        # Find model name
        model_name = model_id
        for model in providers[provider_id]["models"]:
            if model["id"] == model_id:
                model_name = model["name"]
                break
        
        st.sidebar.success(f"Using: {provider_name} - {model_name}")
    else:
        st.sidebar.warning("No LLM configured")

def save_llm_config_to_session_state(provider_id: str, model_id: str, 
                                    api_key: Optional[str], temperature: float, 
                                    max_tokens: int) -> None:
    """
    Save the LLM configuration to session state.
    
    Args:
        provider_id: Selected provider ID
        model_id: Selected model ID
        api_key: API key (if applicable)
        temperature: Temperature parameter
        max_tokens: Max tokens parameter
    """
    st.session_state.llm_provider_id = provider_id
    st.session_state.llm_model_id = model_id
    st.session_state.llm_api_key = api_key
    st.session_state.llm_temperature = temperature
    st.session_state.llm_max_tokens = max_tokens
    st.session_state.llm_configured = True

def get_llm_config_from_session_state() -> Tuple[str, str, Optional[str], float, int, bool]:
    """
    Get the LLM configuration from session state.
    
    Returns:
        Tuple containing provider ID, model ID, API key, temperature, max tokens, and configured flag
    """
    provider_id = st.session_state.get("llm_provider_id", "huggingface")
    model_id = st.session_state.get("llm_model_id", "google/flan-t5-base")
    api_key = st.session_state.get("llm_api_key", None)
    temperature = st.session_state.get("llm_temperature", 0.5)
    max_tokens = st.session_state.get("llm_max_tokens", 512)
    configured = st.session_state.get("llm_configured", False)
    
    return provider_id, model_id, api_key, temperature, max_tokens, configured

def initialize_llm_processor() -> Optional[EnhancedLLMProcessor]:
    """
    Initialize the LLM processor based on session state configuration.
    
    Returns:
        Initialized EnhancedLLMProcessor or None if not configured or initialization failed
    """
    provider_id, model_id, api_key, temperature, max_tokens, configured = get_llm_config_from_session_state()
    
    if not configured:
        return None
    
    try:
        return EnhancedLLMProcessor(
            provider_id=provider_id,
            model_id=model_id,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    except Exception as e:
        st.error(f"Failed to initialize LLM processor: {str(e)}")
        return None
