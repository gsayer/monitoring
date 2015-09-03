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

awk_cqlsh='{print "INSERT INTO vmstat.free_memory(addr,value,time) VALUES ('"'"'"$19"'"'"', " $4 ", now()) USING TTL 20; INSERT INTO vmstat.cpu_idle(addr,value,time) VALUES ('"'"'"$19"'"'"', " $15 ", now()) USING TTL 20;"}'

while true;do
#  time=$(date +"%Y-%m-%d %T")
  addr=$(ip -4 addr show eth0 | grep inet )
  resvm=$(vmstat | tail -1;echo $addr)
  #free_mem = $4
  #cpu_idle = $15
  #addr = l$18

 echo $resvm | awk "$awk_cqlsh"


#echo "INSERT INTO vmstat.free_memory(addr,value,time)
#            VALUES ('$addr', $free_mem, now())
#            USING TTL 20;
#            INSERT INTO vmstat.cpu_idle(addr,value,time
#            VALUES ('$addr','$cpu_idle','$time') USING TTL 20;"
  # DBUG
  #echo $addr  $free_mem $cpu_idle

sleep 0.3
done | cqlsh
