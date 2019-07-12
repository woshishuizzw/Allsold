import datetime
from django.utils.deprecation import MiddlewareMixin

from .models import Flow


class Middleware1(MiddlewareMixin):
    def process_view(self,request, view_func, view_args, view_kwargs):
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        res = Flow.objects.filter(ftime=time).first()
        if res:
            res.view+= 1
            res.save()
        else:

            tmp = Flow(view=1,ftime=time)
            tmp.save()