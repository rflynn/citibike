begin;
delete from neighborhood_borough;
\copy neighborhood_borough(state, neighborhood_name, borough) from 'neighborhood2borough.csv' with csv header;
commit;
