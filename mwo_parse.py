import zipfile
import os
import sqlite3

# Connect to the database
conn = sqlite3.connect('mwo_season_stats.db')
c = conn.cursor()

# I ran this a lot in testing so these commands will clear out the database and rebuild the table
c.execute('''DROP TABLE IF EXISTS mwo_stats''')
c.execute('''CREATE TABLE IF NOT EXISTS mwo_stats ( Season INTEGER,
													Mech_Type TEXT,
													Pilot_Name TEXT,
													Total_Wins INTEGER,
													Total_Losses INTEGER,
													WL_Ratio REAL,
													Total_Kills INTEGER,
													Total_Deaths INTEGER,
													KD_Ratio REAL,
													Games_Played INTEGER,
													Average_Match_Score REAL)
	''')
conn.commit()

# Finds files in the current working directory
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
	if f[-3:] == 'zip':  # determines whether or not they're zip files
		season_number = f[:-4][6:]  # pulls the season number from the zip's name
		archive = zipfile.ZipFile(f, 'r')  # opens the zip file
		archive_files= archive.namelist()  # lists all the files in the zip
		for csv in archive_files:
			with archive.open(csv) as csvfile:
				csvfile.readline()  # need to read the first line to get rid of headers
				lines = csvfile.readlines()  # reads in all the data

			# determines the type of mech from the filename
			charts = ['global', 'assault', 'heavy', 'medium', 'light']
			mechtype = next(chart for chart in charts if chart in csv)

			for line in lines:
				l = str(line).replace('"', '').split(',')[1:][:-1]  # formats the individual lines into a list
				c.execute('''INSERT INTO mwo_stats (Season, Mech_Type, Pilot_Name, Total_Wins, Total_Losses, WL_Ratio, Total_Kills, Total_Deaths, KD_Ratio, Games_Played, Average_Match_Score)
							 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
							 (season_number, mechtype, l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8]))
conn.commit()
conn.close()
