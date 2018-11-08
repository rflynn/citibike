#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                   [2, 0], [2, 1], [2, 2]])
points = [(10.2, 5.1), (4.7, 2.2), (5.3, 5.7), (2.7, 5.3)]
from scipy.spatial import Voronoi, voronoi_plot_2d
vor1 = Voronoi(points)
vor1.vertices


# In[2]:


vor1.regions


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
fig = voronoi_plot_2d(vor1)
plt.show()


# In[4]:


help(voronoi_plot_2d)


# In[5]:


import psycopg2
connstr = 'host=localhost port=5432 dbname=citibike user=postgres password=password'
conn = psycopg2.connect(connstr)
c = conn.cursor()
c.execute('''
select
    station_id,
    name,
    ARRAY[coord_long, coord_lat]
from citibike_station_status s
where last_reported = (select max(last_reported)
                       from citibike_station_status
                       where station_id=s.station_id)
and installed  -- not 'Coming Soon'
order by station_id
''')
from collections import OrderedDict
stations = list(c.fetchall())
Stations = OrderedDict()
for st in stations:
    Stations[st[0]] = {
        'id': st[0],
        'name': st[1],
        'coords': tuple(st[2])
    }
points = [v['coords'] for _k, v in Stations.items()]
stations[0], points[0]


# In[6]:


assert len(stations) == len(Stations)


# In[7]:


stations[153]


# In[8]:


vor = Voronoi(points)
vor.vertices


# In[9]:


vor.point_region[0:10]


# In[10]:


dir(vor)
help(vor)


# In[11]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
fig = voronoi_plot_2d(vor, show_vertices=False, line_width=0.25, point_size=0.5)
fig.set_size_inches((10, 10))
fig.set_dpi(220)
plt.tick_params(labelsize=3)
for i, (station_id, _name, (lng, lat)) in enumerate(stations):
    plt.text(lng, lat, station_id, fontsize=4,
             horizontalalignment='center',
             verticalalignment='center')
    if station_id == '523':
        plt.text(lng, lat, '*', fontsize=12, color='r',
         horizontalalignment='center',
         verticalalignment='center')

'''
lng9 = stations[120][-1][0]
lat9 = stations[120][-1][1]
plt.text(lng9, lat9, '*', fontsize=12, color='r',
         horizontalalignment='center',
         verticalalignment='center')
'''
'''
for i, (lng, lat) in enumerate(vor.vertices):
    if i in {105, 102, 101, 43, 42, 3, 1, 2, 0, -1, 104}:
        plt.text(lng, lat, i, fontsize=3,
                 horizontalalignment='center',
                 verticalalignment='center')
'''

# HOW DO I LIMIT THIS? ARGGGG
#plt.xlim(lng9 - 0.005, lng9 + 0.005)
#plt.ylim(lat9 - 0.005, lat9 + 0.005)
#plt.axis([lng9 - 0.025, lng9 + 0.025,
#          lat9 - 0.025, lat9 + 0.025])

import datetime
ts = datetime.datetime.now()
tsstr = ts.strftime('%Y-%m-%d-%H-%M-%S')
savepath = '/Users/rf/src/citibike/analysis/voronoi/voronoi-stations-{}.svg'.format(tsstr)
# options reduce whitespace
plt.savefig(savepath, format='svg', dpi=220, bbox_inches='tight', pad_inches=0)
print('done')
#plt.show()


# In[12]:


vor.vertices


# In[13]:


vor.ridge_points


# In[14]:


c.execute('''
with x as (
select csi.station_id, max(csi.last_reported) as last_reported
from citibike_station_inventory csi
where csi.station_id in %s
group by csi.station_id
)
select
    x.station_id,
    bikes_available
from citibike_station_inventory c
join x on x.station_id=c.station_id
and c.last_reported=x.last_reported
order by x.station_id
''', (tuple(Stations.keys()),))
StationBikesAvailable = dict(c.fetchall())
StationBikesAvailable


# In[34]:


c.execute('''select distinct nname from station_neighborhoods order by nname''')
Neighborhoods = list(name for name, in c.fetchall())
#print('Neighborhoods', len(Neighborhoods), Neighborhoods)
c.execute('''
select name,
regexp_split_to_array(substr(shape::text, 3, length(shape::text)-4), E'[(),]+')::float[]
from neighborhood
where name in %s
''', (tuple(Neighborhoods),))
NeighborhoodShapes = dict((name, list(zip(n[::2], n[1::2]))) for name, n in c.fetchall())
#print('NeighborhoodShapes', len(NeighborhoodShapes), list(NeighborhoodShapes.keys()))
missing = set(Neighborhoods) - set(NeighborhoodShapes.keys())
print('missing', missing)
assert missing == {}


# In[51]:


import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt

#constructing the first rect as a polygon
#r1 = sg.Polygon(NeighborhoodShapes['Park Slope'])

#a shortcut for constructing a rectangular polygon
#r2 = sg.box(0.5,0.5,1.5,1.5)
#r2 = sg.Polygon(NeighborhoodShapes['Sunnyside'])

#cascaded union can work on a list of shapes
#new_shape = so.cascaded_union([r1,r2])

#exterior coordinates split into two arrays, xs and ys
# which is how matplotlib will need for plotting
#print(dir(new_shape))
#xs, ys = new_shape.xy

NeighborhoodShapesPatches = [Polygon(shape, True, color='none') for _name, shape in NeighborhoodShapes.items()]
print(len(NeighborhoodShapesPatches))
p = PatchCollection(NeighborhoodShapesPatches, alpha=1.)

#plot it
plt.clf()
fig, ax = plt.subplots()
#axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')
ax.add_collection(p)
fig.set_size_inches((5, 5))
fig.set_dpi(220)
plt.axis([xmin, xmax, 
          ymin, ymax])
plt.tick_params(labelsize=3)
plt.box(False)

'''
ts = datetime.datetime.now()
tsstr = ts.strftime('%Y-%m-%d-%H-%M-%S')
savepath = '/Users/rf/src/citibike/analysis/voronoi/neighborhoods-{}.svg'.format(tsstr)
# options reduce whitespace
plt.savefig(savepath, format='svg', dpi=220, bbox_inches='tight', pad_inches=0)
'''

plt.show() #if not interactive


# In[109]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

plt.clf()
fig, ax = plt.subplots()

xmin = vor.points[:, 0].min()
xmax = vor.points[:, 0].max()
ymin = vor.points[:, 1].min()
ymax = vor.points[:, 1].max()
xc = xmin + ((xmax - xmin) / 2)
yc = ymin + ((ymax - ymin) / 2)

#ax.plot((xc, xc), (ymin, ymax), 'k', lw=0.5)
#ax.plot((xmin, xmax), (yc, yc), 'k', lw=0.5)

import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

patches = []
bikes_available = []
for i, (st, pt) in enumerate(zip(stations, vor.points)):
    # print(i, st, pt)
    pr = vor.point_region[i]
    r = vor.regions[pr]
    ba = StationBikesAvailable[st[0]]
    bikes_available.append(ba)
    if -1 not in r:
        region_points = [vor.vertices[vi] for vi in r]
        polygon = Polygon(region_points, True, color=None, fill=True, url=None)
        patches.append(polygon)
    else:
        polygon = Polygon([(0,0),(1,1),(0,1)])  # FIXME: XXX: fake placeholders
        patches.append(polygon)

clist = ['red', 'red', 'goldenrod', 'green', 'darkgreen']
cmap = matplotlib.colors.ListedColormap(clist)


colors = [1 if ba == 0 else 2 if ba < 4 else 3  # map bike cnt to [red,yellow,green] index
          for i, (p, ba) in enumerate(zip(patches, bikes_available))]
p = PatchCollection(patches, alpha=0.3, cmap=cmap)
p.set_array(np.array(colors))
c = ax.add_collection(p)



# apply clip paths...
'''
from descartes import PolygonPatch
from shapely.geometry import LineString
#for nsp in NeighborhoodShapesPatches:
#    plt.axes().add_artist(nsp)
#from matplotlib.patches import Circle
#testclip = Circle((-74., 40.74), 0.02, color='none')
#plt.axes().add_artist(testclip)
for (regionpatch, pt) in zip(patches, vor.points):
    #plt.axes().add_artist(regionpatch)
    print(regionpatch.xy)
    xy = LineString(regionpatch.xy)
    x, y = xy.xy
    ax.plot(x, y)
    print('xy', xy)
    ring_patch = PolygonPatch(xy)
    x = ax.add_patch(ring_patch)
    for nsp in NeighborhoodShapesPatches:
        if nsp.get_path().contains_point(pt):
            #sh = ax.plot(regionpatch.xy)
            #sh = ax.add_patch(regionpatch)
            #regionpatch.set_clip_path(nsp)
            x.set_clip_path(nsp)
            break
'''
from descartes import PolygonPatch
import shapely.geometry as sg
import shapely.ops as so
xys = [[(x,y) for (x,y) in p.xy] for p in NeighborhoodShapesPatches]
for i, coords in enumerate(xys):
    if len(coords) < 3:
        print('xys < 3!', i, coords)
#help(sg.Polygon)
polys = [sg.Polygon(coords) for coords in xys]
all_neighborhoods = so.cascaded_union(polys)
npp = PolygonPatch(all_neighborhoods, color='none')  # used as a mask, not displayed
ax.add_patch(npp)  # neat!
for col in ax.collections:
    col.set_clip_path(npp)
#print(dir(npp))
#xys2 = [[(x,y) for (x,y) in p.xy] for p in npp]
#ax.plot(xys2)
#c.set_clip_path(npp)  # displays nothing...
#p.set_clip_path(npp)  # displays nothing...
#ax.set_clip_path(npp)  # runs but does nothing
#for p in patches:
#    p.set_clip_path(npp)
#ax.set_clip_path(ring_patch)
#x = ax.add_patch(ring_patch)
#x.set_clip_path(nsp)


def complement_slope(s):
    return -1. / (s if s != 0 else 0.00001)

for i, (rv0, rv1) in enumerate(vor.ridge_vertices):
    if rv0 != -1 and rv1 != -1:
        x0, y0 = vor.vertices[rv0]
        x1, y1 = vor.vertices[rv1]
        ax.plot((x0, x1), (y0, y1), 'k-', lw=0.1, alpha=0.5)
    else:
        # print(rv0, rv1)
        # ensure -1 always in rv0
        if rv0 != -1 and rv1 == -1:
            rv0, rv1 = rv1, rv0
        x0, y0 = None, None
        x1, y1 = vor.vertices[rv1]
        #ax.scatter(x1, y1, s=2, facecolor='yellow')
        is_top = y1 >= yc
        is_left = x1 <= xc
        rp0, rp1 = vor.ridge_points[i]
        p0 = vor.points[rp0]
        px0, py0 = p0
        #ax.scatter(px0, py0, s=2, facecolor='r')
        p1 = vor.points[rp1]
        px1, py1 = p1
        #ax.scatter(px1, py1, s=2, facecolor='r')
        dx = px0 - px1
        dy = py0 - py1
        s = dy / dx
        sc = complement_slope(s)
        #print(s, sc)
        # distance to extrapolate our next point
        dist = max(xmax - xmin, ymax - ymin)
        if is_left:
            x0 = x1 - dist
            if is_top:
                y0 = y1 - (sc * dist)
            else:
                y0 = y1 + (-sc * dist)
        else:
            x0 = x1 + dist
            if is_top:
                y0 = y1 + (abs(sc) * dist)
            else:
                y0 = y1 - (abs(sc) * dist)
        # x2 = x1 - 1.
        # y2 = y1 - (sc * 1.)
        ax.plot((x0, x1), (y0, y1), 'k-', lw=0.25, linestyle='--')

# ax.scatter(vor.vertices[:, 0], vor.vertices[:, 1], s=0.1, facecolor='gray')
# ax.scatter(vor.points[:, 0], vor.points[:, 1], s=0.05, alpha=0.5, facecolor='xkcd:cerulean')

# label station with their value
for (x, y), ba in zip(vor.points, bikes_available):
    ax.text(x, y, ba, fontsize=5,
            horizontalalignment='center',
            verticalalignment='center')

fig.set_size_inches((10, 10))
fig.set_dpi(220)
plt.axis([xmin - ((xmax - xmin) / 200.), xmax + ((xmax - xmin) / 200.), 
          ymin - ((ymax - ymin) / 200.), ymax + ((ymax - ymin) / 200.)])
plt.tick_params(labelsize=3)
plt.box(False)

ts = datetime.datetime.now()
tsstr = ts.strftime('%Y-%m-%d-%H-%M-%S')
savepath = '/Users/rf/src/citibike/analysis/voronoi/voronoi-stations-scratch-{}.svg'.format(tsstr)
# options reduce whitespace
plt.savefig(savepath, format='svg', dpi=220, bbox_inches='tight', pad_inches=0)

plt.show()


# In[16]:


def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


# In[17]:


sorted(list(enumerate(vor.regions)), key=lambda x: len(x[1]), reverse=True)
len(vor.regions)


# In[18]:


share_vertex = [set() for _ in vor.vertices]
for i, region in enumerate(vor.regions):
    for vertex in region:
        if vertex > -1:
            share_vertex[vertex].add(i)
share_vertex[0:10]


# In[19]:


Neighbors = [set() for _ in vor.regions]
for i, region in enumerate(vor.regions):
    for vertex in region:
        Neighbors[i] |= share_vertex[vertex]
    if Neighbors[i]:
        Neighbors[i].remove(i)  # remove self-reference
    assert i not in Neighbors[i]
assert len(Neighbors) == len(stations) + 1
# sorted(neighbors, key=lambda x: len(x), reverse=True)
# sorted(list(enumerate(neighbors)), key=lambda x: len(x[1]), reverse=True)[0:10]
Neighbors[0:12]


# In[20]:


len(Neighbors)


# In[21]:


vor.point_region[86]


# In[22]:


spr = set(vor.point_region)
print(len(vor.point_region), len(spr))


# In[23]:


# reverse mapping -- needed for neighbors
region_point = {vor.point_region[i]: i for i, _s in enumerate(stations)}
len(region_point)


# In[24]:


station_id_neighbors = dict()
try:
    assert len(Neighbors) == len(stations) + 1
except AssertionError:
    print(len(Neighbors), len(stations) + 1)
    raise
for i, (st, pt) in enumerate(zip(stations, vor.points)):
    # print(i, st, pt)
    try:
        assert st[0] not in station_id_neighbors
    except AssertionError:
        pprint(station_id_neighbors)
        raise
    pr = vor.point_region[i]
    myneighbors = Neighbors[pr]
    # print(i, pr, st, pt)
    neighbor_ids = []
    for neighbor in myneighbors:
        npr = region_point[neighbor]
        stx = stations[npr]
        neighbor_ids.append(stx[0])
        # print(' neighbor:', neighbor, npr, st)
    station_id_neighbors[st[0]] = sorted(neighbor_ids)

print('len(station_id_neighbors)', len(station_id_neighbors))
assert len(station_id_neighbors) == len(stations)

import json
print(json.dumps(station_id_neighbors))
savepath = '/Users/rf/src/citibike/analysis/voronoi/voronoi-neighbors-{}.json'.format(tsstr)
with open(savepath, 'w') as jf:
    json.dump(station_id_neighbors, jf)
len(station_id_neighbors)


# In[25]:


'''
TODO: XXX: stations shouldn't be considered neighbors unless
1) they're in the same borough (Brooklyn/Queens exception(?))
2) they're within walking distance of each other

also -- we should save the station network configuration that resulted in this
adjacency configuration; it'll be used for caching (and debugging)
'''
import networkx as nx
G = nx.Graph()
# help(G.add_node)
for st in stations:
    st_id, name, (long, lat) = st
    G.add_node(st_id, name=name, long=long, lat=lat, bikes_available=StationBikesAvailable[st_id])
for st in stations:
    st_id, _name, (_long, _lat) = st
    neighbors = station_id_neighbors[st_id]
    for neighbor_id in neighbors:
        G.add_edge(st_id, neighbor_id)
print(G['119'])
print(G.node['119']['bikes_available'])
print(G['119']['144'])
neighbor_nodes = list(G.neighbors('119'))
print(neighbor_nodes) 
ba_sum_neighbors = sum(G.node[k]['bikes_available'] for k in G.neighbors('119'))
print('ba_sum_neighbors', ba_sum_neighbors)
#print(dir(G['119'].items()))
# edges are reciprocal
assert G['119']['144'] == G['144']['119']
#print(G.nodes.data())


# In[26]:


StationConfig = {'stations': {stid: {'coords': st['coords']} for stid, st in Stations.items()}}
# NOTE: long/lat must be numeric/Decimal type; must match exactly;
# if a station is added, removed or moves we recalculate adjacency
StationConfig


# In[27]:


nx.clustering(G)
list(nx.connected_components(G))
sorted((d, n) for n, d in G.degree())


# In[28]:


nx.draw(G, with_labels=True, font_weight='bold')
plt.show()


# In[ ]:




