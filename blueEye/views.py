from django.shortcuts import render, get_object_or_404
from .models import CellInfo, CompareCell, busyHourDaily
from .core import Cell
from django.template import RequestContext, loader
from django.http import HttpResponse
from .core import getCellBeamForm, getNeighbors
from schedProc import reArrangeSched, schedule_chart
from efficiency import getNeighborEffciency
import logging

# Create your views here.
logging.basicConfig(format='%(asctime)s {%(filename)s: %(lineno)d} %(funcName)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

def saveSchedule(request):
    cell_name =""
    startHour =""
    endHour =""
    pd = 0
    busyHourList = {}
    if request.method == 'POST':
        cell_name = request.POST.get("CellName", "")
        startHour = request.POST.get("StartHour", "")
        endHour = request.POST.get("EndHour", "")
        pd = request.POST.get("popDen", "")
        id = request.POST.get("identity", "")
        print cell_name, startHour, endHour, pd, id
        if id == '9999':
            elem = busyHourDaily()
        else:
            elem = busyHourDaily.objects.get(pk=id)
        print startHour, endHour
        if not int(startHour) >= int(endHour):
            print "Here"
            elem.startHour = startHour
            elem.endHour = endHour 
            elem.density = int(pd)
            print pd
            cell_obj = CellInfo.objects.get(cell_name=cell_name)
            elem.busyHour = cell_obj
            elem.save()
            logging.debug("Saving New Element pd %d", int(pd))
            reArrangeSched(elem, cell_obj)
    cht = schedule_chart(request,cell_name)
    template = loader.get_template('blueEye/showSchedule.html')
    busyHourList = busyHourDaily.objects.filter(busyHour=cell_name)
    context = RequestContext(request, 
              {'busyHourList':busyHourList,
               'cell_name':cell_name,
               'sched_chart':cht})
    return HttpResponse(template.render(context))

def addSchedule(request, cell_name):
    busyHourList = {}
    template = loader.get_template('blueEye/showSchedule.html')
    busyHourList = busyHourDaily.objects.filter(busyHour=cell_name)
    cht = schedule_chart(request,cell_name)
    context = RequestContext(request, 
              {'busyHourList':busyHourList,
                'cell_name':cell_name,
                'addSchedule':True,
                'sched_chart':cht})
    return HttpResponse(template.render(context))


def deleteSchedule(request, cell_name, pk):
    try:
        elem = busyHourDaily.objects.get(pk=pk)
        elem.delete()
    except:
        print "Element not found"
    cell_obj = CellInfo.objects.get(cell_name=cell_name)
    reArrangeSched(0,cell_obj)
    template = loader.get_template('blueEye/showSchedule.html')
    busyHourList = busyHourDaily.objects.filter(busyHour=cell_name)
    cht = schedule_chart(request,cell_name)
    context = RequestContext(request, 
              {'busyHourList':busyHourList,
               'cell_name':cell_name,
               'sched_chart':cht})
    return HttpResponse(template.render(context))

def changeSchedule(request, cell_name, pk):
    busyHourList = {}
    template = loader.get_template('blueEye/showSchedule.html')
    busyHourList = busyHourDaily.objects.filter(busyHour=cell_name)
    elem = busyHourDaily.objects.get(pk=pk)
    cht = schedule_chart(request,cell_name)
    context = RequestContext(request, 
              {'busyHourList':busyHourList,
               'cell_name':cell_name,
              'elem':elem,
              'sched_chart':cht})
    return HttpResponse(template.render(context))

def showSchedule(request):
    busyHourList = {}
    print "showSchedule Called"
    template = loader.get_template('blueEye/showSchedule.html')
    cell_name = ""
    if request.method == 'POST':
        cell_name = request.POST.get("CellName", "")
        busyHourList = busyHourDaily.objects.filter(busyHour=cell_name)
        if len(busyHourList) == 0:
            try:
                cell_obj = CellInfo.objects.get(cell_name=cell_name)
                reArrangeSched(0, cell_obj)
            except:
                cell_obj=""
    sched_chart = schedule_chart(request,cell_name)
    print sched_chart.datasource
    context = RequestContext(request, 
              {'busyHourList':busyHourList,
               'cell_name':cell_name,
               'sched_chart': sched_chart})
    return HttpResponse(template.render(context))

def index(request):
    print "Index Method called"
    cellinfo = []
    cell_list = CellInfo.objects.all()
    compare_cells = CompareCell.objects.all()
    if request.method == 'POST':
        if request.POST.get("postMethod", "") == "AddToCompare":
            cell_name = request.POST.get("CellName", "")
            found = False
            for c in compare_cells:
                if c.cell_name == cell_name:
                    found = True
                    break;
            if found == False:
                newCompareCell = CompareCell()
                newCompareCell.cell_name = cell_name
                newCompareCell.save()
        if request.POST.get("postMethod", "") == "CompareDelete":
            cell_name = request.POST.get("CellName", "")
            print cell_name
            found = False
            for c in compare_cells:
                if c.cell_name == cell_name:
                    print "Match Found"
                    print c.id
                    obj=CompareCell.objects.get(pk=c.id)
                    obj.delete()
    compare_cells = CompareCell.objects.all()
    template = loader.get_template('blueEye/index.html')
    compareCells = getCellBeamForm(True)
    celldict = []
    cellCompare = []
    if compareCells:
        cellCompare = compareCells.items()
    for key,cell in cellCompare:
        cellinfo.append(cell)
    cellsfound = getCellBeamForm(False)
    if cellsfound:
        celldict = cellsfound.items()
    cell_list=[]
    for cell in compare_cells:
        cell_list.append(cell.cell_name)
    for key,cell in celldict:
        cellinfo.append(cell)
    context = RequestContext(request, {
        'cellinfo': cellinfo,
        'cell_list': cell_list})
    return HttpResponse(template.render(context))

def neighborInfo(request):
    template = loader.get_template('blueEye/neighborInfo.html')
    cell_name = ""
    pivotCell = ""
    neighbor_list = []
    if request.method == 'POST':
        cell_name = request.POST.get("CellName", "")
        pivotCell,neighbor_list = getNeighbors(cell_name)
    context = RequestContext(request, {
        'pivotCell': pivotCell,
        'neighbor_list': neighbor_list})
    return HttpResponse(template.render(context))

def efficiency(request):
    template = loader.get_template('blueEye/efficiency.html')
    cell_name = ""
    cosector_cells = []
    efficiency_list = []
    print "Here"
    if request.method == 'POST':
        cell_name = request.POST.get("CellName", "")
        cosector_cells,efficiency_list = getNeighborEffciency(cell_name)
    context = RequestContext(request, {
        'cosector_cells': cosector_cells,
        'efficiency_list': efficiency_list})
    return HttpResponse(template.render(context))


def empty(request):
    return HttpResponse('')

def resetParams():
    newCellReqeust_g = True

def addNewCell(request):
    resetParams()
    index(request)
