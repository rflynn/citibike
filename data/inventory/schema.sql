
-- drop table citibike_inventory_log;
create table citibike_inventory_log (
    oid                     serial not null primary key,
    ts                      timestamp not null,
    created_at              timestamp not null default now()
);

-- drop table citibike_inventory_raw;
create table citibike_inventory_raw (
    -- station statuses; expected to remain relative stable, and only change occasionally
    coords_longlat          numeric[2] not null,
    -- at the time of creation most entries will be stations; but some entries are lone lockable bikes
    station_id              text,
    terminal                text,
    name                    text,
    installed               boolean,
    accepts_dockable_bikes  boolean,
    accepts_lockable_bikes  boolean,
    capacity                smallint,
    renting                 boolean,
    returning_              boolean,
    valet_status            text,
    docks_disabled          smallint,
    -- bike/dock availability; expected to fluctuate throughout the day
    bikes_available         smallint,
    docks_available         smallint,
    bikes_disabled          smallint,
    bikes                   jsonb,
    -- extra statuses, importance unclear
    -- ...
    -- time info
    last_reported           integer,
    ts                      timestamp not null,
    created_at              timestamp not null default now()
);

create index idx_citibike_inventory_raw_coords_longlat on citibike_inventory_raw (coords_longlat);
create index idx_citibike_inventory_raw_last_reported on citibike_inventory_raw (last_reported);


-- drop table citibike_inventory_updates ;
create table citibike_inventory_updates (
    -- station statuses; expected to remain relative stable, and only change occasionally
    coords_longlat          numeric[2] not null,
    -- at the time of creation most entries will be stations; but some entries are lone lockable bikes
    station_id              text,
    terminal                text,
    name                    text,
    installed               boolean,
    accepts_dockable_bikes  boolean,
    accepts_lockable_bikes  boolean,
    capacity                smallint,
    renting                 boolean,
    returning_              boolean,
    valet_status            text,
    docks_disabled          smallint,
    -- bike/dock availability; expected to fluctuate throughout the day
    bikes_available         smallint,
    docks_available         smallint,
    bikes_disabled          smallint,
    bikes                   jsonb,
    -- extra statuses, importance unclear
    -- ...
    -- time info
    last_reported           integer,
    ts                      timestamp not null,
    created_at              timestamp not null default now()
);

create index idx_citibike_inventory_updates_coords_longlat on citibike_inventory_updates (coords_longlat);
create index idx_citibike_inventory_updates_last_reported on citibike_inventory_updates (last_reported);




drop table citibike_station_status;
create table citibike_station_status (
    station_id              text not null check (station_id <> ''),
    terminal                text not null check (terminal <> ''),
    name                    text,
    coords_longlat          numeric[2] not null,
    installed               boolean,
    accepts_dockable_bikes  boolean,
    accepts_lockable_bikes  boolean,
    capacity                smallint,
    renting                 boolean,
    returning_              boolean,
    valet_status            text,
    -- timing/update info
    update_cnt              integer default 1,
    min_last_reported       integer,
    last_reported           integer,
    ts_created              timestamp not null,
    ts_updated              timestamp not null,
    created_at              timestamp not null default now(),
    updated_at              timestamp not null default now()
);

create unique index idx_citibike_station_status_uniq on citibike_station_status (
    station_id, terminal, coalesce(name, ''), coords_longlat,
    installed, accepts_dockable_bikes, accepts_lockable_bikes,
    capacity, renting, returning_, coalesce(valet_status, ''));

create index idx_citibike_station_status_id on citibike_station_status (station_id);
create index idx_citibike_station_status_last_reported on citibike_station_status (last_reported);

-- drop table citibike_station_inventory;
create table citibike_station_inventory (
    station_id              text not null check (station_id <> ''),
    -- bike/dock availability; expected to fluctuate throughout the day
    docks_available         smallint,
    docks_disabled          smallint,
    bikes_available         smallint,
    bikes_disabled          smallint,
    -- timing info
    last_reported           integer, -- freshness as reported by api
    ts                      timestamp not null, -- when API is hit
    created_at              timestamp not null default now() -- when record was created
);
create index idx_citibike_station_inventory_id on citibike_station_inventory (station_id);
create index idx_citibike_station_inventory_last_reported on citibike_station_inventory (last_reported);
