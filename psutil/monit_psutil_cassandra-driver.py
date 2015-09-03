#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cassandra.cluster import Cluster
import logging
import time
import psutil

log = logging.getLogger()
log.setLevel('INFO')


class SimpleClient:
    session = None

    def connect(self, nodes):
        cluster = Cluster(nodes)
        metadata = cluster.metadata
        self.session = cluster.connect()
        log.info('Connected to cluster: ' + metadata.cluster_name)
        for host in metadata.all_hosts():
            log.info('Datacenter: %s; Host: %s; Rack: %s',
                host.datacenter, host.address, host.rack)

    def close(self):
        self.session.cluster.shutdown()
        self.session.shutdown()
        log.info('Connection closed.')

#########

    def create_schema(self):
        self.session.execute("""CREATE KEYSPACE IF NOT EXISTS stat
        WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor':3}
        AND DURABLE_WRITES = false;""")
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS stat.memory (
            addr varchar,
            value float,
            time timeuuid PRIMARY KEY
            );
        """)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS stat.cpu (
                addr varchar,
                value float,
                time timeuuid PRIMARY KEY
                );
        """)
        log.info('Simplex keyspace and schema created.')

##############

##############      TTTTLLL

    def save_data(self, addr, cpu, mem):
        print("mem : %s", mem)
        self.session.execute("""
            INSERT INTO stat.memory (addr, value, time)
            VALUES (
                %s,
                %s,
                now()
            );
        """,[addr, mem])
        print("cpu : %s", cpu)
        self.session.execute("""
            INSERT INTO stat.cpu (addr, value, time)
            VALUES (
                %s,
                %s,
                now()
            );
        """,[addr, cpu])
        log.info('Data loaded.')

#    def query_schema(self):
#        results = self.session.execute("""
#    SELECT * FROM simplex.playlists
#    WHERE id = 2cc9ccb7-6221-4ccb-8387-f22b6a1b354d;
#""")
#        print "%-30s\t%-20s\t%-20s\n%s" % \
#    ("title", "album", "artist",
#        "-------------------------------+-----------------------+--------------------")
#        for row in results:
#            print "%-30s\t%-20s\t%-20s" % (row.title, row.album, row.artist)
#        log.info('Schema queried.')





def main():
    logging.basicConfig()
    client = SimpleClient()
    client.connect(['127.0.0.1'])
    client.create_schema()
    addr = psutil.net_if_addrs()['eth0'][0][1]
#boucle infini
    while True:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()[2]
        time.sleep(1)
        client.save_data(addr, cpu, mem)

#fin de boucle
#    client.query_schema()
    client.close()

if __name__ == "__main__":
    main()
