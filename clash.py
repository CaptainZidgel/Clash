from spot import Fetcher, spot
from steam.steamid import SteamID
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

def load_teams(file):
    with open(file, 'r') as f:
        j = json.load(f)
        f = {}
        for team in j:
            f[team] = {}
            for player, id in j[team].items():
                f[team][player] = {}
                f[team][player]["id"] = SteamID(id).as_steam3
                f[team][player]["team"] = team
        return f

season_dates = spot.tf2seasons.all_seasons

def player_lookup(id, m_teams):
    for team in m_teams:
        for name, steam3 in m_teams[team]:
            if id == steam3:
                return (name, steam3, team)


def is_scrim(log, league_teams):
    match_teams = {}
    match_teams["Red"] = set()
    match_teams["Blue"] = set()
    for steam3, player_stats in log['players'].items():
        match_teams[player_stats['team']].add(steam3)
    red, blu = False, False
    for teamname, team in league_teams.items():
        ids = {x["id"] for x in team.values()}
        '''
        print("TEAM")
        print(sorted(match_teams["Red"]))
        print("IDS")
        print(sorted(ids))
        '''
        if len(match_teams["Red"] & ids) >= 5: #Allow 1 sub
            red = True
        if len(match_teams["Blue"] & ids) >= 5:
            blu = True
    return red and blu


class Player:
    def __init__(self, IDs, directory, team_list, start=datetime(2000, 1, 1), end=datetime(2040, 1, 1), sink='file'):
        if not sink in {'file', 'object'}:
            raise Exception("Unknown sink: must be 'file' or 'object', not {}".format(sink))
        self.directory = directory
        self.IDs = IDs
        self.e = spot.Extract(IDs)
        print("Fetching for player {} with {} sink".format(IDs['3'], sink))
        fetcher = Fetcher(sink=sink, IDs=IDs, save_directory=directory, precondition=lambda l: start <= datetime.fromtimestamp(l['date']) <= end)
        self.logs = [l for l in fetcher.fetch(do_file_return=True if sink=='file' else False) if start <= datetime.fromtimestamp(l['info']['date']) <= end] #Using this list comp to double check the precondition for cached files.
        print("Filtering logs for player {}".format(IDs['3']))
        self.plotter = spot.Plotter(self.logs)
        approver = spot.Approver(IDs, self.plotter, spot.PLAYEDFULL)
        approver.Custom(lambda l: is_scrim(l, team_list))
        approver.Finalize()
        self.data = []

    def get_data(self, stat):
        self.data = self.plotter.get_timestamped_values(getattr(self.e, stat))
        return self.data

    def ew(self):
        self.data = self.data.expanding(5).mean()


class QuickPlot:
    def __init__(self, players, start, end):
        if not type(players) == dict:
            raise Exception("players must be a dict of Player objects, keyed with a username")
        fig, ax1 = plt.subplots()
        for name, player in players.items():
            if len(player.data) == 0:
                raise Exception("Missing data. Did you call Player.get_data()?")
            try:
                ax1.plot(player.data.index, player.data.val, label=name)
            except AttributeError:
                ax1.plot(player.data.index, player.data.values, label=name)
            for lab, s in season_dates.items():
                if start <= s['start'] <= end or start <= s['end'] <= end:
                    ax1.axvspan(s['start'], s['end'], alpha=0.1, color="gray")
                    ax1.text(s['start'], ax1.get_ylim()[0], lab, rotation=90, fontsize='small')
            player.plotter.set_xbounds(ax1, (None, None))
        ax1.legend()
        fig.show()
