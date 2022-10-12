cd repository
dnc . -v
cd ..
cd dc
dnc . -sp ../repository/ -v
cd ..
cd distributor
dnc . -sp "../dc;../repository" -v
cd ..