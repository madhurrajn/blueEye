from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from startnow import  Scheduler

def handlePostMethod(request):
    print "Inside post method"
    print request.body
    orig_lat = request.POST.get("orig_lat")
    orig_lng = request.POST.get("orig_lng")
    dest_lat = request.POST.get("dest_lat")
    dest_lng = request.POST.get("dest_lng")
    sched = Scheduler(orig_lat, orig_lng, dest_lat, dest_lng)
    return (sched.get_schedule())

def index(request):
    if request.method == 'POST':
        list = handlePostMethod(request)
        template = loader.get_template('startnow/dir.html')
        context = RequestContext(request, {
            'sched_list':list})
        return HttpResponse(template.render(context))
    else:
        template = loader.get_template('startnow/index.html')
        context = RequestContext(request)
        return HttpResponse(template.render(context))

def empty(request):
    return HttpResponse('')


# Create your views here.
