from matplotlib import pyplot
from matplotlib.patches import Circle
from shapely.geometry import Polygon, Point
from descartes.patch import PolygonPatch
from .models import CellInfo, CompareCell
import math
import geopy
from geopy.distance import VincentyDistance
import logging

logging.basicConfig(format='%(asctime)s {%(filename)s: %(lineno)d} %(funcName)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

#from figures import SIZE

COLOR = {
    True:  '#6699cc',
    False: '#ff3333'
    }

SampleCellData = [
    ["Cell1", -3.68003, 42.36526, 150, 65, 15],
    ["Cell2", -3.689498889, 42.33775583, 150, 65, 15]
]

cells_g = {}

class Cell(object):
    def __init__(self, name, lat, long, azimuth, bw, radius, uarfcn, workingRadius):
        self.name = name
        self.lat  = lat
        self.long = long
        self.azimuth = azimuth
        self.bw = bw
        self.radius = workingRadius 
        self.geo = Geometry(self)
        self.uarfcn = uarfcn
        self.actualRadius = radius
        self.cosectors = {}
        self.cosectorsId = -1
        self.normalCell = True

class Geometry(object):
    def __init__(self, cell):
        self.cell = cell
        cell.geo = self
        self.poly_lines = 16 
        self.edgeL = 0.0
        self.edgeR = 0.0
        self.geo_polygon = list()

    def getOriginLatLong(self):
        cellitems = list(cells_g)
        return (math.radians(cells_g[cellitems[0]].lat), math.radians(cells_g[cellitems[0]].long))

    def get_distance_from_origin(self):
        '''
        Using Haversine formula
        '''
        radius_of_earth = 6371
        latR = math.radians(self.cell.lat)
        lonR = math.radians(self.cell.long)
        originlatR, originlongR = self.getOriginLatLong()
        deltaLon = lonR - originlongR
        deltaLat = latR - originlatR
        a = math.sin(deltaLat/ 2) ** 2 + math.cos(originlatR) * math.cos(latR) * math.sin(deltaLon/2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        dist = radius_of_earth * c
        '''
        Reference
        http://www.movable-type.co.uk/scripts/latlong.html
        '''
        y = math.sin(deltaLon) * math.cos(latR)
        x = math.cos(originlatR) * math.sin(latR) - math.sin(originlatR) * math.cos(latR) * math.cos(deltaLon)
        brng = math.degrees(math.atan2(y, x)) % 360

        return dist,brng

    def get_coordinates(self):
        cellitems = list(cells_g)
        if self.cell.name == cellitems[0]:
            #print 0,0
            return 0,0
        else:
            dist,brng = self.get_distance_from_origin()
            rfx = math.radians((90-brng) % 360)
            return ( dist*math.cos(rfx), dist*math.sin(rfx))

    def get_cone_edges(self, azimuth, beamwidth):
        half_sector = float(beamwidth)/2
        left_edge = (azimuth-half_sector) % 360
        right_edge = (azimuth+half_sector) % 360
        return(left_edge, right_edge)

    def create_polygon(self):
        center = (self.x, self.y)
        polygon_vertex = [(self.x, self.y)]
        step = float(self.cell.bw)/self.poly_lines
        self.geo_polygon.append((self.cell.lat, self.cell.long))
        for i in range(self.poly_lines + 1):
            angle_from_x = ( (self.edgeR - step*i)) % 360
            angle_from_y = (90 - self.edgeR - step*i) % 360
            yrad = math.radians(angle_from_y)
            xrad = math.radians(angle_from_x)
            polygon_vertex.append(((self.x + math.cos(xrad) * self.cell.radius),
                                      (self.y + math.sin(xrad) * self.cell.radius)))
            origin = geopy.Point(self.cell.lat, self.cell.long)
            dest = VincentyDistance(kilometers=self.cell.radius).destination(origin, angle_from_x)
            self.geo_polygon.append((dest.latitude, dest.longitude))
        #self.geo_polygon.append((self.cell.lat, self.cell.long))
        #for lat,long in self.geo_polygon:
        #    print lat, long
        #    print "Latitude"    

        polygon1 = Polygon(polygon_vertex)
        self.polygon = polygon1
        for delta in (0, 0.01, -0.01):
            self.polygon = polygon1.union(Point(center).buffer(0.6 + delta))
            if self.polygon.is_valid:
                break;

    def generate_beam_form(self):
        if len(cells_g) == 0:
            print len(cells_g)
            print "Returning without processing"
            return
        self.x,self.y =  self.get_coordinates()
        #print self.x,self.y
        if self.cell.normalCell == False:
            leng = len(self.cell.cosectors)
            left = (self.cell.azimuth - (self.cell.bw/2))%360
            self.cell.bw = self.cell.bw/(leng+1)
            self.cell.azimuth = left + ((self.cell.bw)*(self.cell.cosectorsId))
            self.cell.azimuth = self.cell.azimuth
        self.edgeL, self.edgeR = self.get_cone_edges(self.cell.azimuth, self.cell.bw)
        self.create_polygon()
        #print self.polygon

def getkey1(item):
    return item[1]

class Plotter:
    def __init__(self):
        self.fig = pyplot.figure(1,figsize=(40,5), dpi=90)
        self.xrange = [-15, 15]
        self.yrange = [-15, 15 ]
        self.polygons = []
        self.ext = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        self.subplotter()

    def subplotter(self):
        self.ax = self.fig.add_subplot(121)
        self.ax.set_title('Cell Cone')
        self.ax.set_xlim(*(self.xrange))
        self.ax.set_xticks(range(*self.xrange) + [self.xrange[-1]])
        self.ax.set_ylim(*self.yrange)
        self.ax.set_yticks(range(*self.yrange) + [self.yrange[-1]])
        self.ax.set_aspect(1)

    def addtosubplot(self, polygon):
        x,y = polygon.xy
        self.ax.plot(x,y, 'o', color='#FF9999', zorder = 1)

    def plotCoords(self, vertexlist):
        #for polygon in self.polygons:
        #   self.addtosubplot(polygon.interiors)
        #self.addtosubplot(self.polygon.interiors[0])
        #self.addtosubplot(self.polygon.interiors[1])
        #self.addtosubplot(self.polygon.exterior)
        self.addtosubplot(vertexlist)

    def plotterColor(self, ob):
        return COLOR[ob.is_valid]

    def updateCellsToPlot(self):
        for key,cell in cells_g.items():
            self.plotCoords(cell.geo.polygon.exterior)

    def display(self):
        pyplot.xlim(5,40)
        pyplot.show()

def updateCoSectors(cell_list):
    for key,cell in cell_list.iteritems():
        cell.cosectors.clear()
        for key,cell2 in cell_list.iteritems():
            if cell.name == cell2.name:
                continue;
            else:
                if (cell.lat == cell2.lat and
                    cell.long == cell2.long and
                    cell.azimuth == cell2.azimuth):
                        cell.cosectors[str(cell2.name)] = cell2
                        cell.normalCell = False
        if cell.cosectorsId == -1:
            print "Test Cell :"+str(cell.name)
            cosectorId = 2
            cell.cosectorsId = 1
            for key, cell3 in cell.cosectors.iteritems():
                print "Cosector Cell"+str(cell3.name)
                if cell3.cosectorsId == -1 :
                    cell3.cosectorsId = cosectorId
                    cosectorId = cosectorId + 1

def getCellBeamForm(compare):
    cell_list = CellInfo.objects.all()
    compare_list = CompareCell.objects.all()
    cells_g.clear()
    for cell in cell_list:
        found = False
        for cl in compare_list:
            if cl.cell_name == cell.cell_name:
                print "Cell Found"+cl.cell_name
                found = True
                if compare == True:
                    print "Compare Cells getting added"
                    cells_g[str(cell.cell_name)]=Cell(cell.cell_name, cell.lattitude, cell.longitude, cell.azimuth, cell.beamwidth, cell.radius, cell.uarfcn, cell.radius)
        if found == False:
            if compare == False:
                print "Normal Cells getting Added"
                cells_g[str(cell.cell_name)]=Cell(cell.cell_name, cell.lattitude, cell.longitude, cell.azimuth, cell.beamwidth, cell.radius, cell.uarfcn, 0.3)
    updateCoSectors(cells_g)
    for key,cell in cells_g.items():
        cell.geo.generate_beam_form()
    return cells_g;

def getNeighbors(cell_name):
    neighbor_list = []
    cell_list = CellInfo.objects.all()
    cells_g.clear()
    try:
        pivot = cells_g[cell_name]
    except:
        return(0,0)
    for cell in cell_list:
        cells_g[str(cell.cell_name)]=Cell(cell.cell_name, cell.lattitude, cell.longitude, cell.azimuth, cell.beamwidth, cell.radius, cell.uarfcn, cell.radius)
    pivot.geo.generate_beam_form()
    for key, cell in cells_g.items():
        if key == cell_name:
            continue
        else:
            cell.geo.generate_beam_form()
            if pivot.geo.polygon.intersects(cell.geo.polygon):
                logging.debug("Neighbor Cell %s intersection found", key)
                neighbor_list.append(cell)
            else:
                logging.debug("Neighbor Cell %s intersection not found", key)
    return (pivot, neighbor_list)

def readCellData():
    for data in SampleCellData:
        cells_g[str(data[0])]=Cell(data[0], data[1], data[2], data[3], data[4], data[5])
    for key,cell in cells_g.items():
        cell.geo.generate_beam_form()


#if __name__ == "__main__":
    #readCellData()
    #plotter = Plotter()
    #plotter.updateCellsToPlot()
    #plotter.display()

