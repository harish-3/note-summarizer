"""
Streamlit deployment configuration for Note Summarizer Application
"""

import os
import toml

# Create a requirements.txt file
requirements = [
    "streamlit",
    "python-docx",
    "PyPDF2",
    "langchain",
    "huggingface_hub"
]

with open("requirements.txt", "w") as f:
    f.write("\n".join(requirements))

# Create a .streamlit directory and config.toml file for theme configuration
os.makedirs(".streamlit", exist_ok=True)

config = {
    "theme": {
        "primaryColor": "#4CAF50",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#000000",
        "font": "sans serif"
    }
}

with open(".streamlit/config.toml", "w") as f:
    toml.dump(config, f)

print("Deployment files created successfully!")
