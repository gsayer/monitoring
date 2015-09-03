#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil



addr = psutil.net_if_addrs()['eth0'][0][1]

#boucle infini
cpu = psutil.cpu_percent()
mem = psutil.virtual_memory()[2]

print (addr)
print (cpu)
print (mem)
