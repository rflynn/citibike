
drop table citibike_station;
create table citibike_station (
    oid             serial not null primary key,
    station_id      text not null unique,
    terminal        text not null unique,
    coord_long      numeric not null,
    coord_lat       numeric not null,
    name            text,
    created_at      timestamp not null default now(),
    updated_at      timestamp not null default now()
);

insert into citibike_station (
    station_id, terminal, coord_long, coord_lat, name, created_at
)
select
    station_id, terminal, coord_long, coord_lat, name, created_at
from (
    select
        row_number() over (partition by station_id order by last_reported) n,
        station_id, terminal, coord_long, coord_lat, name, created_at
    from citibike_station_status
)_ where n=1
on conflict (station_id) do nothing;


/*
-- triang1
with x as (
    select station_id, count(*)
    from citibike_station_inventory
    group by station_id
),
y as (
    select avg(count) from x
)
select
    s.coord_long,
    s.coord_lat,
    log(x.count::float/(select avg from y))
from citibike_station s
join x using (station_id)
order by oid;
*/

/*
select coord_long, coord_lat from citibike_station order by oid;
*/


create table citibike_station_distance (
    s1              smallint not null references citibike_station (oid),
    s2              smallint not null references citibike_station (oid),
    dist            real not null,
    nth             smallint
    -- created_at      timestamp not null default now()
);
create index idx_citibike_station_distance_stations on citibike_station_distance (s1, s2);

insert into citibike_station_distance (s1, s2, dist)
select
    s.oid,
    s2.oid,
    sqrt(pow(s.coord_long - s2.coord_long, 2)
       + pow(s.coord_lat  - s2.coord_lat, 2))
from citibike_station s
join citibike_station s2 on s2.oid <> s.oid
where not exists (select 1 from citibike_station_distance d where s1=s.oid and s2=s2.oid)
;

/*
-- triang2
-- select the shortest edges that includes all nodes at least once
with x as (
    select
        row_number() over (partition by s1 order by dist) n1,
        row_number() over (partition by s2 order by dist) n2,
        s1, s2, dist
    from citibike_station_distance
)
select s1-1, s2-1, s2-1
from x
where n1 <= 3 or n2 <= 3
order by dist;
*/

-- original sketch
/*
with s as (
    select distinct coords_longlat as longlat
    from citibike_station_status
),
distance as (
    select
        s.longlat as s1_longlat,
        s2.longlat as s2_longlat,
        sqrt(abs(s.longlat[1] - s2.longlat[1]) + abs(s.longlat[2] - s2.longlat[2])) as dist
    from s
    join s s2 on s2.longlat > s.longlat
),
closest as (
    select
        row_number() over (partition by s1_longlat order by dist) rn,
        s1_longlat, s2_longlat, dist
    from distance
)
select
    s1_longlat,
    s2_longlat,
    dist
from closest
where rn <= 3;
*/
