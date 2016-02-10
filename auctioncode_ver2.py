from __future__ import print_function
# Echo client program
import socket
import random
import time
import os
import platform

import operator

#HOST = 'localhost'
HOST = '10.225.5.201'

# to act as a client
PORT = 50018			  # The server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


# APPLICATION

partnerid = -1 # no partner
numberbidders = 0 # will be given by server
artists = ['Picasso', 'Rembrandt', 'Van_Gogh', 'Da_Vinci']

# DO SOMETHING HERE
# you need to change this to do something much more clever
def determinebid(itemsinauction, winnerarray, winneramount, numberbidders, players, artists, standings, rd):

    startpoint = 0
    if(rd != 0 and rd %3 == 0):
        startpoint = rd

    freq = {'Picasso': 0, 'Rembrandt': 0, 'Van_Gogh': 0, 'Da_Vinci': 0}
    order = []
    points = {'Picasso': 0, 'Rembrandt': 0, 'Van_Gogh': 0, 'Da_Vinci': 0}

    for i in range(startpoint, 20):
        freq[itemsinauction[i]] += 1
        if freq[itemsinauction[i]] == 3:
            order.append(itemsinauction[i])

    sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

    for i in range(len(sorted_freq)):
        points[sorted_freq[i][0]] = 4 - i
    for i in range(len(order)):
        points[order[i]] += 5-i
    
    sorted_points = sorted(points.items(), key=operator.itemgetter(1), reverse=True)

    #determine price for bid item
    biditem = sorted_points[0][0]
    bidval = 3
    average_price = 0
    max_price = 0
    if(rd > 0):
        average_price = float(sum(winneramount)/len(winneramount))
        if(max(winneramount) < 15):
            max_price = max(winneramount) + 5
        elif(max(winneramount) < 30 and max(winneramount) >= 15):
            max_price = max(winneramount) + 2
        else:
            max_price = 33

    print("Round: " + str(rd + 1) + " with item " + itemsinauction[rd] + " for sale")
    print(sorted_points)
    print("Aiming to purchase: " + biditem)

    if(itemsinauction[rd] == biditem):
        if(rd == 0):
            bidval = 20
        else:
            bidval = random.randint(int(average_price), max_price) #change
        print ("Bidding on: " + biditem + " for " + str(bidval))
    elif(itemsinauction[rd] != biditem and rd > 2):
        bidval = 0

    return bidval

mybidderid = raw_input("Input team / player name : ").strip()  # this is the only thing that distinguishes the clients 
while len(mybidderid) == 0 or ' ' in mybidderid:
  mybidderid = raw_input("You input an empty string or included a space in your name which is not allowed (_ or / are all allowed)\n for example Emil_And_Nischal is okay\nInput team / player name: ").strip()

moneyleft = 100 # should change over time
winnerarray = [] # who won each round
winneramount = [] # how much they paid

itemsinauction = []
myTypes = {'Picasso': 0, 'Rembrandt': 0, 'Van_Gogh': 0, 'Da_Vinci': 0, 'money': moneyleft}

# EXECUTION

# get list of items and types
getlistflag = 1
s.send(str(mybidderid))
while(getlistflag == 1):
  # print "Have sent data from ", str(mybidderid)
  data = s.recv(5024)
  x = data.split(" ")
  # print "Have received response at ", str(mybidderid), " of: ", ' '.join(x)
  if(x[0] != "Not" and len(data) != 0):
	getlistflag = 0
	numberbidders = int(x[0])
	itemsinauction = x[1:]
  else:
	time.sleep(2)

while True:
  s.send(str(mybidderid) + ' ')
  data = s.recv(5024)
  x = data.split(" ")
  if (x[0] == 'wait'):
	continue
  players = []
  for player in range(1, numberbidders + 1):
	players.append(x[player])
  break
standings = {name: {'Picasso': 0, 'Van_Gogh': 0, 'Rembrandt': 0, 'Da_Vinci': 0, 'money': 100} for name in players}
# now do bids
continueflag = 1
j = 0
while(continueflag == 1):
  #roundStart = time.time()
  print(random.choice(["I'm doing my best, okay?", "Why aren't you cheering louder?", "Aren't you proud of me?", "Damn I'm good, and I don't even have a brain!", "And do you think you could do any better?", "I feel like it's me doing all the work, you're just chilling in your chair", "If I lose this it's your fault not mine... I'm doing EXACTLY what you told me to do!"]))
  print()
  bidflag = 1
  bid = determinebid(itemsinauction, winnerarray, winneramount, numberbidders, players, artists, standings, len(winnerarray))
  time.sleep(0.2)
  s.send(str(mybidderid) + " " + str(bid))
  while(bidflag == 1):
	# print "Have sent data from ", str(mybidderid)
	data = s.recv(5024)
	x = data.split(" ")
	# print "Have received response at ", str(mybidderid), " of: ", ' '.join(x)
	if(x[0] != "Not"):
	  bidflag = 0
	else:
	  print("exception")
	  time.sleep(2)


  resultflag = 1
  while(resultflag == 1):
	s.send(str(mybidderid))
	# print "Have sent data from ", str(mybidderid)
	data = s.recv(5024)
	x = data.split(" ")
	if (x[0] == 'wait'):
	  continue
	# print "Have received response at ", str(mybidderid), " of: ", ' '.join(x)
	if len(x) >= 7 and x[7] == 'won.':
	  time.sleep(5)
	  continueflag = 0
	  resultflag = 0
	  print(data)
	  print()
	  print('game over')
	if(x[0] != "ready") and (continueflag == 1):
	  #roundLength = time.time()-roundStart
	  #time.sleep(max(0, 5-roundLength))
	  resultflag = 0
	  if platform.system() == 'Windows':
		os.system('cls')
	  else:
		os.system('clear')
	  if platform.system() == 'Windows':
		os.system('cls')
	  else:
		os.system('clear')
	  # print x
	  winnerarray.append(x[0])
	  winneramount.append(int(x[5]))
	  standings[x[0]]['money'] -= int(x[5])
	  standings[x[0]][x[3]] += 1
	  if (x[0] == mybidderid):
		moneyleft -= int(x[5])
		myTypes[itemsinauction[j]] += 1
	  # update moneyleft, winnerarray
	else:
	  time.sleep(2)
  j+= 1
