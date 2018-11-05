-- neighborhood as defined by Zillow
-- drop table neighborhood;
create table neighborhood (
    oid         serial  not null primary key,
    state       char(2) not null,
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

create index idx_neighborhood_regionid on neighborhood (regionid);

create table citibike_station_neighborhood (
    oid                 serial not null primary key,
    citibike_station_id text   not null,
    neighborhood_oid    integer
);


create table neighborhood_borough (
    oid                 serial not null primary key,
    state               char(2) not null,
    neighborhood_name   text not null,
    borough             text not null,
    unique (state, neighborhood_name)
);


create table neighborhood_section_manhattan (
    oid                 serial not null primary key,
    state               char(2) not null,
    neighborhood_name   text not null,
    section             text not null,
    unique (state, neighborhood_name)
);
comment on table neighborhood_section_manhattan is 'larger-scale sections of Manhattan -- >= neighborhood, < borough';
