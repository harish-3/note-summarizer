# Technical Documentation: Note Summarizer Application

## Architecture Overview

The Note Summarizer Application is built with a modular architecture that separates concerns and promotes maintainability. The application consists of the following main components:

1. **User Interface Layer** - Built with Streamlit
2. **File Processing Layer** - Handles file uploads and text extraction
3. **LLM Integration Layer** - Processes extracted text using language models
4. **Output Generation Layer** - Creates summaries and flashcards

## Component Details

### 1. User Interface Layer

The UI is implemented using Streamlit, a Python framework for building data applications. The main UI components include:

- File upload widget
- Processing status indicators
- Summary display section
- Interactive flashcard component
- Theme switching functionality

**Key Files:**
- `/app/main.py` - Main application entry point and UI implementation

### 2. File Processing Layer

This layer handles file uploads and extracts text content from PDF and DOCX files.

**Key Files:**
- `/utils/file_upload.py` - Manages file upload functionality
- `/utils/file_parser.py` - Extracts text from different file formats

**Key Classes:**
- `FileParser` - Main class for parsing different file formats
  - `parse_file()` - Entry point for file parsing
  - `parse_pdf()` - PDF-specific parsing logic
  - `parse_docx()` - DOCX-specific parsing logic

### 3. LLM Integration Layer

This layer integrates with language models to process the extracted text.

**Key Files:**
- `/models/llm_processor.py` - Handles LLM integration and processing
- `/models/prompt_templates.py` - Defines prompts for different tasks

**Key Classes:**
- `LLMProcessor` - Main class for LLM integration
  - `generate_summary()` - Generates summaries from notes
  - `generate_flashcards()` - Creates flashcards from notes
  - `process_notes()` - Combines summary and flashcard generation

### 4. Output Generation Layer

This layer formats and presents the processed results to the user.

**Implementation:**
- The output generation is integrated into the main application file
- Summary display uses Streamlit's markdown rendering
- Flashcards use a custom interactive component with state management

## Data Flow

1. User uploads a file through the Streamlit interface
2. The file is saved to a temporary location
3. The file parser extracts text content based on file type
4. The extracted text is sent to the LLM processor
5. The LLM processor generates a summary and flashcards
6. Results are displayed in the UI

## Dependencies

The application relies on the following key dependencies:

- `streamlit` - For the web interface
- `python-docx` - For parsing DOCX files
- `PyPDF2` - For parsing PDF files
- `langchain` - For LLM integration
- `huggingface_hub` - For accessing free LLM models

## Deployment

The application is configured for deployment on Streamlit Cloud:

1. The `requirements.txt` file lists all necessary dependencies
2. The `.streamlit/config.toml` file contains theme configuration
3. The main entry point is `/app/main.py`

## Development Guidelines

### Adding New File Formats

To add support for a new file format:

1. Add a new parsing method in `FileParser` class
2. Update the `is_supported_file()` function
3. Update the file uploader in the UI to accept the new format

### Modifying LLM Integration

To change the LLM model or adjust prompts:

1. Update the model configuration in `LLMProcessor.__init__()`
2. Modify prompt templates in `prompt_templates.py`

### UI Customization

To customize the UI:

1. Modify the CSS in the `apply_theme()` function in `main.py`
2. Update the Streamlit configuration in `.streamlit/config.toml`

## Testing

While formal tests are not included in this version, manual testing should focus on:

1. File upload with different file formats and sizes
2. Text extraction accuracy
3. Summary and flashcard quality
4. UI responsiveness and theme switching
5. Error handling and edge cases

## Future Development

Potential areas for enhancement include:

1. Adding support for more file formats (e.g., TXT, HTML)
2. Implementing user accounts for saving results
3. Adding export functionality for summaries and flashcards
4. Implementing more advanced LLM prompting techniques
5. Adding analytics to track usage patterns

## Troubleshooting

Common development issues:

1. **LLM API Rate Limits** - Free models may have usage limitations
2. **Memory Issues** - Large files may cause memory problems
3. **Deployment Errors** - Check requirements.txt for compatibility

## Security Considerations

1. Temporary files are deleted after processing
2. No user data is permanently stored
3. File processing is done server-side
4. No authentication is required for this version
