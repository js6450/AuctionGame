#!/usr/bin/env python
# Echo server program
import select
import socket
import sys
import random
import time
import os


bot = True #Don't change this
numbidders = 2 #change this for how many bots you want to play with
#HOST = 'localhost'
HOST = '10.225.5.201'

os.system('cls')
if not bot:
  print "Server initiated, waiting for players to connect.\n"
else:
  print "Server initiated, waiting for bots to connect.\n"


PORT = 50018              # Arbitrary non-privileged port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
input = [server]
bidderids = []
neededtowin = 3 # how many items each player needs to win
itemtypes = ['Picasso', 'Van_Gogh', 'Rembrandt', 'Da_Vinci'] # four different types
maxbudget = 100 # budget per player
won = {}
listtosend = str(numbidders) + ' '
typearray = []
i = 0
while(i < 200):
  x = itemtypes[int((len(itemtypes))*random.random())]
  typearray.append(x)
  listtosend = listtosend + x + ' '
  i+= 1

# distribute list to send to everyone
bidderids = []
readybidders = []
while(numbidders > len(readybidders)):
  inputready,outputready,exceptready = select.select(input,[],[])
  for s in inputready:
    if s == server:
      # print "In server case"
      client, address = server.accept()
      input.append(client)
    if((s != server) & (s!=sys.stdin)):
      data = s.recv(1024)
      if not data: 
        print "Have not received data from", str(s)
      indata = data.split(" ")
      # print ' '.join(indata)
      if(indata[0] in bidderids):
        if len(bidderids) == numbidders:
          if indata[0] in readybidders:
            pass
          else:
            stringtosend = 'ready '
            for name in bidderids:
              stringtosend += name + ' '
            s.send(stringtosend)
            readybidders.append(indata[0])
        else:
          s.send('wait ')
        #s.send("Not ready " + indata[0] )
      else:
        s.send(listtosend)
        bidderids.append(indata[0])
        print indata[0], "joined the game"
if not bot:
  print "everyone has connected, let's go!\n"
else:
  print "everyone has connected, let the Bot Battles begin!"
  time.sleep(2)
won['Picasso'] = {name: 0 for name in bidderids}
won['Van_Gogh'] = {name: 0 for name in bidderids}
won['Rembrandt'] = {name: 0 for name in bidderids}
won['Da_Vinci'] = {name: 0 for name in bidderids}
moneyspent = {name: 0 for name in bidderids}
players = bidderids
doneflag = 0 # will be done only if someone wins or goes over budget with money spent
j = 0
while(0 == doneflag):
  os.system('cls')
  mytype = typearray[j]
  start = time.time()
  hurried = [False for i in range(201)]
  hurried[20] = True
  for i in range(20, 201, 10):
    hurried[i] = True
  print "Auction round", str(j+1) + ':'
  print
  if not bot:
    if j != 0:
      print winnerid, "bought item", mytype, "for", bestbid
      print
    print "Current standings are:\n"
    for player in players:
      print player + ':', {'money': 100-moneyspent[player], 'Picasso': won['Picasso'][player], "Rembrandt": won['Rembrandt'][player], "Da_Vinci": won['Da_Vinci'][player], "Van_Gogh": won['Van_Gogh'][player]}
    print
  print "We are currently bidding for", mytype + '.'
  print
  bidderids = []
  bids = []
  while(numbidders > len(bidderids)):
    inputready,outputready,exceptready = select.select(input,[],[])
    timePassed = int(time.time()-start)
    if hurried[timePassed]:
      hurried[timePassed] = False
      for player in players:
        if not player in bidderids:
          print player + ',',
      print("hurry up!")
    for s in inputready:
      if s == server:
        # print "In server case"
        client, address = server.accept()
        input.append(client)
      if((s != server) & (s!=sys.stdin)):
        data = s.recv(1024)
        if not data: 
          print "Have not received data from", str(s)
        indata = data.split(" ")
        # print ' '.join(indata)
        if(indata[0] in bidderids):
          s.send('wait ')
          #s.send("Not ready " + indata[0] + " to tell you about move " + str(j+1) )
        else:
          x = int(indata[1])
          if (x > (maxbudget - moneyspent[indata[0]])):
            x = -1 # indata[0] is not allowed to bid over budget
          bids.append(x)
          bidderids.append(indata[0])
          s.send('bid received')
          if not bot:
            print "received bid of", "from", indata[0]
          else:
            print "received bid of", x, "from", indata[0]
            print
          # print "number of bids received is: ", len(bidderids)
  # Now have all the bids
  bestbid = max(bids)
  # print "Best bid for step ", j, " is ", bestbid
  # print "Here are the identifiers of the bidders " 
  # print bidderids
  # print "Here are the bids "
  # print bids
  #winnerid=bidderids[random.choice([x for x in range(len(bids)) if bids[x]==bestbid])]
  winnerid = bidderids[bids.index(bestbid)]
  if (won[mytype][winnerid] >= neededtowin-1):
    doneflag = 1
    os.system('cls')
    print  winnerid, "has won."
    print "Please close all child processes and this one"
  # Now receive requests for results
  deletedindexes = [] # record which indexes are gone
  while(numbidders > len(deletedindexes)):
    inputready,outputready,exceptready = select.select(input,[],[])
    for s in inputready:
      if((s != server) & (s!=sys.stdin)):
        data = s.recv(1024)
        if not data: 
          print "Have not received data from", str(s)
        indata = data.split(" ")
        # print ' '.join(indata)
        myindex = bidderids.index(indata[0])
        if(myindex not in deletedindexes):
          deletedindexes.append(myindex)
          if(winnerid == indata[0]):
            # s.send(bidderids[myindex] + ' you have bought this item of type ' + mytype)
            
            won[mytype][winnerid]+= 1
            moneyspent[winnerid]+= bestbid
            if(doneflag == 1):
              s.send(winnerid + ' has bought ' + mytype + ' for ' + str(bestbid) + ' and won.')
            else:
              s.send(winnerid + ' has bought ' + mytype + ' for ' + str(bestbid))
          else:
            if doneflag == 1:
              s.send(winnerid + ' has bought ' + mytype + ' for ' + str(bestbid) + ' and won.')
            else:
              s.send(winnerid + ' has bought ' + mytype + ' for ' + str(bestbid))
        else:
          s.send('ready')
          #s.send("Not ready for next round yet " + indata[0])
  j+=1
  if bot:
    time.sleep(3)
    print winnerid, "bought item", mytype, "for", bestbid
    print
    print "Current standings are:\n"
    for player in players:
      print player + ':', {'money': 100-moneyspent[player], 'Picasso': won['Picasso'][player], "Rembrandt": won['Rembrandt'][player], "Da_Vinci": won['Da_Vinci'][player], "Van_Gogh": won['Van_Gogh'][player]}, "\n"
    print
    time.sleep(5)

time.sleep(40)