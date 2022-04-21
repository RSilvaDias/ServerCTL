# DataCollector

## Compiling

### Repository

dnc . -v

### DC

dnc . -sp ../repository/ -v

### Distributor

dnc . -sp ../dc/ -v

## Running
* Requires Dana Version 237

dana -sp "../repository/;../dc" Distributor.o
