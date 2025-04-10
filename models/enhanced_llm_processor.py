"""
Enhanced LLM Processor Module for Note Summarizer Application

This module handles the integration with multiple LLM models for generating summaries and flashcards.
"""

import os
from typing import Dict, List, Any, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import BaseLLM
from models.llm_provider import LLMProviderManager
from models.prompt_templates import get_summary_prompt, get_flashcard_prompt

class EnhancedLLMProcessor:
    """Class to handle LLM processing with multiple provider options."""
    
    def __init__(self, provider_id: str, model_id: str, api_key: Optional[str] = None,
                 temperature: float = 0.5, max_tokens: int = 512):
        """
        Initialize the enhanced LLM processor.
        
        Args:
            provider_id: Provider ID (e.g., "huggingface", "openai")
            model_id: Model ID (e.g., "google/flan-t5-base", "gpt-3.5-turbo")
            api_key: Optional API key for the provider
            temperature: Temperature parameter for the model
            max_tokens: Maximum tokens parameter for the model
        """
        # Initialize the LLM provider manager
        self.provider_manager = LLMProviderManager()
        
        # Store configuration
        self.provider_id = provider_id
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Create the LLM instance
        self.llm = self.provider_manager.create_llm(
            provider_id=provider_id,
            model_id=model_id,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if not self.llm:
            raise ValueError(f"Failed to initialize LLM with provider '{provider_id}' and model '{model_id}'")
        
        # Create prompt templates
        self.summary_prompt = get_summary_prompt()
        self.flashcard_prompt = get_flashcard_prompt()
        
        # Create LLM chains
        self.summary_chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)
        self.flashcard_chain = LLMChain(llm=self.llm, prompt=self.flashcard_prompt)
    
    def generate_summary(self, notes: str) -> str:
        """
        Generate a summary of the provided notes.
        
        Args:
            notes: Text content of the notes
            
        Returns:
            Generated summary
        """
        return self.summary_chain.run(notes=notes)
    
    def generate_flashcards(self, notes: str) -> List[Dict[str, str]]:
        """
        Generate flashcards from the provided notes.
        
        Args:
            notes: Text content of the notes
            
        Returns:
            List of flashcards, each as a dictionary with 'question' and 'answer' keys
        """
        raw_flashcards = self.flashcard_chain.run(notes=notes)
        
        # Parse the raw flashcards text into a structured format
        flashcards = []
        current_question = None
        current_answer = None
        
        for line in raw_flashcards.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('Q:'):
                # If we have a previous Q&A pair, add it to the list
                if current_question and current_answer:
                    flashcards.append({
                        'question': current_question,
                        'answer': current_answer
                    })
                
                # Start a new Q&A pair
                current_question = line[2:].strip()
                current_answer = None
            elif line.startswith('A:'):
                current_answer = line[2:].strip()
        
        # Add the last Q&A pair if it exists
        if current_question and current_answer:
            flashcards.append({
                'question': current_question,
                'answer': current_answer
            })
        
        return flashcards
    
    def process_notes(self, notes: str) -> Dict[str, Any]:
        """
        Process notes to generate both summary and flashcards.
        
        Args:
            notes: Text content of the notes
            
        Returns:
            Dictionary containing the generated summary and flashcards
        """
        summary = self.generate_summary(notes)
        flashcards = self.generate_flashcards(notes)
        
        return {
            'summary': summary,
            'flashcards': flashcards
        }
    
    @staticmethod
    def get_available_providers() -> Dict[str, Dict]:
        """
        Get all available LLM providers.
        
        Returns:
            Dictionary of providers and their configurations
        """
        provider_manager = LLMProviderManager()
        return provider_manager.get_providers()
    
    @staticmethod
    def get_provider_names() -> List[str]:
        """
        Get list of provider display names.
        
        Returns:
            List of provider display names
        """
        provider_manager = LLMProviderManager()
        return provider_manager.get_provider_names()
    
    @staticmethod
    def get_models_for_provider(provider_id: str) -> List[Dict]:
        """
        Get available models for a specific provider.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            List of models for the provider
        """
        provider_manager = LLMProviderManager()
        return provider_manager.get_models_for_provider(provider_id)
    
    @staticmethod
    def requires_api_key(provider_id: str) -> bool:
        """
        Check if a provider requires an API key.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            True if the provider requires an API key, False otherwise
        """
        provider_manager = LLMProviderManager()
        return provider_manager.requires_api_key(provider_id)
    
    @staticmethod
    def get_api_key_instruction(provider_id: str) -> Optional[str]:
        """
        Get instructions for obtaining an API key for a provider.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            Instructions or None if not applicable
        """
        provider_manager = LLMProviderManager()
        return provider_manager.get_api_key_instruction(provider_id)
