"""
Text Paraphraser Views

This module provides the view routes for the text paraphraser functionality.
"""

import httpx
import markdown2
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.core.templates import templates
from app.core.config import settings
from typing import Optional

text_paraphraser_router = APIRouter(tags=["Text Paraphraser Views"])


@text_paraphraser_router.get("/ai-text-paraphraser")
async def paraphraser_view(request: Request):
    """
    Render the text paraphraser page.

    Args:
        request (Request): The incoming request

    Returns:
        TemplateResponse: The rendered template
    """
    return templates.TemplateResponse(
        "text-paraphraser.html", {"request": request, "title": "AI Text Paraphraser"}
    )


@text_paraphraser_router.post("/ai-text-paraphraser")
async def process_text(
    request: Request,
    text: str = Form(...),
    style: str = Form("casual"),
    intensity: str = Form("medium"),
    length_option: str = Form("same"),
):
    """
    Process the text and return the paraphrased version.

    Args:
        request (Request): The incoming request
        text (str): The text to paraphrase
        style (str): Paraphrasing style (casual, formal, simple)
        intensity (str): Paraphrasing intensity (low, medium, high)
        length_option (str): Desired output length (same, shorter, longer)

    Returns:
        HTMLResponse: The paraphrased text
    """
    try:
        # Prepare API request
        api_url = f"{settings.AI_TOOL_NEST_API_URL}/paraphrase"
        headers = {"X-API-Key": settings.AI_TOOL_NEST_API_KEY}

        # Prepare request data
        json_data = {
            "text": text,
            "style": style,
            "intensity": intensity,
            "length_option": length_option,
        }

        # Make API request
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=headers, json=json_data)

            if response.status_code != 200:
                error_detail = response.json().get(
                    "detail", "Failed to paraphrase text"
                )
                raise ValueError(error_detail)

            result = response.json()

        # Convert paraphrased text to HTML using markdown
        paraphrased_html = markdown2.markdown(result["paraphrased_text"])

        # Prepare the response HTML
        response_html = f"""
            <div class="space-y-4">
                <div class="bg-white p-4 rounded-xl border border-gray-200 prose prose-sm max-w-none">
                    {paraphrased_html}
                </div>
                <div class="flex justify-end">
                    <button onclick="navigator.clipboard.writeText(document.querySelector('#result-container .prose').innerText).then(() => this.innerHTML = 'Copied!')" 
                            class="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
                        </svg>
                        Copy
                    </button>
                </div>
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
