"""
Web Application Entry Point

This module serves as the entry point for the web application.
It initializes the application and sets up static files.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app import include_routers


def create_app() -> FastAPI:
    """
    Create and configure the web application.

    Returns:
        FastAPI: The configured application instance.
    """
    app = FastAPI(
        title="AI Tool Nest",
        description="A modern web application using HTMX and Tailwind CSS",
        version="1.0.0",
        root_path="/ai-tool-nest",
    )

    # Mount static directory for serving static files (CSS, JS, images)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Include all application routers (views only)
    include_routers(app)

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings

    # Run the application with hot reload enabled for development
    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
