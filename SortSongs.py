# Created by Neha Deshpande 2/4/2022
# 
# 						Instructions for use:
# 
# 1. Download your Spotify data here: https://support.spotify.com/us/article/data-rights-and-privacy-settings/
# 2. Move this file (SortSongs.py) into the folder \my_spotify_data\MyData\
# 3. Run the following command from a terminal:
# 						python SortSongs.py
# To graph your top songs and artists, run the following. [Number] is how many you want to graph, default is 5:
# 						python SortSongs.py -graph [Number]
# 
# Three new files will be created - SortedSongs.txt, SortedArtists.txt, and SortedLikedSongs.txt
# 
# SortedSongs.txt will be in the following format, with each line being a different song.
# 				Number of times played  --  Song Name  --  Artist Name
# 
# SortedArtists.txt will be in the following format, with each line being a different artist.
# 				Number of times played  --  Artist Name
#
# SortedLikedSongs.txt displays the number of times each of the liked songs are played. It
# will be in the following format, with each line being a different artist. 
# 				Number of times played  --  Song Name  --  Artist Name

import json
import os
import re
import sys

# add song and artist data to dictionaries
def sortData(fileName, allSongs, allArtists, likedSongs):
	file = open(fileName, encoding="utf8")
	data = json.load(file)
	file.close()

	for i in data:
		song = (i['trackName'], i['artistName'])
		if song in allSongs:
			allSongs[song] += 1
		else:
			allSongs[song] = 1

		if song in likedSongs:
			likedSongs[song] += 1

		artist = i['artistName']
		if artist in allArtists:
			allArtists[artist] += 1
		else:
			allArtists[artist] = 1

# add songs to dictionary
allSongs = {}
allArtists = {}
likedSongs = {}

# make a list of all liked songs
file = open('YourLibrary.json')
data = json.load(file)
file.close()
for i in data['tracks']:
	song = (i['track'], i['artist'])
	likedSongs[song] = 0

# check which files in the current directory match this regex pattern
# e.x. StreamingHistory0.json
regex = re.compile("^(StreamingHistory[0-9]+\.json)$")
for file in os.listdir(os.getcwd()):
    if regex.match(file):
        sortData(file, allSongs, allArtists, likedSongs)

# sort dictionary in descending order by value
allSongs = dict(sorted(allSongs.items(), reverse=True, key=lambda item: item[1]))
allArtists = dict(sorted(allArtists.items(), reverse=True, key=lambda item: item[1]))
likedSongs = dict(sorted(likedSongs.items(), reverse=True, key=lambda item: item[1]))



# write result to file
output = open("SortedSongs.txt", "w", encoding="utf8")
output.write("All Streamed Songs\n\n")
for i in allSongs:
	output.write(str(allSongs[i]) + "  --  " + i[0] + "  --  " + i[1] + "\n")
output.close()

output = open("SortedArtists.txt", "w", encoding="utf8")
output.write("All Streamed Artists\n\n")
for i in allArtists:
	output.write(str(allArtists[i]) + "  --  " + i + "\n")
output.close()

output = open("SortedLikedSongs.txt", "w", encoding="utf8")
output.write("All Liked Songs\n\n")
for i in likedSongs:
	output.write(str(likedSongs[i]) + "  --  " + i[0] + "  --  " + i[1] + "\n")
output.close()


print("Data added to SortedSongs.txt, SortedArtists.txt, and SortedLikedSongs.txt")

# create bar graphs
if len(sys.argv) >= 2 and sys.argv[1] == '-graph':
    
    # command line arg is how many songs/artists to display
    numToDisplay = 5
    if len(sys.argv) == 3 and sys.argv[2].isdigit():
        numToDisplay = int(sys.argv[2])

    # import only if graphing
    import matplotlib.pyplot as plt
    from collections import Counter

    # FIRST GRAPH
    # keep track of songs
    xSongs = []
    ySongs = []
    for i in Counter(allSongs).most_common(numToDisplay):
        xSongs.append(i[0][0] + "\nby " + i[0][1])
        ySongs.append(i[1])
      
    fig = plt.figure(figsize=(10,6))
     
    # create a bar plot
    plt.bar(xSongs, ySongs, color ='crimson')
    
    plt.xlabel("Song", weight = 'bold')
    plt.ylabel("Number of Listens", weight = 'bold')
    plt.title("Your Top " + str(numToDisplay) + " Songs", weight='bold')


    # add numbers to label each bar
    for index, value in enumerate(ySongs):
        plt.text(index, value + ySongs[0] * 0.01, str(value), ha="center")
    plt.savefig('SortedSongs.png')

    # SECOND GRAPH
    # keep track of artists
    xArtists = []
    yArtists = []
    for i in Counter(allArtists).most_common(numToDisplay):
        xArtists.append(i[0])
        yArtists.append(i[1])
      
    fig = plt.figure(figsize=(10,6))
     
    # create a bar plot
    plt.bar(xArtists, yArtists, color ='darkorchid')
    
    plt.xlabel("Artist", weight = 'bold')
    plt.ylabel("Number of Listens", weight = 'bold')
    plt.title("Your Top " + str(numToDisplay) + " Artists", weight='bold')

    # add numbers to label each bar
    for index, value in enumerate(yArtists):
        plt.text(index, value + yArtists[0] * 0.01, str(value), ha="center")
    plt.savefig('SortedArtists.png')
    print("Top " + str(numToDisplay) + " graphs saved!")

else:
    print("Hint: try \'-graph #\' to visualize your top # songs and artists!")

