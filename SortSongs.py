# Created by Neha Deshpande 2/4/2022
# 
# 						Instructions for use:
# 
# Download your Spotify data here: https://support.spotify.com/us/article/data-rights-and-privacy-settings/
# Move this file (SortSongs.py) into the folder \my_spotify_data\MyData\
# Run the following command from a terminal:
# 						python SortSongs.py
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
