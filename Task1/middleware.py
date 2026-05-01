import requests
from django.http import JsonResponse
from django.core.cache import cache


class EgyptOnlyMiddleware:
    ALLOWED_COUNTRY = "EG"
    CACHE_TIMEOUT = 60 * 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if not self.is_from_egypt(ip):
            return JsonResponse(
                {"error": "Access restricted to Egypt only."},
                status=403
            )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def is_from_egypt(self, ip):
        if ip in ("127.0.0.1", "::1") or ip.startswith("192.168.") or ip.startswith("10."):
            return True

        cache_key = f"geo_country_{ip}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached == self.ALLOWED_COUNTRY

        try:
            response = requests.get(
                f"http://ip-api.com/json/{ip}?fields=countryCode",
                timeout=3
            )
            data = response.json()
            country = data.get("countryCode", "")
        except Exception:
            country = self.ALLOWED_COUNTRY

        cache.set(cache_key, country, self.CACHE_TIMEOUT)
        return country == self.ALLOWED_COUNTRY