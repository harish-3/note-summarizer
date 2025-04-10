"""
Streamlit app entry point for cloud deployment

This file serves as the main entry point for the Note Summarizer application
when deployed to Streamlit Cloud.
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main application
from app.main import main

# Run the application
if __name__ == "__main__":
    main()
