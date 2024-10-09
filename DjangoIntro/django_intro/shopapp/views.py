from typing import Dict, Any

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def shop_index(request: HttpRequest) -> HttpResponse:
    context: Dict[str, Any] = {
        "value1": 2,
        "value2": 3,
        "headers": [
            "a" * num for num in range(5)
        ]
    }
    return render(request, "shopapp/shop-index.html", context=context)
