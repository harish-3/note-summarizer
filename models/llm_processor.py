"""
LLM Integration Module for Note Summarizer Application

This module handles the integration with LLM models for generating summaries and flashcards.
"""

import os
from typing import Dict, List, Any, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub

class LLMProcessor:
    """Class to handle LLM processing for note summarization and flashcard generation."""
    
    def __init__(self, huggingface_api_token: Optional[str] = None):
        """
        Initialize the LLM processor.
        
        Args:
            huggingface_api_token: Optional API token for HuggingFace Hub
        """
        # Set HuggingFace API token if provided
        if huggingface_api_token:
            os.environ["HUGGINGFACE_API_TOKEN"] = huggingface_api_token
        
        # Initialize the LLM
        self.llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",  # Using a free model
            model_kwargs={"temperature": 0.5, "max_length": 512}
        )
        
        # Create prompt templates
        self.summary_prompt = self._create_summary_prompt()
        self.flashcard_prompt = self._create_flashcard_prompt()
        
        # Create LLM chains
        self.summary_chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)
        self.flashcard_chain = LLMChain(llm=self.llm, prompt=self.flashcard_prompt)
    
    def _create_summary_prompt(self) -> PromptTemplate:
        """
        Create a prompt template for summarization.
        
        Returns:
            PromptTemplate for summarization
        """
        template = """
        You are an expert academic assistant. Your task is to create a concise summary of the following academic notes.
        Focus on the key concepts, main ideas, and important details. Organize the summary in a clear and structured way.
        
        ACADEMIC NOTES:
        {notes}
        
        SUMMARY:
        """
        
        return PromptTemplate(
            input_variables=["notes"],
            template=template
        )
    
    def _create_flashcard_prompt(self) -> PromptTemplate:
        """
        Create a prompt template for flashcard generation.
        
        Returns:
            PromptTemplate for flashcard generation
        """
        template = """
        You are an expert academic assistant. Your task is to create flashcards based on the following academic notes.
        Each flashcard should have a question on one side and the answer on the other side.
        Focus on key concepts, definitions, and important facts that would be useful for studying.
        Create at least 5 flashcards, but no more than 10.
        
        Format each flashcard as:
        Q: [Question]
        A: [Answer]
        
        ACADEMIC NOTES:
        {notes}
        
        FLASHCARDS:
        """
        
        return PromptTemplate(
            input_variables=["notes"],
            template=template
        )
    
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
