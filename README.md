# AI Tool Nest

AI Tool Nest is a modern web application that provides a suite of AI-powered tools for text and image processing. Built with FastAPI and HTMX, it offers a responsive and user-friendly interface for various AI operations.

## Features

- **Text Summarizer**: Condense long texts into concise summaries with keyword extraction
- **Image to Text**: Extract text and descriptions from images using OCR and image analysis
- **Text Paraphraser**: Rephrase text with different styles and tones

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTMX + Tailwind CSS
- **Package Manager**: uv (modern Python package manager)
- **Template Engine**: Jinja2
- **HTTP Client**: HTTPX

## Prerequisites

- Python 3.11 or higher
- UV package manager (`pip install uv`)
- Access to AI Tool Nest API (separate service)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ThisisAqib/AI_Tool_Nest.git
   cd AI_Tool_Nest
   ```

2. Create virtual environment and install dependencies:
   ```bash
   uv sync
   ```

3. Configure environment variables:
   ```bash
   cp .env-example .env
   # Edit .env with your settings
   ```

4. Run the application:
   ```bash
   uv run main.py
   ```

## API Integration

This application requires the AI Tool Nest API to be running. Make sure to:
1. Set up the [AI Tool Nest API](https://github.com/ThisisAqib/AI_Tool_Nest_API)
2. Configure the API URL and key in your `.env` file

## Documentation

- **Technical Guide**: See [docs/technical.md](docs/technical.md) for detailed technical documentation, API endpoints, and development guidelines
- **Architecture**: See [docs/architecture.md](docs/architecture.md) for system design, components, and architectural decisions

## Development

- The application runs on port 8001 by default
- HTMX is used for dynamic interactions
- Tailwind CSS is used for styling
- Templates are in the `app/templates` directory
- Views are in the `app/views` directory

## Project Structure

```
.
├── app/
│   ├── core/          # Core configuration and utilities
│   ├── static/        # Static files (CSS, JS)
│   ├── templates/     # HTML templates
│   ├── views/         # View handlers
│   └── __init__.py    # Application initialization
├── docs/              # Documentation
├── main.py           # Application entry point
├── pyproject.toml    # Project dependencies
└── .env-example      # Environment template
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

