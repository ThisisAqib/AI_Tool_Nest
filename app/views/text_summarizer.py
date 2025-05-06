"""
Text Summarizer Views

This module provides the view routes for the text summarizer functionality.
"""

import httpx
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from app.core.templates import templates
from app.core.config import settings
from typing import Optional

text_summarizer_router = APIRouter(tags=["Text Summarizer Views"])


@text_summarizer_router.get("/ai-text-summarizer")
async def summarizer_view(request: Request):
    """
    Render the text summarizer page.

    Args:
        request (Request): The incoming request

    Returns:
        TemplateResponse: The rendered template
    """
    return templates.TemplateResponse(
        "text-summarizer.html", {"request": request, "title": "AI Text Summarizer"}
    )


@text_summarizer_router.post("/ai-text-summarizer")
async def summarize_text(
    text: str = Form(...),
    mode: str = Form("paragraph"),
    max_length: Optional[int] = Form(None),
    custom_instructions: Optional[str] = Form(None),
    extract_keywords: bool = Form(True),
):
    """
    Process the text and return a summary with statistics.

    Args:
        text (str): The input text to summarize
        mode (str): Summarization mode (paragraph, bullet_points, or custom)
        max_length (int, optional): Maximum length for paragraph mode
        custom_instructions (str, optional): Custom instructions for custom mode
        extract_keywords (bool): Whether to extract key terms from the text

    Returns:
        HTMLResponse: The summarized text, keywords, and statistics
    """
    try:
        # Calculate statistics
        word_count = len(text.split())
        char_count = len(text)

        # Prepare API request
        api_url = f"{settings.AI_TOOL_NEST_API_URL}/summarize"
        headers = {
            "X-API-Key": settings.AI_TOOL_NEST_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "mode": mode,
            "max_length": max_length,
            "custom_instructions": custom_instructions,
            "extract_keywords": extract_keywords,
        }

        # Make API request
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload, headers=headers)

            if response.status_code != 200:
                error_detail = response.json().get("detail", "Failed to summarize text")
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

            result = response.json()

        # Prepare the response with OOB updates
        keywords_html = ""
        if result.get("keywords"):
            keywords_html = '<div class="mt-4"><h3 class="text-sm font-medium text-gray-700 mb-2">Key Terms</h3><div class="flex flex-wrap gap-2">'
            for keyword in result["keywords"]:
                keywords_html += f'<span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">{keyword}</span>'
            keywords_html += "</div></div>"

        response_html = f"""
            <textarea id="output-text" class="w-full p-3 md:p-5 min-h-[250px] md:min-h-[400px] border rounded-md" placeholder="Your summary will appear here...">{result["summary"]}</textarea>
            {keywords_html}
            <div id="word-count" hx-swap-oob="true" class="text-gray-600">
                Words: {word_count}
            </div>
            <div id="char-count" hx-swap-oob="true" class="text-gray-600">
                Characters: {char_count}
            </div>
        """

        return HTMLResponse(content=response_html)

    except HTTPException as e:
        error_html = f"""
            <textarea id="output-text" class="w-full p-3 md:p-5 min-h-[250px] md:min-h-[400px] border border-red-500 rounded-md" placeholder="Error occurred...">{e.detail}</textarea>
            <div id="word-count" hx-swap-oob="true" class="text-gray-600">
                Words: {word_count}
            </div>
            <div id="char-count" hx-swap-oob="true" class="text-gray-600">
                Characters: {char_count}
            </div>
        """
        return HTMLResponse(content=error_html, status_code=e.status_code)
    except Exception as e:
        error_html = f"""
            <textarea id="output-text" class="w-full p-3 md:p-5 min-h-[250px] md:min-h-[400px] border border-red-500 rounded-md" placeholder="Error occurred...">An unexpected error occurred. Please try again later.</textarea>
            <div id="word-count" hx-swap-oob="true" class="text-gray-600">
                Words: {word_count}
            </div>
            <div id="char-count" hx-swap-oob="true" class="text-gray-600">
                Characters: {char_count}
            </div>
        """
        return HTMLResponse(content=error_html, status_code=500)
