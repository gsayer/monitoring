addr = psutil.net_if_addrs()['eth0'][0][1]
#boucle infini
  while True:
      cpu = psutil.cpu_percent()
      mem = psutil.virtual_memory()[2]
      time.sleep(1)
