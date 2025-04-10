# User Guide: Note Summarizer Application (Updated)

## Introduction

Welcome to the Note Summarizer Application! This tool is designed to help students efficiently process their academic notes by automatically generating concise summaries and interactive flashcards. By leveraging the power of Large Language Models (LLMs), this application transforms lengthy notes into study-friendly formats that enhance learning and retention.

## New Features: Flexible LLM Integration

The application now supports multiple LLM providers, allowing you to choose your preferred AI model and use your own API keys. This gives you greater control over the quality and cost of the AI processing.

### Supported LLM Providers

- **Hugging Face** - Access to models like Flan-T5, BART, and GPT-Neo
- **OpenAI** - Access to GPT-3.5 Turbo and GPT-4 models
- **Anthropic** - Access to Claude models (coming soon)
- **Local Models** - Support for locally hosted models (advanced setup required)

## Getting Started

### System Requirements

- Web browser (Chrome, Firefox, Safari, or Edge recommended)
- Internet connection
- Academic notes in PDF or DOCX format
- API key for your chosen LLM provider

### Accessing the Application

The Note Summarizer Application is deployed on Streamlit and can be accessed through any web browser. No installation or account creation is required to use the application.

## Features Overview

### 1. LLM Configuration

- **Provider Selection**: Choose from multiple AI providers
- **Model Selection**: Select specific models based on your needs
- **API Key Management**: Securely input your own API keys
- **Advanced Settings**: Adjust parameters like temperature and max tokens

### 2. File Upload

- **Supported Formats**: PDF (.pdf) and Microsoft Word (.docx) documents
- **File Size Limit**: Files up to 200MB can be processed
- **File Information**: After upload, the application displays details about your file including filename, size, and type

### 3. Note Processing

- **Text Extraction**: The application automatically extracts text content from your uploaded documents
- **AI Processing**: The extracted text is processed by your chosen language model to identify key concepts and important information
- **Processing Time**: Processing time varies based on file size, complexity, and chosen model

### 4. Summary Generation

- **Concise Summaries**: The application generates a condensed version of your notes, focusing on main ideas and key concepts
- **Structured Format**: Summaries maintain the logical structure of the original content while eliminating redundancy
- **Highlighting**: Important terms and concepts are emphasized in the summary

### 5. Flashcard Creation

- **Question-Answer Format**: Flashcards are presented in a traditional question on one side, answer on the other format
- **Key Concept Focus**: Flashcards target the most important concepts, definitions, and facts from your notes
- **Interactive Navigation**: Easily move between flashcards with previous/next buttons
- **Show/Hide Answers**: Test your knowledge by revealing answers only when you're ready

### 6. Theme Customization

- **Light/Dark Mode**: Switch between light and dark themes based on your preference
- **Responsive Design**: The interface adapts to different screen sizes, including mobile devices

## Step-by-Step Usage Guide

### Step 1: Configure Your LLM

1. Navigate to the "LLM Configuration" tab
2. Select your preferred LLM provider from the dropdown menu
3. Choose a specific model from the available options
4. Enter your API key if required (see provider-specific instructions)
5. Adjust advanced settings if desired (temperature, max tokens)
6. Click "Save Configuration" to apply your settings
7. Wait for the connection test to complete

### Step 2: Upload Your Notes

1. Navigate to the "Upload & Process" tab
2. Click on the "Choose a file" button
3. Select a PDF or DOCX file from your device
4. Wait for the file to upload (a progress indicator will be displayed)
5. Once uploaded, you'll see file information displayed below the upload area

### Step 3: Process Your Notes

1. After uploading your file, click the "Process Notes" button
2. A processing status message will appear, indicating that your notes are being analyzed
3. Wait for the processing to complete (this may take a few moments depending on file size and chosen model)

### Step 4: Review Your Results

1. Once processing is complete, you'll be automatically taken to the "Results" tab
2. Read through the generated summary to get a concise overview of your notes
3. Explore the flashcards section to test your knowledge
4. Use the "Show Answer" button to reveal answers
5. Navigate between flashcards using the "Previous" and "Next" buttons

## Provider-Specific Information

### Hugging Face

- **API Key**: Required for most models
- **Where to Get Key**: https://huggingface.co/settings/tokens
- **Recommended Models**:
  - Flan-T5 Base: Good general-purpose model
  - BART Large CNN: Specialized for summarization tasks

### OpenAI

- **API Key**: Required for all models
- **Where to Get Key**: https://platform.openai.com/api-keys
- **Recommended Models**:
  - GPT-3.5 Turbo: Fast and cost-effective
  - GPT-4: Higher quality but more expensive

### Anthropic (Coming Soon)

- **API Key**: Will be required
- **Where to Get Key**: https://console.anthropic.com/settings/keys

### Local Models (Advanced)

- **Setup Required**: Requires separate installation and configuration
- **No API Key**: Uses locally installed models

## Tips for Best Results

1. **Choose the Right Model**: Different models have different strengths. For summarization, BART or GPT models often perform best
2. **Use Well-Structured Notes**: The application works best with clearly organized notes that have headings, paragraphs, and a logical flow
3. **Check File Quality**: Ensure PDF files are text-based rather than scanned images for better text extraction
4. **Process Chapters Separately**: For very large documents, consider splitting them into smaller sections for more focused summaries
5. **Review Generated Content**: While the AI is powerful, always review the generated summaries for accuracy
6. **Experiment with Settings**: Try adjusting the temperature setting to control the creativity of the AI output

## Troubleshooting

### Common Issues and Solutions

1. **API Key Errors**
   - Verify that you've entered the correct API key
   - Check that you have sufficient credits/quota with your provider
   - Ensure you have the necessary permissions for the selected model

2. **File Upload Fails**
   - Ensure your file is in PDF or DOCX format
   - Check that the file size is under the limit
   - Try a different browser if problems persist

3. **Text Extraction Issues**
   - For PDFs, ensure they contain actual text (not just scanned images)
   - For DOCX files, avoid complex formatting or embedded objects
   - Try converting your file to a different format and re-uploading

4. **Processing Takes Too Long**
   - Large files may take longer to process
   - More powerful models (like GPT-4) take longer than simpler models
   - Check your internet connection
   - Try processing a smaller portion of your notes

5. **Summary or Flashcards Seem Inaccurate**
   - Try a different model that may be better suited to your content
   - Adjust the temperature setting (lower for more factual output)
   - The quality of output depends on the clarity and structure of input notes
   - Technical or specialized content may be summarized with varying accuracy

## Privacy and Data Security

- Your uploaded files are processed temporarily and are not permanently stored
- Your API keys are used only for the current session and are not saved between sessions
- The application does not collect personal information
- Uploaded content is only used for generating summaries and flashcards

## Technical Support

If you encounter issues not covered in this guide, please reach out to the development team with:
- A description of the problem
- Steps to reproduce the issue
- Information about your browser and operating system
- Which LLM provider and model you were using

## Future Enhancements

The Note Summarizer Application is continuously improving. Planned future features include:
- Support for additional file formats
- More LLM providers and models
- Custom flashcard creation
- Export options for summaries and flashcards
- Collaborative note sharing

Thank you for using the Note Summarizer Application! We hope it enhances your learning experience.
