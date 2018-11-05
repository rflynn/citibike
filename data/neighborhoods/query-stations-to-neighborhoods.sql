-- XXX: not great yet, but just a sketch...
-- NOTE: yields dupes based on neighborhood definition
-- NOTE: some lat/long almost certainly slightly wrong, leading to wrong answers, oh well...
select row_number() over (partition by station_id) n, *
from (
    select distinct on (n.county, n.name, s.name)
        n.county as ncounty, n.name as nname, s.name as sname, s.station_id, s.terminal, s.coord_long, s.coord_lat, regionid
    from citibike_station s
    left join neighborhood n on n.shape @> point(s.coord_long, s.coord_lat)  -- juicy part: polygon/point geometric "contains?" -- neato!
)_ order by ncounty, nname, sname;
