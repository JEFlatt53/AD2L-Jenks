"""
Created on 20240122
@author: JEFlatt53
"""
#%% Import packages
from func import *
import statistics
from matplotlib import pyplot as plt

#%% Get Inputs
rostersDir = input("Enter path to roster files: ")
while (clusterMethod := input("Cluster by player MMR or team MMR? (1=Player, 2=Team): ")) not in ['1', '2']: print("Invalid input. Please enter either '1' or '2'. ")
includeHeroic = input("Include Heroic players? (y/n): ")
if includeHeroic.lower() == 'y' or includeHeroic.lower() == 't':
    includeHeroic = True
else:
    includeHeroic = False
nDivisions = int(input("Enter desired number of divisions: "))

#%% Get Player/Team Metrics
combinedRosters = CombineRosters(rostersDir)
teams = Teams(combinedRosters)

clusterMethods = {'1': 'Player', '2': 'Team'}

if clusterMethod == '1':
    if includeHeroic:
        metric = list(combinedRosters['MMR'])
    else:
        metric = [mmr for mmr in combinedRosters['MMR'] if mmr <= GetMMR('Immortal 2')]

if clusterMethod == '2':
    metric = GetTeamMetric(teams, includeHeroic)

#%% Cluster
bounds = GetBounds(metric, nDivisions)

for team in teams:
    if any(mmr > GetMMR('Immortal 2') for mmr in team['MMR']) and includeHeroic == False:
        continue
    meanMMR = round(statistics.mean(team['MMR']))
    medianMMR = round(statistics.median(team['MMR']))
    avgDevMMR = round(GetMD(team['MMR']))
    totalMMR = sum(team['MMR'])

    if clusterMethod == '1':
        assignmentMetric = meanMMR + avgDevMMR
    if clusterMethod == '2':
        assignmentMetric = totalMMR + (5*avgDevMMR)

    team['MeanMMR'] = meanMMR
    team['MedianMMR'] = medianMMR
    team['TotalMMR'] = totalMMR
    team['AvgDevMMR'] = avgDevMMR
    team['AdjustedMMR'] = assignmentMetric

    

    for i, upperBound in enumerate(bounds):
        if assignmentMetric <= upperBound:
            team['Division'] = i
            break

roster = pd.concat(teams, ignore_index=True).dropna()
floatCols = roster.select_dtypes(include=['float64'])
for col in floatCols.columns.values:
    roster[col] = roster[col].astype('int64')
roster.to_csv(rostersDir + '/Roster.tsv', index=False, sep='\t')

assignments = roster.drop_duplicates(subset='TeamName')
assignments.to_csv(rostersDir + '/Teams.tsv', index=False, sep='\t')

#%% Make Plots

info = 'Number of Divisions = ' + str(nDivisions) + '\n' + \
       'Includes Heroic? = ' + str(includeHeroic) + '\n' + \
       'Cluster Method = ' + clusterMethods[clusterMethod]
plt.figure()
plt.hist(assignments['Division'], bins=nDivisions)
plt.title('Division Assignments')
plt.xlabel('Division')
plt.ylabel('Number of Teams')
plt.text(0.01, -0.25, info, transform=plt.gca().transAxes)
plt.tight_layout()
plt.savefig(rostersDir + '/DivisionAssignments.png', dpi=300)

# %%
