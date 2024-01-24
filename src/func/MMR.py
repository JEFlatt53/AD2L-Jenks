import statistics

mmrLut = {
    'Herald 1': 154,
    'Herald 2': 308,
    'Herald 3': 462,
    'Herald 4': 616,
    'Herald 5': 769,
    'Guardian 1': 924,
    'Guardian 2': 1078,
    'Guardian 3': 1232,
    'Guardian 4': 1386,
    'Guardian 5': 1540,
    'Crusader 1': 1694,
    'Crusader 2': 1848,
    'Crusader 3': 2002,
    'Crusader 4': 2156,
    'Crusader 5': 2310,
    'Archon 1': 2464,
    'Archon 2': 2618,
    'Archon 3': 2772,
    'Archon 4': 2926,
    'Archon 5': 3080,
    'Legend 1': 3234,
    'Legend 2': 3388,
    'Legend 3': 3542,
    'Legend 4': 3696,
    'Legend 5': 3850,
    'Ancient 1': 4004,
    'Ancient 2': 4158,
    'Ancient 3': 4312,
    'Ancient 4': 4466,
    'Ancient 5': 4620,
    'Divine 1': 4820,
    'Divine 2': 5020,
    'Divine 3': 5220,
    'Divine 4': 5420,
    'Divine 5': 5620,
    'Immortal 1': 5800,
    'Immortal 2': 6050,
    'Immortal 3': 6300,
    'Immortal 4': 6550,
    'Immortal 5': 6800,
    'Immortal 6': 7050,
    'Immortal 7': 7300
}

def GetMMR(rank):
    try:
        return(mmrLut[rank])
    except:
        return(None)
    
def GetTeamMetric(teams, includeHeroic):
    teamMetrics = []
    for team in teams:
        if includeHeroic:
            teamMetrics.append(sum(team['MMR']))
        else:
            if any(mmr > 6050 for mmr in team['MMR']):
                continue
            else:
                teamMetrics.append(sum(team['MMR']))
    return teamMetrics

def GetMD(data):
    median = statistics.median(data)
    deviation = [x - median for x in data]
    mean_deviation = statistics.mean(deviation)
    return mean_deviation
