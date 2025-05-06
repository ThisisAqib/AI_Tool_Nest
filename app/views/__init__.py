"""
Views Package

This package handles all template-based views and pages for the application.
It uses the centralized template configuration from core.templates.
"""

from fastapi import APIRouter
from app.core.templates import templates
from app.views.text_summarizer import text_summarizer_router
from app.views.image_to_text import image_to_text_router
from app.views.text_paraphraser import text_paraphraser_router

# Create main views router
views_router = APIRouter()

# Import view routers
from app.views.home import home_router

# Include home route
views_router.include_router(home_router, tags=["pages"])

# Include summarizer route
views_router.include_router(text_summarizer_router)

# Include image to text route
views_router.include_router(image_to_text_router)

# Include text paraphraser route
views_router.include_router(text_paraphraser_router)
