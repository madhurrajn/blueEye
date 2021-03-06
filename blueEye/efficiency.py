from collections import defaultdict
from chartit import PivotDataPool, Chart, PivotChart
from .models import CellInfo, RoundClock
import logging
import bisect
from django.db.models import Sum

CELL_MAX_CAPACITY = 99

logging.basicConfig(format='%(asctime)s {%(filename)s: %(lineno)d} %(funcName)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

class cellState():
    CELL_ON = 1
    CELL_OFF = 2
    CELL_UP = 3

class CellState:
    def __init__(self, den, cell_name, state):
        self.density = den
        self.cell_name = cell_name
        self.state = state

class Efficiency:
    def __init__(self):
        self.density = 0
        self.cell_list = []

def getCoSectorCells(pivot, cell_list):
    cosector_list = []
    for cell in cell_list:
        if (pivot.lattitude  == cell.lattitude  and
            pivot.longitude  == cell.longitude  and 
            pivot.azimuth == cell.azimuth and
            pivot.radius == cell.radius):
                cosector_list.append(cell)
                logging.debug("Adding cosector cell %s", cell.cell_name)
    return cosector_list;

def getEfficientyList(pivot, cosector_list):
    if not cosector_list:
        return (0,0)
    round_clock = defaultdict(list)
    #round_clock = RoundClock.objects.filter(cell_name=pivot.cell_name)
    efficiency = {}
    for cosectorcell in cosector_list:
        logging.debug("Filtering round clock for cosector cell %s %s", cosectorcell.cell_name, pivot.cell_name)
        filterlist = RoundClock.objects.filter(cell_name=cosectorcell.cell_name)
        for listelem in filterlist:
            round_clock[cosectorcell.cell_name].append(listelem)
    for cell_name, rc_list in round_clock.iteritems():
        for rc in rc_list:
            try:
                efficiency[rc.hour].density += rc.density
                efficiency[rc.hour].cell_list.append(CellState(rc.density, rc.cell_name, cellState.CELL_ON))
                logging.debug("Adding density %d to efficiency list at %d hour", rc.density, rc.hour)
            except:
                efficiency[rc.hour] = Efficiency()
                efficiency[rc.hour].density = rc.density
                efficiency[rc.hour].cell_list.append(CellState(rc.density, rc.cell_name, cellState.CELL_ON))
                logging.debug("Adding density %d to efficiency list at %d hour", rc.density, rc.hour)
        try:
            sorted(efficiency[rc.hour].cell_list,  key=lambda x:x[0])
        except:
            continue
    return round_clock,efficiency

def processEfficiency(round_clock, efficienty_list):
    for hour,efficiency in efficienty_list.iteritems():
        count = len(efficiency.cell_list)
        logging.debug("Efficiency at %d is %d", hour, efficiency.density)
        capacity_av = (CELL_MAX_CAPACITY*count)-efficiency.density
        density = efficiency.density
        debt = 0
        for idx, cell_state in enumerate(efficiency.cell_list):
            diff = CELL_MAX_CAPACITY - cell_state.density;
            if capacity_av > diff:
                efficiency.cell_list[idx].state = cellState.CELL_OFF
                count -= 1
                capacity_av = capacity_av - CELL_MAX_CAPACITY - cell_state.density
                logging.debug("Cell %s has been turned off", cell_state.cell_name)
            

def getNeighborEffciency(cell_name):
    if not cell_name:
        return;
    cell_list = CellInfo.objects.all()
    logging.debug("Getting efficiency for cell %s", cell_name)
    pivot = CellInfo.objects.get(cell_name=cell_name)
    cosector_list = getCoSectorCells(pivot, cell_list)
    round_clock, efficienty_list = getEfficientyList(pivot, cosector_list)
    if not round_clock:
        return
    processEfficiency(round_clock, efficienty_list)
    return cosector_list,efficienty_list

def efficiency_sched_chart(cosector_list):
    series = []
    for cell in cosector_list:
        series.append(cell.cell_name)
    elems = RoundClock.objects.filter(cell_name__in=['BGL10', 'BGL15'])
    print "Madhur here"
    print elems
    chart_elem = [{'options':{
                    'source':RoundClock.objects.filter(cell_name__in=series).extra(select={'hour_id':'CAST(hour AS UNSIGNED)'}).extra(order_by=['hour_id']),
                    'categories':'hour',
                    'legend_by':'cell_name'},
                    'terms': {
                    'density':Sum('density')}}]

    scheduleData = PivotDataPool(series = chart_elem)
    cht = PivotChart(
        datasource = scheduleData,
        series_options =
        [{'options':{
            'type': 'column',
            'stacking':True},
          'terms':['density']
                }],
        chart_options = 
          {'title': {
            'text': 'Schedule '},
            'xAxis': {
                'title':{
                    'text': 'Hourly Clock'}} })
    return cht;
