from typing import Dict, List
import time

from django.http import HttpRequest, HttpResponseBadRequest  # The limit on the number of requests


REQUESTS_PER_MIN: int = 3


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.history_requests: Dict[str, List[float]] = dict()

    def __call__(self, request: HttpRequest):
        client_ip: str = request.META["REMOTE_ADDR"]
        client_history: List[float] = self.history_requests.get(client_ip, list())

        if not client_history:
            self.history_requests[client_ip] = list()

        # The limit on the number of requests is 3 request per minute
        if len(client_history) >= REQUESTS_PER_MIN:
            if time.time() - client_history[REQUESTS_PER_MIN - 1] < 60:  # 1 min
                return HttpResponseBadRequest(
                    f"Exceeded the allowed number of "
                    f"requests per minute ({REQUESTS_PER_MIN})<br>"
                    f"Client history: {client_history}"
                )

            # add time of last request and cut history
            client_history = client_history[:REQUESTS_PER_MIN - 1]
        client_history.insert(0, time.time())

        self.history_requests[client_ip] = client_history
        request.history_requests = client_history

        return self.get_response(request)
