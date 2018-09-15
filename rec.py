# -*- coding: utf-8 -*-


from math import sqrt
from scipy.spatial import minkowski_distance
from scipy import stats

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
     'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
      'The Night Listener': 3.0},
      'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
           'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
            'You, Me and Dupree': 3.5}, 
      'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
           'Superman Returns': 3.5, 'The Night Listener': 4.0},
      'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
           'The Night Listener': 4.5, 'Superman Returns': 4.0, 
            'You, Me and Dupree': 2.5},
      'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
           'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
            'You, Me and Dupree': 2.0}, 
      'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
           'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
      'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


def sim_distance(prefs, p1, p2):
    si = {}
    for elt in prefs[p1]:
        if elt in prefs[p2]:
            si[elt] = 1
    
    if(len(si)) == 0:
        return 0

    sum_of_squares = sum(pow(prefs[p1][elt]-prefs[p2][elt],2) for elt in prefs[p1] if elt in prefs[p2])
    return 1/(1+sqrt(sum_of_squares))


def sim_person(prefs, p1, p2):
    si = {}
    for elt in prefs[p1]:
        if elt in prefs[p2]:
            si[elt] = 1
    n = len(si)

    if n == 0:
        return 0

    sum1 = sum(prefs[p1][it] for it in si)
    sum2 = sum(prefs[p2][it] for it in si)

    sum1sq = sum(pow(prefs[p1][it], 2) for it in si)
    sum2sq = sum(pow(prefs[p2][it], 2) for it in si)

    pSum = sum(prefs[p1][it] * prefs[p2][it] for it in si)

    num = pSum - (sum1*sum2)/n
    den = sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den == 0:
        return 1
    return num/den


# use scipy function
def sim_person2(prefs, p1, p2):
    si = {}
    for elt in prefs[p1]:
        if elt in prefs[p2]:
            si[elt] = 1
    n = len(si)

    if n == 0:
        return 0
    p1_lst = [prefs[p1][it] for it in si] 
    p2_lst = [prefs[p2][it] for it in si] 

    r = stats.pearsonr(p1_lst, p2_lst)
    return r[0]
    

def topMatches(prefs, person, n=5, similarity=sim_person):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[:n]



def getRecommendtions(prefs, person, similarity=sim_person2):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        
        if sim <=0:
            continue
        
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(total/simSums[item],item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def loadMovieLens(path='/home/hys/code/pci/datasets/ml-100k'):
    movies = {}
    with open(path+'/u.item', encoding='ISO-8859-1') as f:
        for line in f:
            (id,title) = line.split('|')[0:2]
            movies[id] = title

    prefs = {}
    with open(path+'/u.data',encoding='ISO-8859-1') as f:
        for line in f:
            (user, movieid, rating, ts) = line.split('\t')
            prefs.setdefault(user, {})
            prefs[user][movies[movieid]] = float(rating)
    return prefs
