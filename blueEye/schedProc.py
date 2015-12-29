
    
def reArrangeSched(elem,  busyHourList):
    for sched in busyHourList:
        print "Hello1"
        print sched.id
        print elem.id
        print elem.startHour
        print elem.endHour
        print sched.startHour
        print sched.endHour
        if sched.id == elem.id:
            continue
        if (elem.startHour > sched.startHour):
            if(elem.startHour < sched.endHour):
                if(elem.endHour > sched.startHour):
                    if(elem.endHour < sched.endHour):
                        sched.delete()
        if (sched.startHour < elem.startHour):
            print "HEre1"
            print elem.startHour
            print sched.startHour
            if (sched.endHour > elem.startHour):
                sched.endHour = elem.startHour
                sched.save()
                print "Here 4"
                print sched.startHour
                print sched.endHour
        if (sched.startHour < elem.endHour ):
            print "Here 2"
            if (elem.endHour < sched.endHour):
                print "Here 3"
                sched.startHour = elem.endHour
                sched.save()
                print sched.startHour
                print sched.endHour
