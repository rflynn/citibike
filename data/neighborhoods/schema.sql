-- neighborhood as defined by Zillow
-- drop table neighborhood;
create table neighborhood (
    oid         serial  not null primary key,
    state       text    not null,
    county      text    not null,
    city        text    not null,
    name        text    not null,
    regionid    integer not null,
    shape       polygon not null
    -- unique (state, county, city, name)
);

/*
$ egrep 270880 nyc_neighborhoods.csv
NY,Bronx,New York,Marble Hill,270880,"-73.91071526499991, 40.87890143900006"
NY,New York,New York,Marble Hill,270880,"-73.91071526499991, 40.87890143900006"
*/

