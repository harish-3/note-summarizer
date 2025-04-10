# Note Summarizer Application

This is a Streamlit application that allows students to upload their academic notes and receive concise summaries, key points, and flashcards generated using Large Language Models (LLMs).

## Features

- Upload notes in PDF or DOCX format
- Extract text content from uploaded files
- Generate concise summaries of academic notes
- Create flashcards with questions and answers for studying
- Switch between light and dark themes
- Interactive flashcard navigation

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app/main.py
```

## Project Structure

```
note_summarizer/
├── app/
│   └── main.py              # Main Streamlit application
├── data/                    # Directory for sample data
├── docs/                    # Documentation
├── models/
│   ├── llm_processor.py     # LLM integration for processing notes
│   └── prompt_templates.py  # Prompt templates for LLM
├── utils/
│   ├── file_parser.py       # File parsing utilities
│   └── file_upload.py       # File upload utilities
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Usage

1. Upload your academic notes in PDF or DOCX format
2. Click the "Process Notes" button
3. View the generated summary
4. Use the flashcard navigation to study key concepts

## Deployment

This application can be deployed to Streamlit Cloud:

1. Push the code to a GitHub repository
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your GitHub repository
4. Select the main.py file as the entry point

## License

This project is licensed under the MIT License.
