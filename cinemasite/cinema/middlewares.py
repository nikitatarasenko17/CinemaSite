from django.contrib.auth import logout
from django.http import HttpResponseRedirect, response
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from django.urls import reverse
from django.contrib import messages


"""Чтобы использовать в качестве атрибута, в не в качестве функции
            #TypeError: 'bool' object is not callable отображается, когда вы пытаетесь вести себя с объектом так,
            #как будто это метод или функция."""

# class SessionIdleTimeout(MiddlewareMixin):
#     def process_request(self, request):
#         if not request.user.is_superuser: 
#             current_datetime = datetime.timestamp(datetime.now())
#             if ('last_activity' in request.session):
#                 last = (current_datetime - request.session['last_activity'])
#                 if last > 60:
#                     logout(request)
#                     return HttpResponseRedirect('/')
#             else:
#                 request.session['last_activity'] = current_datetime


class SessionIdleTimeout(MiddlewareMixin):
    def process_request(self, request):
        current_datetime = datetime.timestamp(datetime.now())
        if ('last_activity' in request.session) and not request.user.is_superuser and \
            (current_datetime - request.session['last_activity']) > 60: 
            logout(request)
            # messages.add_message(request, messages.ERROR, 'Your session has been timed out.')
            return HttpResponseRedirect(reverse('login'))
        else:
            request.session['last_activity'] = current_datetime
    


