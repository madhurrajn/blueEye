from .models import CellInfo, CompareCell, busyHourDaily
from chartit import DataPool, Chart
import logging

    
logging.basicConfig(format='%(asctime)s {%(filename)s: %(lineno)d} %(funcName)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

def reArrangeSched(elem, cell_obj):
    clockdict = {}
    logging.info("Inside ReArrange")
    busyHourList = busyHourDaily.objects.filter(busyHour=cell_obj.cell_name)
    for hour in range(0,24):
        clockdict[hour] = (999, -1)
    for sched in busyHourList:
        for hour in range(sched.startHour, sched.endHour):
            clockdict[hour] = (sched.density, sched.id) 
    if elem:
        for hour in range(int(elem.startHour), int(elem.endHour)):
            clockdict[hour] = (sched.density, elem.id)
    minId = {}
    maxId = {}
    idlist = set()
    idlist.clear()
    newlist = set()
    newSchedlist = []
    currId = -1
    currMin = -1
    for hour in range(0,24):
        den,id = clockdict[hour]
        logging.debug("Clock Dict Density %d id %d", den, id)
        if id in idlist:
            logging.debug("Max Hour test currId %d, id %d", currId, id)
            if (currId != id) and currId not in newlist and currId != -1:
                logging.debug("Adding %d to found newlist maxHour to %d", currId, hour)
                maxId[currId] = hour
                newlist.add(currId)
        if (currId != id) and currId not in newlist and currId != -1:
            logging.debug("Adding %d to found newlist maxHour to %d", currId, hour)
            maxId[currId] = hour
            newlist.add(currId)
        if id not in idlist:
            logging.debug("Setting min Hour to %d id %d", hour, id)
            minId[id] = hour
            logging.debug("Adding %d to found idlist", id)
            idlist.add(id);
        if currId != id:
            if currMin == -1 and den == 999 and hour != 23:
                logging.debug("Inserting New Busyhour min %d", hour)
                sched = busyHourDaily()
                currMin = hour
                sched.startHour = hour
                newSchedlist.append(sched)
            else:
                if len(newSchedlist) > 0:
                    logging.debug("Finalizing New Busyhour max %d", hour)
                    sched = newSchedlist.pop()
                    if sched:
                        sched.endHour = hour
                        sched.busyHour = cell_obj
                        sched.density = 99
                        sched.save()
                        currMin = -1
        currId = id
    if len(newSchedlist) > 0:
        sched.endHour = 23
        sched.busyHour = cell_obj
        sched.density = 99
        sched.save()
    for sched in busyHourList:
        if sched.id in idlist:
            sched.startHour = minId[sched.id]
            sched.endHour = maxId[sched.id]
            sched.save()
            logging.debug(" id %d starthour %d endhour %d density %d", sched.id, sched.startHour, sched.endHour, sched.density)
    for sched in busyHourList:
        if sched.id not in idlist:
            logging.error("Deleting sched id %d", sched.id)
            sched.delete()


def schedule_chart(request):
    scheduleData = DataPool(\
                series = [{'options':{
                            'source':busyHourDaily.objects.all()},
                           'terms': [
                            'startHour',
                            'density']}
                          ])
    cht = Chart(
        datasource = scheduleData,
        series_options =
        [{'options':{
            'type': 'line',
            'stacking':False},
          'terms':{
            'startHour':[
                'density']
                }}],
        chart_options = 
          {'title': {
            'text': 'Schedule '},
            'xAxis': {
                'title':{
                    'text': 'Hourly Clock'}}})
    return cht;
