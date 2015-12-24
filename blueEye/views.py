from django.shortcuts import render, get_object_or_404
from .models import CellInfo, CompareCell, busyHourDaily
from .core import Cell
from django.template import RequestContext, loader
from django.http import HttpResponse
from .core import getCellBeamForm

# Create your views here.

def showSchedule(request):
    cell_list = CellInfo.objects.all()
    busyHourList = {}
    print "showSchedule Called"
    template = loader.get_template('blueEye/showSchedule.html')
    if request.method == 'POST':
        print request.POST
        cell_name = request.POST.get("CellName", "")
        print cell_name
        busyHourList = busyHourDaily.objects.filter(busyHour=cell_name)
        print busyHourList
        for busyHour in busyHourList:
            print busyHour
    context = RequestContext(request, 
              {'busyHourList':busyHourList})
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
    cellsfound = getCellBeamForm(False)
    celldict = []
    cellCompare = []
    if cellsfound:
        celldict = cellsfound.items()
    cell_list=[]
    for cell in compare_cells:
        cell_list.append(cell.cell_name)
    for key,cell in celldict:
        cellinfo.append(cell)
    compareCells = getCellBeamForm(True)
    if compareCells:
        cellCompare = compareCells.items()
    for key,cell in cellCompare:
        cellinfo.append(cell)
    context = RequestContext(request, {
        'cellinfo': cellinfo,
        'cell_list': cell_list})
    return HttpResponse(template.render(context))

def empty(request):
    return HttpResponse('')

def resetParams():
    newCellReqeust_g = True

def addNewCell(request):
    resetParams()
    index(request)
