import vcs, cdms2

dataset = cdms2.open(vcs.sample_data + "/clt.nc")
clt = dataset('clt')

timeaxis = clt.getTime()
for row in timeaxis:
    print row
lataxis = clt.getLatitude()
lonaxis = clt.getLongitude()

# So, if we want to know where a given point is...
lat_index = 24
lon_index = 50
time_index = 60

# This is the module for easy use of time axis values
import cdtime

print 'Value:', clt[time_index][lat_index][lon_index]
# Times are stored as "relative times", or "time since X date"
relative_time = cdtime.relativetime(timeaxis[time_index], timeaxis.units)
# Component time is a more useful format, that has the date/time in human-readable attributes
print "Time:", relative_time.tocomponent()
print "Lat:", lataxis[lat_index]
print "Lon:", lonaxis[lon_index]

# Now we can plot clt at the specified time, and stick a marker at the lat/lon
x = vcs.init()

template = x.createtemplate()
template.scale(.66, "x")
template.blank()
template.data.priority = 1

x.plot(clt(time=time_index), template)

marker = vcs.createmarker()
marker.type = "cross"

# data describes where the actual plot is placed on the canvas
data = template.data

# Viewport represents the area in which markers are drawn
marker.viewport = (data.x1, data.x2, data.y1, data.y2)
# Worldcoordinate represents the scale that x/y are given in
marker.worldcoordinate = (min(lonaxis), max(lonaxis), min(lataxis), max(lataxis))
marker.x = [lonaxis[lon_index]]
marker.y = [lataxis[lat_index]]
marker.size = 10
x.plot(marker)

murica = clt(time=time_index, latitude=(12, 80), longitude=(-150, -40))
templ_2 = x.createtemplate()
templ_2.scale(.33, "x")
templ_2.scale(.5, "y")
templ_2.move(.63, "x")
templ_2.move(.4, "y")
templ_2.blank()
templ_2.data.priority = 1
x.plot(murica, templ_2)

marker2 = vcs.createmarker()
marker2.type = "cross"
marker2.viewport = (templ_2.data.x1, templ_2.data.x2, templ_2.data.y1, templ_2.data.y2)

murica_lat = murica.getLatitude()
murica_lon = murica.getLongitude()

marker2.worldcoordinate = (min(murica_lon), max(murica_lon), min(murica_lat), max(murica_lat))
marker2.y = [37.6819]
marker2.x = [-121.7681]
marker2.size = 20

text = vcs.createtext()
text.string = ["You are here"]
text.viewport = marker2.viewport
text.worldcoordinate = marker2.worldcoordinate
text.x = [-121.7681]
text.y = [37.6819]
text.height = 8

x.plot(marker2)
x.plot(text)

raw_input("enter")