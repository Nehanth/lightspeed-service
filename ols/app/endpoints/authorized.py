"""Handler for REST API call to provide user feedback."""

import asyncio
import logging

from fastapi import APIRouter, Request

from ols.app.models.models import (
    AuthorizationResponse,
    ErrorResponse,
    ForbiddenResponse,
    UnauthorizedResponse,
)
from ols.utils.auth_dependency import AuthDependency

logger = logging.getLogger(__name__)
router = APIRouter(tags=["authorized"])
auth_dependency = AuthDependency(virtual_path="/ols-access")

authorized_responses = {
    200: {
        "description": "The user is logged-in and authorized to access OLS",
        "model": AuthorizationResponse,
    },
    401: {
        "description": "Missing or invalid credentials provided by client",
        "model": UnauthorizedResponse,
    },
    403: {
        "description": "User is not authorized",
        "model": ForbiddenResponse,
    },
    500: {
        "description": "Unexpected error during token review",
        "model": ErrorResponse,
    },
}


@router.post("/authorized", responses=authorized_responses)
def is_user_authorized(request: Request) -> AuthorizationResponse:
    """Validate if the logged-in user is authorized to access OLS.

    Parameters:
        request (Request): The FastAPI request object.

    Returns:
        The user's UID and username if authentication and authorization succeed.

    Raises:
        HTTPException: If authentication fails or the user does not have access.

    """
    user_id, username = asyncio.run(auth_dependency(request))
    return AuthorizationResponse(
        user_id=user_id,
        username=username,
    )
