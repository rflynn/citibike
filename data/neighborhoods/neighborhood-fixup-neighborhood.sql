
-- check:
-- should all West Village just be 'Greenwich Village' - probably

begin;

/*

create table station_neighborhoods as select row_number() over (partition by station_id) n, * from (select distinct on (n.state, n.county, city, n.name, s.name) n.state, n.county as ncounty, NULL as city, n.name as nname, s.name as sname, s.station_id, s.terminal, s.coord_long, s.coord_lat, regionid from citibike_station s left join neighborhood n on n.shape @> point(s.coord_long, s.coord_lat))_ order by sname, ncounty, nname;

update station_neighborhoods set state='NJ', city='Jersey City' where state is null and terminal like 'JC%';
update station_neighborhoods set city='New York' where state='NY' and city is null;

select * from station_neighborhoods where station_id in (select station_id from station_neighborhoods group by station_id having count(*)>1) order by sname;
*/

delete from station_neighborhoods where sname='11 Ave & W 59 St' and nname <> 'Upper West Side';
delete from station_neighborhoods where sname='W 59 St & 10 Ave' and nname <> 'Upper West Side';


-- Clinton (Hell's Kitchen)
update station_neighborhoods set nname='Clinton', regionid=null where sname='W 34 St & 11 Ave';
delete from station_neighborhoods where sname='W 34 St & 11 Ave' and n>1;
delete from station_neighborhoods where sname='W 50 St & 9 Ave' and nname <> 'Clinton';
delete from station_neighborhoods where sname='W 45 St & 8 Ave' and nname <> 'Clinton';

delete from station_neighborhoods where sname='8 Ave & W 52 St' and nname <> 'Midtown';

delete from station_neighborhoods where sname='12 St & 4 Ave' and nname <> 'Gowanus';
delete from station_neighborhoods where sname='4 Ave & 9 St' and nname <> 'Gowanus';

delete from station_neighborhoods where sname='1 Ave & E 16 St' and nname <> 'Stuyvesant Town';
delete from station_neighborhoods where sname='1 Ave & E 18 St' and nname <> 'Stuyvesant Town';

delete from station_neighborhoods where sname='3 Ave & Schermerhorn St' and nname <> 'Downtown';

delete from station_neighborhoods where sname='3 St & Prospect Park West' and nname <> 'Prospect Park';

delete from station_neighborhoods where sname='5 Ave & E 126 St' and nname <> 'East Harlem';

delete from station_neighborhoods where sname='5 Ave & E 88 St' and nname <> 'Carnegie Hill';
delete from station_neighborhoods where sname='5 Ave & E 93 St' and nname <> 'Carnegie Hill';

delete from station_neighborhoods where sname='8 Ave & W 31 St' and nname <> 'Chelsea';
delete from station_neighborhoods where sname='8 Ave & W 33 St' and nname <> 'Chelsea';
delete from station_neighborhoods where sname='W 15 St & 6 Ave' and nname <> 'Chelsea';

delete from station_neighborhoods where sname='Atlantic Ave & Furman St' and nname <> 'Brooklyn Heights';

delete from station_neighborhoods where sname='Bayard St & Leonard St' and nname <> 'Williamsburg';

delete from station_neighborhoods where sname='Carroll St & Smith St' and nname <> 'Carroll Gardens';
delete from station_neighborhoods where sname='Smith St & 3 St' and nname <> 'Carroll Gardens';
delete from station_neighborhoods where sname='Smith St & 9 St' and nname <> 'Carroll Gardens';
delete from station_neighborhoods where sname='Warren St & Court St' and nname <> 'Carroll Gardens';
delete from station_neighborhoods where sname='Henry St & Degraw St' and nname <> 'Carroll Gardens';

-- Upper West Side
delete from station_neighborhoods where sname='Cathedral Pkwy & Broadway' and nname <> 'Upper West Side';
delete from station_neighborhoods where sname='W 82 St & Central Park West' and nname <> 'Upper West Side';

-- Morningside Heights
delete from station_neighborhoods where sname='W 110 St & Amsterdam Ave' and nname <> 'Morningside Heights';

delete from station_neighborhoods where sname='Howard St & Centre St' and nname <> 'Little Italy';
delete from station_neighborhoods where sname='Lafayette St & Jersey St' and nname <> 'Little Italy';


delete from station_neighborhoods where sname='W 37 St & 5 Ave' and nname <> 'Garment District';


delete from station_neighborhoods where sname='Central Park North & Adam Clayton Powell Blvd' and nname <> 'Harlem';
--delete from station_neighborhoods where sname='St. Nicholas Ave & W 126 St' and nname <> 'Manhattanville';
--update station_neighborhoods set nname='Manhattanville',regionid=270879 where sname='St. Nicholas Ave & W 126 St';
-- insert into station_neighborhoods values (1, 'NY', 'New York', 'New York', 'Manhattanville', 'St. Nicholas Ave & W 126 St', '3533', '7756.10', '-73.9518776', '40.8114323', 270879);
update station_neighborhoods set nname='Manhattanville', regionid=270879 where sname='Broadway & Moylan Pl';
update station_neighborhoods set nname='Manhattanville', regionid=270879 where sname='Amsterdam Ave & W 125 St';
update station_neighborhoods set nname='Manhattanville', regionid=270879 where sname='Frederick Douglass Blvd & W 129 St';

-- Civic Center
update station_neighborhoods set nname='Civic Center', regionid=null where sname='Centre St & Chambers St';
delete from station_neighborhoods where sname='Centre St & Chambers St' and n>1;
update station_neighborhoods set nname='Civic Center', regionid=null where sname='Reade St & Broadway';
update station_neighborhoods set nname='Civic Center', regionid=null where sname='St James Pl & Oliver St';

-- Yorkville
update station_neighborhoods set nname='Yorkville', regionid=null where sname='3 Ave & E 95 St';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='2 Ave & E 96 St';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 93 St & 2 Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='1 Ave & E 94 St';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 91 St & 2 Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 89 St & 3 Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 89 St & York Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 88 St & 1 Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='East End Ave & E 86 St';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 85 St & 3 Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 85 St & York Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 84 St & 1 Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 82 St & East End Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 81 St & 2 Ave';
update station_neighborhoods set nname='Yorkville', regionid=null where sname='E 81 St & York Ave';

-- Lenox Hill
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='1 Ave & E 62 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='1 Ave & E 68 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='1 Ave & E 78 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='3 Ave & E 62 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='3 Ave & E 71 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='3 Ave & E 72 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='5 Ave & E 63 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='5 Ave & E 73 St';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 59 St & Madison Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 60 St & York Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 65 St & 2 Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 66 St & Madison Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 67 St & Park Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 68 St & 3 Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 68 St & Madison Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 71 St & 2 Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 72 St & Park Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 72 St & York Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 74 St & 1 Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 75 St & 3 Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 76 St & Park Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='E 77 St & 3 Ave';
update station_neighborhoods set nname='Lenox Hill', regionid=null where sname='Lexington Ave & E 63 St';

-- Two Bridges
update station_neighborhoods set nname='Two Bridges', regionid=null where sname='St James Pl & Pearl St';
update station_neighborhoods set nname='Two Bridges', regionid=null where sname='Madison St & Clinton St';
update station_neighborhoods set nname='Two Bridges', regionid=null where sname='Madison St & Montgomery St';
update station_neighborhoods set nname='Two Bridges', regionid=null where sname='Pike St & Monroe St';
update station_neighborhoods set nname='Two Bridges', regionid=null where sname='Catherine St & Monroe St';

-- Battery Park City
update station_neighborhoods set nname='Battery Park City', regionid=null where sname='West St & Chambers St';
update station_neighborhoods set nname='Battery Park City', regionid=null where sname='Vesey Pl & River Terrace';
update station_neighborhoods set nname='Battery Park City', regionid=null where sname='South End Ave & Liberty St';
update station_neighborhoods set nname='Battery Park City', regionid=null where sname='West Thames St';
update station_neighborhoods set nname='Battery Park City', regionid=null where sname='Little West St & 1 Pl';

-- Brooklyn Heights
delete from station_neighborhoods where sname='Clinton St & Tillary St' and nname <> 'Brooklyn Heights';
delete from station_neighborhoods where sname='Henry St & Atlantic Ave' and nname <> 'Brooklyn Heights';
delete from station_neighborhoods where sname='Schermerhorn St & Court St' and nname <> 'Brooklyn Heights';


delete from station_neighborhoods where sname='Court St & State St' and nname <> 'Downtown';
delete from station_neighborhoods where sname='Johnson St & Gold St' and nname <> 'Downtown';


delete from station_neighborhoods where sname='Division St & Bowery' and nname <> 'Chinatown';

delete from station_neighborhoods where sname='Douglass St & 4 Ave' and nname <> 'Park Slope';

delete from station_neighborhoods where sname='E 16 St & Irving Pl' and nname <> 'Gramercy';

delete from station_neighborhoods where sname='E 20 St & FDR Drive' and nname <> 'Stuyvesant Town';

delete from station_neighborhoods where sname='E 35 St & 3 Ave' and nname <> 'Murray Hill';
delete from station_neighborhoods where sname='E 39 St & 3 Ave' and nname <> 'Murray Hill';

delete from station_neighborhoods where sname='E 51 St & Lexington Ave' and nname <> 'Turtle Bay';
delete from station_neighborhoods where sname='E 53 St & 3 Ave' and nname <> 'Turtle Bay';

delete from station_neighborhoods where sname='E 59 St & Madison Ave' and nname <> 'Upper East Side';


-- Kips Bay
update station_neighborhoods set nname='Kips Bay', regionid=null where sname='Lexington Ave & E 26 St';
delete from station_neighborhoods where sname='Lexington Ave & E 26 St' and n>1;
update station_neighborhoods set nname='Kips Bay', regionid=null where sname='Lexington Ave & E 29 St';
delete from station_neighborhoods where sname='Lexington Ave & E 29 St' and n>1;


delete from station_neighborhoods where sname='W 25 St & 6 Ave' and nname <> 'Chelsea';

delete from station_neighborhoods where sname='W 4 St & 7 Ave S' and nname <> 'Greenwich Village';
delete from station_neighborhoods where sname='Mercer St & Bleecker St' and nname <> 'Greenwich Village';


commit;
