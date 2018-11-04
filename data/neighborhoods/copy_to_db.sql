begin;
delete from neighborhood where state='NY';
\copy neighborhood(state, county, city, name, regionid, shape) from 'nyc_neighborhoods.csv' with csv header;
commit;
