#!/usr/bin/env python
# coding: utf-8

# 

# In[1]:


import numpy as np

def every_minute(ts_start, sparse):
    """given sparse input as [(ts, total),...] produce 'dense' result for every minute of the day"""
    d = np.array([-1] * (24 * 60), dtype=np.int8)
    eod = ts_start + (24 * 60 * 60)
    sparse2 = [(ts_start, sparse[0][1])] + sparse + [(eod, 0)]
    for ((ts1, c1), (ts2, _c2)) in zip(sparse2, sparse2[1:]):
        min1 = (ts1 - ts_start) // 60
        min2 = (ts2 - ts_start) // 60
        #print('ts_start={} min1={} min2={} c1={}'.format(ts_start, min1, min2, c1))
        #assert min1 >= 0
        #assert min2 >= min1
        #assert min2 <= 24 * 60
        d[min1:min2] = c1
    return d

every_minute(0, [(1, 1), (24*60*60-1, 2)])


# In[2]:


import psycopg2
#connstr = 'host=localhost port=5432 dbname=citibike user=postgres password=password'
connstr = 'host=mbp15.local port=5432 dbname=citibike user=postgres password=password'
conn = psycopg2.connect(connstr)

c = conn.cursor()
station_id = '3711'  # 'E 13 St & Avenue A', big deficit
#station_id = '3333'  # biggest surplus
#station_id = '3336'  # E 97 St & Madison Ave, defecit
q = c.mogrify("""
select
extract(epoch from (((timestamp 'epoch' + last_reported * interval '1 second') at time zone 'EDT' + interval '-9 hours')::date))::int as day_start,
extract(epoch from (((timestamp 'epoch' + last_reported * interval '1 second') at time zone 'EDT' + interval '-9 hours')))::int as last_reported,
bikes_available
from citibike_station_inventory
where station_id=%s
and last_reported >= extract(epoch from timestamp '2018-10-31' at time zone 'EDT')::int -- first full day
order by last_reported
""", (station_id,))
'''
q = c.mogrify("""
select
max(timestamp 'epoch' + last_reported * interval '1 second' - interval '4 hours')
from citibike_station_inventory
where station_id=%s
and last_reported >= 1540944000 + (4 * 60 * 60)  -- Oct 30th, first full day
""", (station_id,))
q = c.mogrify("""
select
count(*)
from citibike_station_inventory
where station_id=%s
and last_reported >= 1540944000 + (4 * 60 * 60)  -- Oct 31th, first full day
""", (station_id,))
'''

print(q.decode())
c.execute(q)
#print(list(c.fetchall()))

from collections import defaultdict
from itertools import groupby
import datetime
import pytz

StationDays = defaultdict(list)
TZNYC = pytz.timezone('America/New_York')
print('{:10s} {:10s} {:3s} {:3s} {:3s} {:3s} {:3s}'.format('ts', 'dt', 'sp', 'p99', 'p95', 'p90', 'p50'))
for day_start, day_rows in groupby(c.fetchall(), lambda x: x[0]):
    # day_rows = list(day_rows)
    sparse = [(ts, ba) for _ts_start, ts, ba in day_rows]
    ts = datetime.datetime.utcfromtimestamp(day_start)
    dt = ts.date()
    #dt = (ts + datetime.timedelta(hours=0)).date()
    #dt2 = ts.astimezone(TZNYC).date()
    dense = every_minute(day_start, sparse)
    p99 = np.percentile(dense, 99)
    p95 = np.percentile(dense, 95)
    p90 = np.percentile(dense, 90)
    p50 = np.percentile(dense, 50)
    print('{} {} {:3}  {:2.0f}  {:2.0f}  {:2.0f}  {:2.0f}'.format(
        day_start, dt, len(sparse), p99, p95, p90, p50))
    #print('sparse', sparse)
    #print('dense', dense)
    StationDays[station_id].append({
        'day_start': day_start,
        'dt': dt,
        #'day_rows': day_rows,
        'sparse': sparse,
        #'dense': dense,
    })
c.close()
conn.close()


# In[53]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
plt.clf()
plt.style.use('fivethirtyeight')
fig, _ax = plt.subplots(nrows=8, ncols=1, sharex=True, sharey=True, figsize=(4, 5))
#fig.set_size_inches((4, 2))
fig.set_dpi(220)
fig.suptitle('bikes_available over time', fontsize=8)
plt.xlabel('time', fontsize=6)
plt.ylabel('bikes_available', fontsize=6)
fig.subplots_adjust(hspace=0, wspace=0, left=0)
#plt.title('bikes_available over time at stations')
#plt.grid(True)
plt.rc('axes', axisbelow=True)
import matplotlib.collections as collections
ymin, ymax = float('inf'), float('-inf')

allx = [np.array([]) for _ in range(7)]
ally = [np.array([]) for _ in range(7)]

for day in StationDays[station_id]:
    sparse = day['sparse']
    day_start = day['day_start']
    spnp = np.array(sparse)
    x = spnp[:, 0]
    x -= day_start  # show relative time during the day
    #x = -x  # convert bikes_available to "demand"
    y = spnp[:, 1]
    #y -= y[0]  # relative to start of day...
    #y = y / 27  # percent capacity
    ymax = max(ymax, y.max())
    ymin = min(ymin, y.min())
    dow = day['dt'].weekday()
    allx[dow] = np.append(allx[dow], x)
    ally[dow] = np.append(ally[dow], y)
    label = day['dt'].strftime('%a %b %d')
    fig.axes[dow].plot(x, y, label=label, linewidth=0.5)
    if dow == 1 and label == 'Tue Nov 13':
        #collection = collections.BrokenBarHCollection.span_where(x, ymin=y.min(), ymax=y.max(), where=x >= 25000, facecolor='lightblue', alpha=0.5)
        #fig.axes[dow].add_collection(collection)
        fig.axes[dow].broken_barh([(25000, 10000)], (15, 26), facecolors='lightblue', alpha=0.3)

for dow in range(7):
    # plot best fit line...
    # ref: https://stackoverflow.com/questions/22239691/code-for-line-of-best-fit-of-a-scatter-plot-in-python
    x = allx[dow]
    ux = np.unique(x)
    y = ally[dow]
    #print('poly1d', np.poly1d(np.polyfit(x, y, 2))(ux))
    fig.axes[dow].plot(ux, np.poly1d(np.polyfit(x, y, 16))(ux), 'k', linewidth=0.5, linestyle='dotted')
    # display all
    fig.axes[7].plot(ux, np.poly1d(np.polyfit(x, y, 16))(ux), label=str(dow), linewidth=0.5)
    # mark 9am and 6pm
    fig.axes[dow].plot([9*60*60, 9*60*60], [ymin, ymax], 'gray', linewidth=0.5)
    fig.axes[dow].plot([18*60*60, 18*60*60], [ymin, ymax], 'gray', linewidth=0.5)
    # configure subplot style...
    fig.axes[dow].legend(loc='lower left', fontsize=4)
    fig.axes[dow].tick_params(labelsize=5)
    fig.axes[dow].locator_params(axis='x', nbins=24)
    fig.axes[dow].locator_params(axis='y', nbins=4)

fig.axes[7].legend(loc='lower left', fontsize=4)
fig.axes[i].axis('tight')
plt.tick_params(labelsize=5)
plt.xlim(0, 24*60*60)
plt.ylim(min(ymin * 1.10, -5), ymax * 1.10)
plt.show()


# In[ ]:





# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit


connstr = 'host=localhost port=5432 dbname=citibike user=postgres password=password'
conn = psycopg2.connect(connstr)
c = conn.cursor()
query = """
select
timestamp 'epoch' + last_reported * interval '1 second' - interval '4 hours' as last_reported,
-- last_reported,
bikes_available
from citibike_station_inventory
where station_id=%s
and last_reported >= 1540903456  -- fixup for some values of '1' for 'Coming Soon', and some erroneous values(?)
order by last_reported
"""

query = """
select
timestamp 'epoch' + (last_reported - (last_reported %% 60)) * interval '1 second' - interval '4 hours' as last_reported,
sum(bikes_available)
from citibike_station_inventory csi
where csi.station_id in (select station_id from station_neighborhood_borough where neighborhood=%s)
-- and last_reported >= 1540903456  -- fixup for some values of '1' for 'Coming Soon', and some erroneous values(?)
and last_reported >= extract(epoch from now() - interval '4 hours')::int
group by (last_reported - (last_reported %% 60))
order by (last_reported - (last_reported %% 60))
"""


# station_ids = ['517', '519']  # Pershing Square North/South
# station_ids = ['127', '128']  # Barrow St & Hudson St / MacDougal St & Prince St
"""
c.execute('''
with x as (
    select station_id, count(*) as cnt
    from citibike_station_inventory
    group by station_id
)
select s.station_id, s.name
from citibike_station s
join x using (station_id)
order by x.cnt desc
limit 800 -- 2^16 pixel size limit :-P
''')

c.execute('''
select station_id, name
from citibike_station_inventory_magnitude m
join citibike_station s using (station_id)
join station_neighborhood_borough snb using (station_id)
order by m.sum desc;
''')
"""


c.execute('''
select snb.neighborhood, sum(csi.bikes_available) as sum
from citibike_station_inventory csi
join station_neighborhood_borough snb using (station_id)
group by snb.neighborhood
order by sum(csi.bikes_available) desc
''')

# stations = list(c.fetchall())
neighborhoods = list(c.fetchall())

plt.close('all')
#plt.figure(figsize=(10, 1000), dpi=180)
#f, _axes = plt.subplots(nrows=(len(stations)+3)//4, ncols=4, sharex=True, sharey=True)
#f.set_size_inches((12, len(stations)*0.7/4))
f, _axes = plt.subplots(nrows=len(neighborhoods), ncols=1, sharex=False, sharey=True)
f.set_size_inches((12, (len(neighborhoods)+1)//2))
f.set_dpi(220)
f.subplots_adjust(hspace=0, wspace=0, left=0)
plt.xlabel('time')
plt.ylabel('bikes_available')
#plt.title('bikes_available over time at stations')
plt.grid(True)
plt.rc('axes', axisbelow=True)
#plt.gca().xaxis.grid(color='gray', linestyle='dotted')
#plt.gca().yaxis.grid(color='gray', linestyle='dotted')


def bounds(d, dmin, dmax):
    if d:
        if dmin is None:
            dmin = min(d)
        else:
            dmin = min(dmin, min(d))
        if dmax is None:
            dmax = max(d)
        else:
            dmax = max(dmax, max(d))
    return dmin, dmax

xmin, xmax = None, None
ymin, ymax = None, None

#for i, (station_id, station_name) in enumerate(stations):
#    c.execute(query, (station_id,))
for i, (neighborhood, _num) in enumerate(neighborhoods):
    continue
    c.execute(query, (neighborhood,))
    rows = list(c.fetchall())
    x = [r[0] for r in rows]
    y = [r[1] for r in rows]
    xmin, xmax = bounds(x, xmin, xmax)
    #ymin, ymax = bounds(y, ymin, ymax)
    # plt.scatter(x, y, label=station_id, s=2)
    #label = station_name + ' ' + station_id
    label = neighborhood
    f.axes[i].plot(x, y, label=label)
    f.axes[i].legend(loc='upper left')
    f.axes[i].grid(True)
    f.axes[i].xaxis.grid(color='gray', linestyle='dotted')
    f.axes[i].yaxis.grid(color='gray', linestyle='dotted')
    f.axes[i].axis('tight')
    # works, but too flat
    #b, m = polyfit(x, y, 1)
    #plt.plot(x, np.asarray(m) * x + b, '-')
    # works
    #from scipy.interpolate import spline
    #xnew = np.linspace(min(x), max(x), 500)  # 300 represents number of points to make between T.min and T.max
    #y_smooth = spline(x, y, xnew)
    #plt.plot(xnew, y_smooth)

plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
f.gca().set_xlim([xmin, xmax])  # scatter fucks the x axis...
#f.gca().set_ylim([ymin, ymax])
plt.tick_params(labelsize=3)
#plt.show()
conn.close()

