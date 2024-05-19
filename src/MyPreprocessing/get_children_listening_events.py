import numpy as np
import pandas as pd
import sys

sys.path.insert(0, '/Users/str1ct0wn3r/Documents/RP/src')

from get_preprocessed_files import load_subsets

#data = pd.read_csv('/Users/str1ct0wn3r/Documents/RP/data/raw/listening-counts.tsv.bz2')

#print("One")
user_index, track_index, u_t_matrix = load_subsets()

user_data = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/user-data/users.tsv.bz2", delimiter="\t")
print("Two")

AGE_LOWER = 6
AGE_UPPER = 17
user_id_age = {}

for x in user_data.to_numpy():
    user_id_age[x[0]] = x[2]

new_data = list()

coo_matrix = u_t_matrix.tocoo()

t = 0
# Step 3: Iterate over non-zero entries
for row, col, value in zip(coo_matrix.row, coo_matrix.col, coo_matrix.data):
    #t += 1
    if value > 0 and AGE_LOWER <= user_id_age[user_index[row]] <= AGE_UPPER:
        new_data.append(track_index[col])

#for i in range(len(user_index)):
#    if AGE_LOWER <= user_id_age[user_index[i]] <= AGE_UPPER:
#        for j in range(len(track_index)):
#            #print(i, j, u_t_matrix)
#            if u_t_matrix[i,j] > 0:
#                new_data.append(track_index[j])

pd.DataFrame(data=new_data, columns=['track_id']).drop_duplicates().to_csv("/Users/str1ct0wn3r/Documents/RP/data/Filtered_Data/left_songs.csv", index=False)