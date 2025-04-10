"""
Enhanced LLM Provider Manager with additional models

This module manages different LLM providers and their models.
"""

from typing import Dict, List, Any, Optional

class LLMProviderManager:
    """Manager for LLM providers and their models."""
    
    def __init__(self):
        """Initialize the LLM provider manager with available providers."""
        self.providers = {
            "huggingface": {
                "name": "Hugging Face",
                "requires_api_key": True,
                "api_key_instruction": "Get your API key from https://huggingface.co/settings/tokens",
                "models": [
                    {
                        "id": "google/flan-t5-base",
                        "name": "Flan-T5 Base",
                        "description": "A good general-purpose model for text generation and summarization."
                    },
                    {
                        "id": "google/flan-t5-large",
                        "name": "Flan-T5 Large",
                        "description": "A larger version of Flan-T5 with better performance but slower processing."
                    },
                    {
                        "id": "facebook/bart-large-cnn",
                        "name": "BART Large CNN",
                        "description": "Specialized for summarization tasks, particularly news articles."
                    },
                    {
                        "id": "EleutherAI/gpt-neo-1.3B",
                        "name": "GPT-Neo 1.3B",
                        "description": "An open-source alternative to GPT models with good general capabilities."
                    },
                    {
                        "id": "mistralai/Mistral-7B-Instruct-v0.2",
                        "name": "Mistral 7B Instruct",
                        "description": "A powerful instruction-tuned model with strong performance on various tasks."
                    }
                ]
            },
            "openai": {
                "name": "OpenAI",
                "requires_api_key": True,
                "api_key_instruction": "Get your API key from https://platform.openai.com/api-keys",
                "models": [
                    {
                        "id": "gpt-3.5-turbo",
                        "name": "GPT-3.5 Turbo",
                        "description": "Fast and cost-effective model with good general capabilities."
                    },
                    {
                        "id": "gpt-4",
                        "name": "GPT-4",
                        "description": "OpenAI's most powerful model with advanced reasoning capabilities."
                    }
                ]
            },
            "anthropic": {
                "name": "Anthropic",
                "requires_api_key": True,
                "api_key_instruction": "Get your API key from https://console.anthropic.com/settings/keys",
                "models": [
                    {
                        "id": "claude-3-haiku-20240307",
                        "name": "Claude 3 Haiku",
                        "description": "Fast and efficient model for everyday tasks."
                    },
                    {
                        "id": "claude-3-sonnet-20240229",
                        "name": "Claude 3 Sonnet",
                        "description": "Balanced model with strong reasoning capabilities."
                    },
                    {
                        "id": "claude-3-opus-20240229",
                        "name": "Claude 3 Opus",
                        "description": "Anthropic's most powerful model for complex tasks."
                    }
                ]
            },
            "google": {
                "name": "Google AI (Gemini)",
                "requires_api_key": True,
                "api_key_instruction": "Get your API key from https://ai.google.dev/",
                "models": [
                    {
                        "id": "gemini-pro",
                        "name": "Gemini Pro",
                        "description": "Google's advanced model with strong reasoning capabilities."
                    },
                    {
                        "id": "gemini-flash",
                        "name": "Gemini Flash",
                        "description": "Faster version of Gemini optimized for quick responses."
                    }
                ]
            },
            "local": {
                "name": "Local Models",
                "requires_api_key": False,
                "api_key_instruction": "",
                "models": [
                    {
                        "id": "llama3",
                        "name": "Llama 3 (Local)",
                        "description": "Open-source model that can be run locally (requires separate setup)."
                    },
                    {
                        "id": "mistral-local",
                        "name": "Mistral (Local)",
                        "description": "Open-source model that can be run locally (requires separate setup)."
                    }
                ]
            }
        }
    
    def get_providers(self) -> Dict[str, Any]:
        """Get all available providers."""
        return self.providers
    
    def get_provider_names(self) -> List[str]:
        """Get a list of provider names."""
        return [provider["name"] for provider in self.providers.values()]
    
    def get_provider_id_by_name(self, name: str) -> str:
        """Get provider ID from name."""
        for provider_id, provider in self.providers.items():
            if provider["name"] == name:
                return provider_id
        return "huggingface"  # Default fallback
    
    def get_models_for_provider(self, provider_id: str) -> List[Dict[str, str]]:
        """Get available models for a specific provider."""
        if provider_id in self.providers:
            return self.providers[provider_id]["models"]
        return []
    
    def get_model_id_by_name(self, provider_id: str, model_name: str) -> str:
        """Get model ID from name for a specific provider."""
        if provider_id in self.providers:
            for model in self.providers[provider_id]["models"]:
                if model["name"] == model_name:
                    return model["id"]
        return ""
    
    def requires_api_key(self, provider_id: str) -> bool:
        """Check if a provider requires an API key."""
        if provider_id in self.providers:
            return self.providers[provider_id]["requires_api_key"]
        return False
    
    def get_api_key_instruction(self, provider_id: str) -> str:
        """Get API key instructions for a provider."""
        if provider_id in self.providers:
            return self.providers[provider_id]["api_key_instruction"]
        return ""
