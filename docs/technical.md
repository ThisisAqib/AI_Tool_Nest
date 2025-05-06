# Technical Documentation

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTMX + Tailwind CSS
- **Package Manager**: uv (modern Python package manager)
- **Template Engine**: Jinja2
- **HTTP Client**: HTTPX

## Project Configuration

### Environment Variables
```env
# Security
SECRET_KEY="your-secret-key"

# CORS Settings
BACKEND_CORS_ORIGINS='["http://localhost:8000","http://localhost:3000"]'

# FastAPI Settings
HOST="0.0.0.0"
PORT=8001
RELOAD=True

# AI Tool Nest API Configuration
AI_TOOL_NEST_API_URL="http://localhost:8002/ai-tool-nest-api/v1/endpoints/ai-tools"
AI_TOOL_NEST_API_KEY="your-api-key"
```

## API Integration

### Base URL
```python
AI_TOOL_NEST_API_URL = "http://localhost:8002/ai-tool-nest-api/v1/endpoints/ai-tools"
```

### Endpoints

1. **Text Summarizer**
   ```python
   POST /summarize
   Content-Type: application/json
   X-API-Key: your-api-key

   {
     "text": "string",
     "mode": "paragraph|bullet_points|custom",
     "max_length": "optional[int]",
     "custom_instructions": "optional[str]",
     "extract_keywords": "bool"
   }
   ```

2. **Image to Text**
   ```python
   POST /image-to-text
   X-API-Key: your-api-key
   Content-Type: multipart/form-data

   {
     "image_file": "file|null",
     "image_url": "string|null",
     "mode": "description|ocr|detailed",
     "detail_level": "brief|standard|comprehensive"
   }
   ```

3. **Text Paraphraser**
   ```python
   POST /paraphrase
   Content-Type: application/json
   X-API-Key: your-api-key

   {
     "text": "string",
     "style": "casual|formal|simple",
     "intensity": "low|medium|high",
     "length_option": "same|shorter|longer"
   }
   ```

## Frontend Development

### Template Structure
```
templates/
├── base.html          # Base template with common layout
├── home.html          # Home page
├── text-summarizer.html
├── image-to-text.html
├── text-paraphraser.html
├── components/        # Reusable components
└── partials/         # Partial templates
```

### HTMX Usage
```html
<!-- Example of HTMX integration -->
<form hx-post="/ai-text-summarizer"
      hx-target="#result-container"
      hx-indicator="#loading">
  <!-- Form fields -->
</form>
```

## Error Handling

### API Errors
```python
try:
    response = await client.post(url, headers=headers, json=data)
    if response.status_code != 200:
        error_detail = response.json().get("detail", "Error message")
        raise HTTPException(status_code=response.status_code, detail=error_detail)
except Exception as e:
    # Handle error and return user-friendly response
```

### Frontend Error Display
```html
<div class="p-4 rounded-xl bg-red-50 border border-red-200">
    <p class="text-sm text-red-700">{error_message}</p>
</div>
```

## Best Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes
- Keep functions focused and small

### Performance
1. Async Operations
   - Use async/await consistently
   - Handle concurrent requests properly
   - Implement timeouts

2. Template Optimization
   - Minimize template inheritance depth
   - Use partial templates efficiently
   - Cache where appropriate
