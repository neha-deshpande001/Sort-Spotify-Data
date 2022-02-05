# Created by Neha Deshpande 2/4/2022
# 
# 						Instructions for use:
# 
# Download your Spotify data here: https://support.spotify.com/us/article/data-rights-and-privacy-settings/
# Move this file (SortSongs.py) into the folder \my_spotify_data\MyData\
# Run the following command from a terminal:
# 						python SortSongs.py
# 
# Two new files will be created - SortedSongs.txt and SortedArtists.txt.
# 
# SortedSongs.txt will be in the following format, with each line being a different song.
# 				Number of times played  --  Song Name  --  Artist Name
# 
# SortedArtists.txt will be in the following format, with each line being a different artist.
# 				Number of times played  --  Artist Name



import json

# add song and artist data to dictionaries
def sortData(fileName, allSongs, allArtists):
	file = open(fileName, encoding="utf8")
	data = json.load(file)
	file.close()

	for i in data:
		song = (i['trackName'], i['artistName'])
		if song in allSongs:
			allSongs[song] += 1
		else:
			allSongs[song] = 1

		artist = i['artistName']
		if artist in allArtists:
			allArtists[artist] += 1
		else:
			allArtists[artist] = 1

# add songs to dictionary
allSongs = {}
allArtists = {}
sortData('StreamingHistory0.json',allSongs, allArtists)
sortData('StreamingHistory1.json',allSongs, allArtists)

# sort dictionary in descending order by value
allSongs = dict(sorted(allSongs.items(), reverse=True, key=lambda item: item[1]))
allArtists = dict(sorted(allArtists.items(), reverse=True, key=lambda item: item[1]))


# write result to file
output = open("SortedSongs.txt", "w", encoding="utf8")
for i in allSongs:
	output.write(str(allSongs[i]) + "  --  " + i[0] + "  --  " + i[1] + "\n")
output.close()

output = open("SortedArtists.txt", "w", encoding="utf8")
for i in allArtists:
	output.write(str(allArtists[i]) + "  --  " + i + "\n")
output.close()
