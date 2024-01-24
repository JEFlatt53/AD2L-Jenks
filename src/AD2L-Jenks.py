"""
Created on 20240122
@author: JEFlatt53
"""
#%% Import packages
from func import *
import statistics

#%% Get Inputs
rostersDir = input("Enter path to roster files: ")
nDivisions = int(input("Enter desired number of divisions: "))

while (clusterMethod := input("Cluster players or teams? (1=Player, 2=Team): ")) not in ['1', '2']: print("Invalid input. Please enter either '1' or '2'. ")

includeHeroic = bool(input("Include Heroic players? (y/n): "))

#%% Get Player/Team Metrics
combinedRosters = CombineRosters(rostersDir)
teams = Teams(combinedRosters)

if clusterMethod == '1':
    if includeHeroic:
        metric = list(combinedRosters['MMR'])
    else:
        metric = [mmr for mmr in combinedRosters['MMR'] if mmr <= 6050]

if clusterMethod == '2':
    metric = GetTeamMetric(teams, includeHeroic)

#%% Cluster
bounds = GetBounds(metric, nDivisions)

for team in teams:
    if any(mmr > 6050 for mmr in team['MMR']):
        continue
    meanMMR = round(statistics.mean(team['MMR']))
    medianMMR = round(statistics.median(team['MMR']))
    avgMedDevMMR = round(GetMD(team['MMR']))
    totalMMR = sum(team['MMR'])
    adjMMR = meanMMR + avgMedDevMMR
    team['MeanMMR'] = meanMMR
    team['MedianMMR'] = medianMMR
    team['TotalMMR'] = totalMMR
    team['AvgMedDevMMR'] = avgMedDevMMR
    team['AdjustedMMR'] = adjMMR

    if clusterMethod == '1':
        assignmentMetric = adjMMR
    if clusterMethod == '2':
        assignmentMetric = totalMMR

    for i, upperBound in enumerate(bounds):
        if adjMMR <= upperBound:
            team['Division'] = i
            break

roster = pd.concat(teams, ignore_index=True)
roster.to_csv(rostersDir + '/Roster.tsv', index=False, sep='\t')

assignments = roster.drop_duplicates(subset='TeamName')
assignments.to_csv(rostersDir + '/Teams.tsv', index=False, sep='\t')