from spot import Fetcher, spot
from datetime import datetime, timedelta
import os
import clash
import pandas as pd
import matplotlib.pyplot as plt

IDs1 = spot.GET_IDs('76561197970669109') #b4nny
IDs2 = spot.GET_IDs('76561198035712034') #slemnish

s3inv = clash.load_teams("invite_S3.json")
##
R2END = clash.season_dates['RGL2']['end']
R3END = clash.season_dates['RGL3']['end']
##
sink = 'object'
b4nny = clash.Player(IDs1, os.path.join("Z:\log_dumps", str(IDs1['64'])), s3inv, start=R2END, end=R3END, sink=sink) #the directory string could be empty if you're using sink object
slemnish = clash.Player(IDs2, os.path.join("Z:\log_dumps", str(IDs2['64'])), s3inv, start=R2END, end=R3END, sink=sink) #I'm sorry, I do not know who the pocket scout on Ascent is.

b4nny.get_data("DPM")
b4nny.ew()

slemnish.get_data("DPM")
slemnish.ew()

clash.QuickPlot({'b4nny': b4nny, 'slemnish': slemnish}, start=R2END, end=R3END)

#Standard scores should use the same log, a log where both players played, to be useful. Otherwise, the comparison isn't level. 2655155 is Map 2 of S3 finals.
#Typically when calculating standard score, you don't use a score from a game that's in the data. I do not care much about that for testing purposes.
b4nny_z = b4nny.std_score(2655155, "DPM") #Scrape the DPM from the given log, and calculate the standard score from that and the player's entire collection of logs.
slemnish_z = slemnish.std_score(2655155, "DPM")

print("Standard scores are for finals: b4nny: {}, slemnish: {}".format(b4nny_z, slemnish_z))
#This could probably be graphed in some interesting way.
