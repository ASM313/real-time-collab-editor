from fastapi import APIRouter
from app.schemas.room import AutocompleteRequest, AutocompleteResponse
from app.services.autocomplete_service import AutocompleteService

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])


@router.post("", response_model=AutocompleteResponse)
async def get_autocomplete(request: AutocompleteRequest) -> AutocompleteResponse:
    """
    Get autocomplete suggestions for a given prefix.
    
    Args:
        request: AutocompleteRequest with prefix and language
        
    Returns:
        AutocompleteResponse: List of suggested completions
    """
    autocomplete_service = AutocompleteService()
    suggestions = autocomplete_service.get_suggestions(request.prefix, request.language)
    return AutocompleteResponse(suggestions=suggestions)
