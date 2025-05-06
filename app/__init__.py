"""
AI Tool Nest - Application Package

This package contains the core application logic, including:
- View routes
- Database models
- Business logic
- Configuration
"""

from fastapi import FastAPI, APIRouter

from app.views import views_router


# Main router that combines all application routers
main_router = APIRouter()


def include_routers(app: FastAPI) -> None:
    """
    Include all application routers in the FastAPI application.

    This function sets up view routes by including them
    in the main router and then including the main router in the app.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Include views routes
    main_router.include_router(views_router)

    # Include the main router in the app
    app.include_router(main_router)
