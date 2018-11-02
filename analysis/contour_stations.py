#%matplotlib inline

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.image as mpimg
from PIL import Image
import skimage

import psycopg2
connstr = 'host=localhost port=5432 dbname=citibike user=postgres password=password'
conn = psycopg2.connect(connstr)
c = conn.cursor()
c.execute('''
select
    station_id,
    coords_longlat::float[2] -- must cast to make numpy dtypes happy
from citibike_station
order by station_id
-- limit 30 offset 180
''')
stations = list(c.fetchall())
station_ids = [i for i, _ll in stations]
p = np.c_[[ll for i,ll in stations]]
print('p.shape', p.shape)
px = p[:, 0]
print('px.shape', px.shape)
py = p[:, 1]
print('py.shape', py.shape)

delta = 0.0001
xmin, xmax = px.min(), px.max()
ymin, ymax = py.min(), py.max()
x = np.arange(xmin, xmax, delta)
y = np.arange(ymin, ymax, delta)
print('x.shape={} y.shape={}'.format(x.shape, y.shape))
X, Y = np.meshgrid(x, y)
print('X.shape={} Y.shape={}'.format(X.shape, Y.shape))

c.execute('''
with x as (
select station_id, max(last_reported) as last_reported
from citibike_station_inventory
where station_id in %s
group by station_id
)
select
    x.station_id,
    bikes_available
from citibike_station_inventory c
join x on x.station_id=c.station_id
and c.last_reported=x.last_reported
order by x.station_id
''', (tuple(station_ids),))
available = list(c.fetchall())
f = np.array([a for st,a in available])
print('f.shape', f.shape)
#Y = [0] * 400 + [1] * 417
#print('Y', Y)

fig, ax = plt.subplots(nrows=1, ncols=1)
fig.set_size_inches((11, 12))
fig.set_dpi(110)
mapimgpath = '/Users/rf/src/citibike/analysis/nyc-bw.png'
# mapimg = mpimg.imread(mapimgpath)
mapimg = np.asarray(Image.open(mapimgpath).convert('L'))  # grayscale
print('mapimg', mapimg.shape, mapimg.dtype)

extent = xmin, xmax, ymin, ymax
#mapimgplot = ax.imshow(mapimg, alpha=0.2,
#                       cmap='gray',
#                       extent=extent)


maskimgpath = '/Users/rf/src/citibike/analysis/nyc-bw-mask.png'
#maskimg = plt.imread(maskimgpath)
maskimg = np.asarray(Image.open(maskimgpath))
print('maskimg', maskimg.shape, maskimg.dtype, maskimg[0])

#maskimg = maskimg.astype(np.bool)
print('maskimg', maskimg.shape, maskimg.dtype,
      np.histogram(maskimg, bins=[False,False]),
      np.histogram(maskimg, bins=[True,True]))

print('maskimg 0/1 shape', maskimg[:,0].shape, maskimg[:,1].shape)


#mapimgmasked = np.ma.array(mapimg, mask=maskimg)
#print('mapimgmasked', mapimgmasked)


Ti = griddata((px, py), f, (X, Y), method='nearest')
print('Ti.shape', Ti.shape)

maskimg = np.invert(maskimg.astype(bool)[::-1])
maskimg2 = skimage.transform.resize(maskimg, X.shape)
print('maskimg2', maskimg2.shape, maskimg2)

Ti2 = np.ma.array(Ti, mask=maskimg2)

#r, c = (i+1) // 2, (i+1) % 2
cn = ax.contourf(X, Y, Ti2,
                 alpha=0.3,
                 levels=[-0.5,0.5,4.5,9999],
                 colors=['red', 'goldenrod', '#009900'])
#fig.colorbar(cn, ax=ax)
'''
cn = ax.contourf(X, Y, Ti,
                 levels=[-1.5,0.5,4.5],
                 colors=['red','#CCFFCC'],
                 alpha=0.3)
#ax.clabel(cn, inline=True, fmt='%.0f', fontsize=10)
'''
cn = ax.contour(X, Y, Ti2, alpha=0.35,
                levels=[-0.5,0.5,4.5,9999],
                colors=['red', 'goldenrod', '#009900'],
                linewidths=0.5)

#ax.scatter(px, py, c='k', alpha=0.1, marker='.')
#maskimgplot = ax.imshow(maskimg, alpha=1.,
#                        cmap='gray',
#                        extent=extent)


for x0, y0, z0 in zip(px, py, f):
    ax.text(x0, y0, z0, fontsize=6,
            horizontalalignment='center',
            verticalalignment='center')
#ax.set_title('method = {}'.format(method))


def get_contour_verts(cn):
    contours = []
    # for each contour line
    print('collections', len(cn.collections))
    for cc in cn.collections:
        paths = []
        # for each separate section of the contour line
        print('paths', len(cc.get_paths()))
        for pp in cc.get_paths():
            xy = []
            # for each segment of that section
            for vv in pp.iter_segments():
                xy.append(vv[0])
            paths.append(np.vstack(xy))
        print('paths', len(paths))
        contours.append(paths)
    print('contours', len(contours))
    return contours    

#print('contours', get_contour_verts(cn)[0])

plt.show()
