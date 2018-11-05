begin;

-- fixups...
delete from neighborhood where state='NY' and name='Marble Hill' and county <> 'New York';
delete from neighborhood where state='NY' and name='Vinegar Hill' and county <> 'Kings';
delete from neighborhood where state='NY' and name='Rikers Island' and county <> 'Queens';
delete from neighborhood where state='NY' and name='Brooklyn Heights' and county <> 'Kings';

commit;
