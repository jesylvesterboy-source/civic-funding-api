from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "message": "Civic Funding API Enterprise Stack",
        "status": "Operational",
        "modules": ["Staff Performance", "Farmer Engagement", "Video Calls"],
        "version": "1.0.0"
    })
