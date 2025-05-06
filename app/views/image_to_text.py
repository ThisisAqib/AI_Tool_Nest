"""
Image to Text Views

This module provides the view routes for the image to text functionality.
"""

import httpx
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from app.core.templates import templates
from app.core.config import settings
from typing import Optional
import markdown2

image_to_text_router = APIRouter(tags=["Image to Text Views"])


@image_to_text_router.get("/ai-image-to-text")
async def image_to_text_view(request: Request):
    """
    Render the image to text page.

    Args:
        request (Request): The incoming request

    Returns:
        TemplateResponse: The rendered template
    """
    return templates.TemplateResponse(
        "image-to-text.html", {"request": request, "title": "AI Image to Text"}
    )


@image_to_text_router.post("/ai-image-to-text")
async def process_image(
    request: Request,
    image_file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
    mode: str = Form(default="description"),
    detail_level: str = Form(default="standard"),
):
    """
    Process the image and return the analysis.

    Args:
        request (Request): The incoming request
        image_file (UploadFile, optional): Uploaded image file
        image_url (str, optional): URL of the image
        mode (str): Analysis mode (description, ocr, detailed)
        detail_level (str): Level of detail (brief, standard, comprehensive)

    Returns:
        HTMLResponse: The analysis results
    """
    try:
        # Input validation
        if not image_file and not image_url:
            error_html = """
                <div class="p-4 rounded-xl bg-red-50 border border-red-200">
                    <p class="text-sm text-red-700">Please provide either an image file or URL</p>
                </div>
            """
            return HTMLResponse(content=error_html, status_code=400)

        # Prepare API request
        api_url = f"{settings.AI_TOOL_NEST_API_URL}/image-to-text"
        headers = {"X-API-Key": settings.AI_TOOL_NEST_API_KEY}

        # Prepare form data
        form_data = {"mode": mode, "detail_level": detail_level}

        files = {}
        if image_file:
            content = await image_file.read()
            files["image_file"] = (
                image_file.filename,
                content,
                image_file.content_type,
            )
        elif image_url:
            form_data["image_url"] = image_url

        # Make API request
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url, headers=headers, data=form_data, files=files
            )

            if response.status_code != 200:
                error_detail = response.json().get("detail", "Failed to analyze image")
                raise ValueError(error_detail)

            result = response.json()

        # Convert analysis text to HTML using markdown
        analysis_html = markdown2.markdown(result["analysis"])

        # Prepare the response HTML
        response_html = f"""
            <div class="space-y-4">
                <div class="bg-white p-4 rounded-xl border border-gray-200 prose prose-sm max-w-none">
                    {analysis_html}
                </div>
                
                {'''
                <div class="bg-gray-50 p-4 rounded-xl border border-gray-200">
                    <h3 class="text-sm font-medium text-gray-900 mb-2">Structured Text</h3>
                    <pre class="whitespace-pre-wrap text-sm text-gray-700">{result["structured_text"]}</pre>
                </div>
                ''' if result.get("structured_text") else ''}
            </div>
        """

        return HTMLResponse(content=response_html)

    except Exception as e:
        error_html = f"""
            <div class="p-4 rounded-xl bg-red-50 border border-red-200">
                <p class="text-sm text-red-700">{str(e)}</p>
            </div>
        """
        return HTMLResponse(content=error_html, status_code=400)
