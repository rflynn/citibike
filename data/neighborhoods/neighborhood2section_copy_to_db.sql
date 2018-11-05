begin;
delete from neighborhood_section_manhattan;
\copy neighborhood_section_manhattan(state, neighborhood_name, section) from 'neighborhood2section.csv' with csv header;
commit;
