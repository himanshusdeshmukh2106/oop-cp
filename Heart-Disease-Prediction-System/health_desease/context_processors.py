"""
Context processors to make variables available in all templates
"""
from django.conf import settings

def google_maps_key(request):
    """Make Google Maps API key available in templates"""
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
