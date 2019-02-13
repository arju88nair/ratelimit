from django.http import JsonResponse
from django.core.cache import cache


"""[Global throttler ]

Uses Redis for caching the hash of the user ip with the ip and checks and increments it everytime and blocks it 
if it gets over a the certain limit

Returns:
    [type] -- [description]
"""

def globalThrottler(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        count=1
        user_ip=get_client_ip(request)
        user_hash=hash(user_ip)
        ip_exists=cache.get(user_hash)
        if(ip_exists):
            if(ip_exists > 5):
                return JsonResponse({"message":"You got to ease up there cowboy"},status=403)
            else:
                ip_exists+=1
                cache.set(user_hash, ip_exists)
                return JsonResponse("hi",safe=False)
        else:
            cache.set(user_hash, int(count),timeout=35)
            return JsonResponse(user_hash,safe=False)
   
    return middleware

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip