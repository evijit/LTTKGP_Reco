import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
import math
import operator


communitytag2vec = json.load(open("communitytag2vec.json","r"))
user2vec = json.load(open("user2vec.json","r"))
song2vec = json.load(open("song2vec.json","r"))
community_dict = json.load(open("community.json","r"))


def find_community(id):
    for key in community_dict.keys():
        user_list = community_dict[key]["user_list"]
        # print(user_list)
        if str(id) in user_list:
            return int(key)


    return -1



def get_reco(id):
    # userid = 1988535971173821 #Siddhant
    # userid = 2310747865617580 #Avijit
    # userid = 2038906389654139 #Apurva

    userid = id

    community_id = find_community(userid)


    user_vec = np.array(user2vec[str(userid)])
    communitytag_vec = np.array(communitytag2vec[str(community_id)])


    SELF_WEIGHT = 3/5
    COMMUNITY_WEIGHT = 2/5


    reco = {}

    for song in song2vec.keys():
        song_vec = np.array(song2vec[song])

        user_sim = 1 - cosine(user_vec, song_vec)
        comm_sim = 1 - cosine(communitytag_vec, song_vec)

        total_sim = (SELF_WEIGHT * user_sim) + (COMMUNITY_WEIGHT * comm_sim)

        if not math.isnan(total_sim): 
            reco[song] = total_sim


    reco = sorted(reco.items(), key=operator.itemgetter(1), reverse = True)
    # print(type(reco))

    for r in reco[:20] :
        print(r)

    return reco[:20]

