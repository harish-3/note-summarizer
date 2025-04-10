"""
Updated LLM Provider Module for Note Summarizer Application

This module handles the integration with multiple LLM providers and API key configuration.
"""

from typing import Dict, List, Any, Optional, Tuple
import os
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms.openai import OpenAI
from langchain.llms.base import BaseLLM

class LLMProviderManager:
    """Class to manage multiple LLM providers and their configurations."""
    
    def __init__(self):
        """Initialize the LLM provider manager."""
        self.providers = {
            "huggingface": {
                "name": "Hugging Face",
                "models": [
                    {"id": "google/flan-t5-base", "name": "Flan-T5 Base", "description": "Google's Flan-T5 Base model - Good general purpose model"},
                    {"id": "google/flan-t5-large", "name": "Flan-T5 Large", "description": "Google's Flan-T5 Large model - Better quality but slower"},
                    {"id": "facebook/bart-large-cnn", "name": "BART Large CNN", "description": "Facebook's BART model fine-tuned on CNN articles - Good for summarization"},
                    {"id": "EleutherAI/gpt-neo-1.3B", "name": "GPT-Neo 1.3B", "description": "EleutherAI's GPT-Neo model - Open source alternative to GPT models"}
                ],
                "requires_api_key": True,
                "api_key_name": "HUGGINGFACE_API_TOKEN",
                "api_key_instruction": "Get your API key from https://huggingface.co/settings/tokens"
            },
            "openai": {
                "name": "OpenAI",
                "models": [
                    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and efficient model for most tasks"},
                    {"id": "gpt-4", "name": "GPT-4", "description": "Most powerful model, better for complex tasks but slower and more expensive"}
                ],
                "requires_api_key": True,
                "api_key_name": "OPENAI_API_KEY",
                "api_key_instruction": "Get your API key from https://platform.openai.com/api-keys"
            },
            "anthropic": {
                "name": "Anthropic",
                "models": [
                    {"id": "claude-2", "name": "Claude 2", "description": "Anthropic's Claude 2 model - Good for thoughtful, nuanced responses"},
                    {"id": "claude-instant", "name": "Claude Instant", "description": "Faster, more efficient version of Claude"}
                ],
                "requires_api_key": True,
                "api_key_name": "ANTHROPIC_API_KEY",
                "api_key_instruction": "Get your API key from https://console.anthropic.com/settings/keys"
            }
        }
        
        # Add local models option
        self.providers["local"] = {
            "name": "Local Models",
            "models": [
                {"id": "local/llama2", "name": "Llama 2 (Local)", "description": "Meta's Llama 2 model running locally - Requires separate installation"}
            ],
            "requires_api_key": False,
            "api_key_name": None,
            "api_key_instruction": "No API key needed. Ensure you have the model installed locally."
        }
    
    def get_providers(self) -> Dict[str, Dict]:
        """
        Get all available providers.
        
        Returns:
            Dictionary of providers and their configurations
        """
        return self.providers
    
    def get_provider_names(self) -> List[str]:
        """
        Get list of provider display names.
        
        Returns:
            List of provider display names
        """
        return [provider["name"] for provider in self.providers.values()]
    
    def get_provider_id_by_name(self, name: str) -> Optional[str]:
        """
        Get provider ID by display name.
        
        Args:
            name: Provider display name
            
        Returns:
            Provider ID or None if not found
        """
        for provider_id, provider in self.providers.items():
            if provider["name"] == name:
                return provider_id
        return None
    
    def get_models_for_provider(self, provider_id: str) -> List[Dict]:
        """
        Get available models for a specific provider.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            List of models for the provider
        """
        if provider_id in self.providers:
            return self.providers[provider_id]["models"]
        return []
    
    def get_model_names_for_provider(self, provider_id: str) -> List[str]:
        """
        Get list of model display names for a specific provider.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            List of model display names
        """
        if provider_id in self.providers:
            return [model["name"] for model in self.providers[provider_id]["models"]]
        return []
    
    def get_model_id_by_name(self, provider_id: str, name: str) -> Optional[str]:
        """
        Get model ID by display name for a specific provider.
        
        Args:
            provider_id: Provider ID
            name: Model display name
            
        Returns:
            Model ID or None if not found
        """
        if provider_id in self.providers:
            for model in self.providers[provider_id]["models"]:
                if model["name"] == name:
                    return model["id"]
        return None
    
    def requires_api_key(self, provider_id: str) -> bool:
        """
        Check if a provider requires an API key.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            True if the provider requires an API key, False otherwise
        """
        if provider_id in self.providers:
            return self.providers[provider_id]["requires_api_key"]
        return False
    
    def get_api_key_name(self, provider_id: str) -> Optional[str]:
        """
        Get the environment variable name for a provider's API key.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            Environment variable name or None if not applicable
        """
        if provider_id in self.providers and self.providers[provider_id]["requires_api_key"]:
            return self.providers[provider_id]["api_key_name"]
        return None
    
    def get_api_key_instruction(self, provider_id: str) -> Optional[str]:
        """
        Get instructions for obtaining an API key for a provider.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            Instructions or None if not applicable
        """
        if provider_id in self.providers and self.providers[provider_id]["requires_api_key"]:
            return self.providers[provider_id]["api_key_instruction"]
        return None
    
    def create_llm(self, provider_id: str, model_id: str, api_key: Optional[str] = None, 
                  temperature: float = 0.5, max_tokens: int = 512) -> Optional[BaseLLM]:
        """
        Create an LLM instance based on provider and model.
        
        Args:
            provider_id: Provider ID
            model_id: Model ID
            api_key: API key (if required)
            temperature: Temperature parameter for the model
            max_tokens: Maximum tokens parameter for the model
            
        Returns:
            LLM instance or None if creation failed
        """
        # Set API key as environment variable if provided
        if api_key and self.requires_api_key(provider_id):
            api_key_name = self.get_api_key_name(provider_id)
            if api_key_name:
                os.environ[api_key_name] = api_key
        
        try:
            if provider_id == "huggingface":
                return HuggingFaceHub(
                    repo_id=model_id,
                    model_kwargs={"temperature": temperature, "max_length": max_tokens}
                )
            elif provider_id == "openai":
                if "gpt-3.5" in model_id or "gpt-4" in model_id:
                    return ChatOpenAI(
                        model_name=model_id,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                else:
                    return OpenAI(
                        model_name=model_id,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
            elif provider_id == "anthropic":
                # This would require additional implementation for Anthropic's Claude
                # For now, we'll return None to indicate it's not implemented
                return None
            elif provider_id == "local":
                # This would require additional implementation for local models
                # For now, we'll return None to indicate it's not implemented
                return None
        except Exception as e:
            print(f"Error creating LLM: {str(e)}")
            return None
        
        return None
