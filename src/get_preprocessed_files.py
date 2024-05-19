from scipy.sparse import lil_matrix, load_npz
import numpy as np
import os

'''
The Full subset are sparse matrixes based on the LFM-2b dataset. Their shape is (users, tracks).
They are filtered for users with at least 5 interactions and tracks with at least 5 interactions. 
(meaning each remaining user has interacted with at least 5 tracks and 
each remaining track has been interacted with by at least 5 users)

Also, only interactions with a playcount of at least 2 are kept.

The Spotify data was filtered before preprocessing to only include tracks for which a Spotify URI exists in the Spotify subset.
This way, we ensure that only usable Spotify URIs remain.
Some of you might need this smaller subset if you want to use the Spotify API to get additional track information.


init_A_matrix includes the user-item interactions. It is a sparse matrix with shape (users, tracks) 
    and includes the counts of each user - item interaction
    
init_R_matrix includes the user-item interactions. It is a sparse matrix with shape (users, tracks)
    and includes the binary information about interactions of each user - item interaction


Remark that both subsets is also includes adult users! Filtering for child users should be done by you.

The mappings are of the form:
    user_index_map_inv: dict with index as key and user_id as value
    track_index_map_inv: dict with index as key and track_id as value
'''

def load_subsets():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    full_data = os.path.join(path, "data", "Processed_data", "Full Subset")
    spotify_data = os.path.join(path, "data", "Processed_data", "Spotify_Subset")

    #change here spotify_data or full_data
    matrixAdataPath = os.path.join(spotify_data, "init_A_matrix.npz")
    matrixRdataPath = os.path.join(spotify_data, "init_R_matrix.npz")
    mappingsPath = os.path.join(spotify_data, "init_mappings.npz")

    user_item_matrix = load_npz(matrixRdataPath)

    mappings = np.load(mappingsPath, allow_pickle=True)
    user_index_map_inv = mappings['user_index_map_inv'].item()
    track_index_map_inv = mappings['track_index_map_inv'].item()

    return user_index_map_inv, track_index_map_inv, user_item_matrix

#Some Notes: summed up values in matrix and the shape of the matrices:
#full_A :   1406552134 (117949, 4825739)
#full_R :    211590265 (117949, 4825739)
#spotify_A: 1168977644 (117337, 2238656)
#spotify_R:  171668326 (117337, 2238656)