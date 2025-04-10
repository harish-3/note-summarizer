"""
Enhanced LLM Processor with support for multiple providers

This module implements the LLM processing functionality with support for
various LLM providers including OpenAI, Hugging Face, Anthropic, and Google.
"""

import os
from typing import Dict, Any, List, Optional
import json

class EnhancedLLMProcessor:
    """
    Enhanced LLM processor that supports multiple providers.
    """
    
    def __init__(self, provider_id: str, model_id: str, api_key: Optional[str] = None, 
                 temperature: float = 0.5, max_tokens: int = 512):
        """
        Initialize the LLM processor with the specified provider and model.
        
        Args:
            provider_id: ID of the LLM provider
            model_id: ID of the specific model to use
            api_key: API key for the provider (if required)
            temperature: Temperature parameter for generation
            max_tokens: Maximum tokens to generate
        """
        self.provider_id = provider_id
        self.model_id = model_id
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize the appropriate LLM based on provider
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on the provider."""
        if self.provider_id == "openai":
            return self._initialize_openai()
        elif self.provider_id == "huggingface":
            return self._initialize_huggingface()
        elif self.provider_id == "anthropic":
            return self._initialize_anthropic()
        elif self.provider_id == "google":
            return self._initialize_google()
        elif self.provider_id == "local":
            return self._initialize_local()
        else:
            raise ValueError(f"Unsupported provider: {self.provider_id}")
    
    def _initialize_openai(self):
        """Initialize OpenAI LLM."""
        try:
            from langchain.llms import OpenAI
            from langchain_openai import ChatOpenAI
            
            if not self.api_key:
                raise ValueError("API key is required for OpenAI")
            
            os.environ["OPENAI_API_KEY"] = self.api_key
            
            return ChatOpenAI(
                model_name=self.model_id,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        except ImportError:
            raise ImportError("OpenAI package not installed. Please install it with: pip install langchain-openai")
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI LLM: {str(e)}")
    
    def _initialize_huggingface(self):
        """Initialize Hugging Face LLM."""
        try:
            from langchain_community.llms import HuggingFaceHub
            
            if not self.api_key:
                raise ValueError("API key is required for Hugging Face")
            
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = self.api_key
            
            return HuggingFaceHub(
                repo_id=self.model_id,
                huggingfacehub_api_token=self.api_key,
                model_kwargs={
                    "temperature": self.temperature,
                    "max_length": self.max_tokens
                }
            )
        except ImportError:
            raise ImportError("Hugging Face package not installed. Please install it with: pip install langchain-community")
        except Exception as e:
            raise ValueError(f"Failed to initialize Hugging Face LLM: {str(e)}")
    
    def _initialize_anthropic(self):
        """Initialize Anthropic LLM."""
        try:
            from langchain_anthropic import ChatAnthropic
            
            if not self.api_key:
                raise ValueError("API key is required for Anthropic")
            
            os.environ["ANTHROPIC_API_KEY"] = self.api_key
            
            return ChatAnthropic(
                model=self.model_id,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                anthropic_api_key=self.api_key
            )
        except ImportError:
            raise ImportError("Anthropic package not installed. Please install it with: pip install langchain-anthropic")
        except Exception as e:
            raise ValueError(f"Failed to initialize Anthropic LLM: {str(e)}")
    
    def _initialize_google(self):
        """Initialize Google AI (Gemini) LLM."""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            if not self.api_key:
                raise ValueError("API key is required for Google AI")
            
            os.environ["GOOGLE_API_KEY"] = self.api_key
            
            return ChatGoogleGenerativeAI(
                model=self.model_id,
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                google_api_key=self.api_key
            )
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Please install it with: pip install langchain-google-genai")
        except Exception as e:
            raise ValueError(f"Failed to initialize Google AI LLM: {str(e)}")
    
    def _initialize_local(self):
        """Initialize local LLM (placeholder for now)."""
        # This would require additional setup for local models
        raise NotImplementedError("Local models are not yet supported in this version")
    
    def process_notes(self, text: str) -> Dict[str, Any]:
        """
        Process notes text to generate summary and flashcards.
        
        Args:
            text: The text content of the notes
            
        Returns:
            Dictionary containing summary and flashcards
        """
        # Truncate text if too long
        max_input_length = 4000
        if len(text) > max_input_length:
            text = text[:max_input_length] + "..."
        
        # Generate summary
        summary = self._generate_summary(text)
        
        # Generate flashcards
        flashcards = self._generate_flashcards(text)
        
        return {
            "summary": summary,
            "flashcards": flashcards
        }
    
    def _generate_summary(self, text: str) -> str:
        """Generate a summary of the notes."""
        prompt = f"""
        Please summarize the following academic notes in a concise but comprehensive manner.
        Focus on the main concepts, key points, and important details.
        
        NOTES:
        {text}
        
        SUMMARY:
        """
        
        try:
            if self.provider_id in ["openai", "anthropic", "google"]:
                from langchain.schema import HumanMessage
                response = self.llm.invoke([HumanMessage(content=prompt)])
                return response.content
            else:
                response = self.llm.invoke(prompt)
                return response
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _generate_flashcards(self, text: str) -> List[Dict[str, str]]:
        """Generate flashcards from the notes."""
        prompt = f"""
        Create 5 question-answer flashcards based on the following academic notes.
        Focus on the most important concepts and facts.
        Format your response as a JSON array of objects with 'question' and 'answer' fields.
        
        NOTES:
        {text}
        
        FLASHCARDS (JSON format):
        """
        
        try:
            if self.provider_id in ["openai", "anthropic", "google"]:
                from langchain.schema import HumanMessage
                response = self.llm.invoke([HumanMessage(content=prompt)])
                response_text = response.content
            else:
                response_text = self.llm.invoke(prompt)
            
            # Extract JSON from response
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                try:
                    flashcards = json.loads(json_str)
                    return flashcards
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    pass
            
            # If JSON extraction fails, create a default flashcard
            return [
                {
                    "question": "What are the main topics covered in these notes?",
                    "answer": "The notes cover various academic concepts. Please review the summary for details."
                }
            ]
        except Exception as e:
            # Return a default flashcard on error
            return [
                {
                    "question": "Error creating flashcards",
                    "answer": f"An error occurred: {str(e)}"
                }
            ]
