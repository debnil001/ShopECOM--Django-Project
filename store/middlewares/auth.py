from django.shortcuts import redirect
from django.http import HttpResponseRedirect
def auth_middlewares(get_response):
    def middleware(request):
        returnURL=request.META['PATH_INFO']
        print(returnURL)
        if not request.session.get('customer'):
            return HttpResponseRedirect(f'/signin?returnurl={returnURL}')
        response = get_response(request)
        return response
    return middleware