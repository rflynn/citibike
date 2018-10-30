begin;

with
statuslatest as (
    select
        station_id,
        max(last_reported) as last_reported
    from citibike_station_status
    group by station_id
),
updates as (
    select
        u.station_id, u.terminal, u.name, u.coords_longlat,
        u.installed, u.accepts_dockable_bikes, u.accepts_lockable_bikes,
        u.capacity, u.renting, u.returning_, u.valet_status,
        u.last_reported, u.ts
    from citibike_inventory_updates u
    left join statuslatest l using (station_id)
    where u.station_id is not null
    and (u.last_reported > l.last_reported or l.last_reported is null)
),
grouped as (
    select
        station_id, terminal, name, coords_longlat,
        installed, accepts_dockable_bikes, accepts_lockable_bikes,
        capacity, renting, returning_, valet_status,
        count(*) as cnt,
        min(last_reported) as min_last_reported,
        max(last_reported) as max_last_reported,
        min(ts) as min_ts,
        max(ts) as max_ts
    from updates
    group by
        station_id, terminal, name, coords_longlat,
        installed, accepts_dockable_bikes, accepts_lockable_bikes,
        capacity, renting, returning_, valet_status
)
insert into citibike_station_status (
    station_id, terminal, name, coords_longlat,
    installed, accepts_dockable_bikes, accepts_lockable_bikes,
    capacity, renting, returning_, valet_status,
    update_cnt,
    ts_created, ts_updated,
    min_last_reported, last_reported
)
select
    station_id, terminal, name, coords_longlat,
    installed, accepts_dockable_bikes, accepts_lockable_bikes,
    capacity, renting, returning_, valet_status,
    cnt,
    min_ts, max_ts,
    min_last_reported, max_last_reported
from grouped
order by station_id,
         max_last_reported,
         max_ts
on conflict (station_id, terminal, coalesce(name, ''), coords_longlat,
             installed, accepts_dockable_bikes, accepts_lockable_bikes,
             capacity, renting, returning_, coalesce(valet_status, ''))
    do update set
        update_cnt=citibike_station_status.update_cnt+1,
        min_last_reported=coalesce(citibike_station_status.min_last_reported,
                                   EXCLUDED.last_reported),
        last_reported=EXCLUDED.last_reported,
        ts_updated=EXCLUDED.ts_updated,
        updated_at=now()
;

commit;
