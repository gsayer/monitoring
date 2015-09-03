#!/bin/bash
cqlsh -e "CREATE KEYSPACE IF NOT EXISTS vmstat
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }
AND DURABLE_WRITES = false;"

cqlsh -e "CREATE TABLE IF NOT EXISTS vmstat.free_memory (
addr varchar,
value int,
time timeuuid PRIMARY KEY
);"

cqlsh -e "CREATE TABLE IF NOT EXISTS vmstat.cpu_idle (
addr varchar,
value int,
time timeuuid PRIMARY KEY
);"

while true;do
#  time=$(date +"%Y-%m-%d %T")
  addr=$(ip -4 addr show eth0 | grep inet | awk {'print $2'} | cut -f 1 -d '/')
  resvm=$(vmstat | tail -1)
  free_mem=$(echo $resvm | awk {'print $4'})
  cpu_idle=$(echo $resvm | awk {'print $15'})

#cqlsh -e "INSERT INTO vmstat.free_memory(addr,value,time)
#            VALUES ('$addr', $free_mem, now())
#            USING TTL 20;"
##cqlsh -e "INSERT INTO vmstat.cpu_idle(addr,value,time
##VALUES ('$addr','$cpu_idle','$time') USING TTL 20;"
  # DBUG
  echo $addr  $free_mem $cpu_idle

sleep 0.5
done
