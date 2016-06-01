import sys
import os
from trectools import TrecRun
import pandas as pd

fname = sys.argv[1] # The output of
participant = TrecRun(sys.argv[2])

metric = "GFI"

if metric ==  "GFI":
    m = "gunning_fog_index"
elif metric ==  "CLI":
    m="coleman_liau_index"

df = participant.run_data

rdata = pd.DataFrame.from_csv(fname).reset_index()

merged = pd.merge(df, rdata, left_on="docid", right_on="filename")

# Remove all the documents that justext was not able to extract text
merged = merged[merged["nsentences"] > 0]

# For example use coleman_liau_index: (because of CIKM paper)
merged = merged[merged[m] > 0]
merged["new_score"] = merged["score"] * 1. / merged[m]

dfsort = merged.sort_values(by=["query", "new_score"], ascending=[True, False])
dfsort["new_rank"] = 1
dfsort["new_rank"] = dfsort.groupby("query")["new_rank"].cumsum()

dfsort[["query","q0","docid","new_rank","new_score","system"]].to_csv("baseline.u" + metric + "_EN_Run1.txt", index=False, header=False, sep=" ")

