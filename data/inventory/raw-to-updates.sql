begin;

with
latest as (
    select
        coord_long,
        coord_lat,
        max(last_reported) as last_reported,
        max(ts) as max_ts
    from citibike_inventory_updates
    group by coord_long, coord_lat
),
updates as (
    -- raw records that are 'last_reported' after our most recent status
    -- could be [0, n] records; raw records may be dupes -- that is, reporting on the same timestamp since no changes have taken place. we sample at a regular rate, but underlying changes may or may not happen
    select
        coord_long,
        coord_lat,
        station_id,
        terminal,
        name,
        installed,
        accepts_dockable_bikes,
        accepts_lockable_bikes,
        capacity,
        renting,
        returning_,
        valet_status,
        docks_disabled,
        bikes_available,
        docks_available,
        bikes_disabled,
        bikes,
        last_reported,
        ts
    from
        (select
            r.*,
            row_number() over (partition by r.coord_long, r.coord_lat,
                                            coalesce(r.last_reported,
                                                     extract(epoch from r.ts)::int)
                               order by coalesce(r.last_reported,
                                                 extract(epoch from r.ts)::int)) as rn
        from citibike_inventory_raw r
        left join latest l using (coord_long, coord_lat)
        where (r.station_id is not null and (r.last_reported > l.last_reported or l.last_reported is null))
        or (r.station_id is null and (r.ts > l.max_ts or l.max_ts is null))
        )_
    where rn=1
)
insert into citibike_inventory_updates (
    coord_long, coord_lat,
    station_id, terminal, name,
    installed, accepts_dockable_bikes, accepts_lockable_bikes,
    capacity, renting, returning_, valet_status,
    docks_disabled, bikes_available, docks_available, bikes_disabled,
    bikes, last_reported, ts
)
select
    coord_long, coord_lat,
    station_id, terminal, name,
    installed, accepts_dockable_bikes, accepts_lockable_bikes,
    capacity, renting, returning_, valet_status,
    docks_disabled, bikes_available, docks_available, bikes_disabled,
    bikes, last_reported, ts
from updates;

commit;
