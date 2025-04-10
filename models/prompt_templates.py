"""
Prompt Templates Module for Note Summarizer Application

This module contains the prompt templates for summarization and flashcard generation.
"""

from langchain.prompts import PromptTemplate

def get_summary_prompt() -> PromptTemplate:
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

def get_flashcard_prompt() -> PromptTemplate:
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
