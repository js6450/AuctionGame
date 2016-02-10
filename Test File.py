import random

inputFile = open("test data.txt", "r")
lines = inputFile.readlines()
for i in range(len(lines)):
	lines[i] = lines[i].strip()
itemsinauction = lines[0].split(" ")
winnerarray = lines[1].split(" ")
winneramount = list(map(int, lines[2].split(" ")))
players = lines[3].split(" ")
artists = lines[4].split(" ")


def determinebid(itemsinauction, winnerarray, winneramount, numberbidders, players, artists, standings, rd):
  #Write smart stuff here
  '''You have all the variables and lists you could need in the arguments of the function,
  these will always be updated and relevant, so all you have to do is use them.
  Write code to make your bot do a lot of smart stuff to beat all the other bots. Good luck,
  and may the games begin!
  '''

  '''
  itemsinauction is a list where at index "rd" the item in that round is being sold is displayed.

  winnerarray is a list where at index "rd" the winner of the item sold in that round is displayed.

  winneramount is a list where at index "rd" the amount of money paid for the item sold in that round is displayed.

  example: I will now construct a sentence that would be correct if you substituted the outputs of the lists:
  In round 5 winnerarray[4] bought itemsinauction[4] for winneramount[4] dirhams/dollars/money unit.

  numberbidders is an integer displaying the amount of people playing the auction game.

  players is a list containing all the names of the current players.

  artists is a list containing all the names of the artists (paintings) that are for sale in our auction.

  standings is a set of nested dictionaries (standings is a dictionary that for each person has another dictionary
  associated with them). standings[name][artist] will return how many paintings "artist" the player "name" currently has
  standings[name]['money'] (remember quotes for string, important!) returns how much money the player "name" has left.

  rd is the current round in 0 based indexing.

  Good luck!
  '''
  return int(30*random.random())


standings = {name: {artist: 0 for artist in artists} for name in players}
for name in players:
	standings[name]['money'] = 100
for index in range(i):
	standings[winnerarray[index]][itemsinauction[index]] += 1
	standings[winnerarray[index]]['money'] -= winneramount[index]

print(determinebid(itemsinauction, winnerarray, winneramount, len(players), players, artists, standings, len(winnerarray)))