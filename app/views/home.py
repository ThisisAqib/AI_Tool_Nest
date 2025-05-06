"""
Home Page Views Module

This module handles the rendering of the main pages of the application,
including the home page and other static pages.
"""

from fastapi import APIRouter, Request
from app.core.templates import templates

# Create router for page views
home_router = APIRouter(
    tags=["pages"], include_in_schema=False  # Exclude from API documentation
)


@home_router.get("/")
async def home(request: Request):
    """
    Render the home page of the application.

    Args:
        request (Request): The incoming request object

    Returns:
        TemplateResponse: The rendered home page template with context
    """
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Welcome to AI Tool Nest",
            # Additional context variables can be added here
        },
    )
