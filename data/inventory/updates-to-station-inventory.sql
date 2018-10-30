begin;

with
inventorylatest as (
    select
        station_id,
        max(last_reported) as last_reported
    from citibike_station_inventory
    group by station_id
),
updates as (
    select
        u.station_id,
        u.docks_available, u.docks_disabled,
        u.bikes_available, u.bikes_disabled,
        u.last_reported, u.ts
    from citibike_inventory_updates u
    left join inventorylatest l using (station_id)
    where u.station_id is not null
    and (u.last_reported > l.last_reported or l.last_reported is null)
)
insert into citibike_station_inventory (
    station_id,
    docks_available, docks_disabled,
    bikes_available, bikes_disabled,
    last_reported, ts
)
select
    station_id,
    docks_available, docks_disabled,
    bikes_available, bikes_disabled,
    last_reported, ts
from updates
order by station_id,
         last_reported
;

commit;
