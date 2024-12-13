from django.http import JsonResponse
from django.views import View
import logging

class ExampleView(View):
    def get(self, request):
        logging.getLogger('django').info("Example route accessed")
        return JsonResponse({"message": "Hello, world!"})