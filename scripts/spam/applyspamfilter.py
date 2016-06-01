import sys
import os
from trectools import TrecRun
import pandas as pd

spam_fname = sys.argv[1] # The output of spam_filter.py
participant = TrecRun(sys.argv[2])
spamP = int(sys.argv[3])

df = participant.run_data

rdata = pd.DataFrame.from_csv(spam_fname).reset_index()

merged = pd.merge(df, rdata, how="outer")

# documents that we dont know the spam score we do not remove
merged["spam"] = merged["spam"].fillna(100)

# Removed results that have spam < than spamP
merged = merged[merged["spam"] >= spamP]

dfsort = merged.sort_values(by=["query", "score"], ascending=[True, False])
dfsort["new_rank"] = 1
dfsort["new_rank"] = dfsort.groupby("query")["new_rank"].cumsum()

dfsort[["query","q0","docid","new_rank","score","system"]].to_csv("baseline.spam" + str(spamP) + "_EN_Run1.txt", index=False, header=False, sep=" ")


