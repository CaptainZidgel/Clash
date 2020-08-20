from spot import Fetcher, spot
from datetime import datetime
import os
import clash
import pandas as pd
import matplotlib.pyplot as plt

IDs1 = spot.GET_IDs('76561197970669109') #b4nny
IDs2 = spot.GET_IDs('76561198035712034') #slemnish

seasons = spot.tf2seasons.all_seasons

s3inv = clash.load_teams("invite_S3.json")
##
R2END = clash.season_dates['RGL2']['end']
R3END = clash.season_dates['RGL3']['end']
##
b4nny = clash.Player(IDs1, os.path.join("Z:\log_dumps", str(IDs1['64'])), s3inv, start=R2END, end=R3END, sink='object') #the directory string could be empty if you're using sink object
slemnish = clash.Player(IDs2, os.path.join("Z:\log_dumps", str(IDs2['64'])), s3inv, start=R2END, end=R3END, sink='object')

b4nny.get_data("DPM")
b4nny.ew()

slemnish.get_data("DPM")
slemnish.ew()

clash.QuickPlot({'b4nny': b4nny, 'slemnish': slemnish}, start=R2END, end=R3END)

'''
fig, ax1 = plt.subplots()
p1.shade_seasons(ax1)
ax1.plot(weekly.index, weekly.val, label="yung b4niel")
ax1.plot(weekly.index, [v-40 for v in weekly.val], label="young man")

ax1.legend()

fig.show()

'''
