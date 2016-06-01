import pandas as pd
import os
from trectools import TrecRun
import sys


if len(sys.argv) < 2:
    print "Usage: python spam_filter.py <input_run> <spam_t>"
    print "<input_run> can be a compressed file (bz2 or gzip) if you want to."
    sys.exit(0)

inputfile = sys.argv[1] # some participant or baseline run
X = int(sys.argv[2])


spam_folder = "/clueweb12b/spamscores/waterloo-spam-cw12-decoded/"

# Reads a run and save it in a pandas dataframe
run = TrecRun(inputfile)
df = run.run_data

def getspam(docid):
    code = docid.split("-")[1]
    cmd = "zgrep " + docid + " " + spam_folder + "cw12-" + code + ".spamPct.gz | cut -f 1 -d' '"
    stream = os.popen(cmd)
    return stream.read().strip()

topX = df.groupby(["query"])["docid"].head(X)
topX = topX.drop_duplicates().reset_index()
topX["spam"] = topX["docid"].apply(getspam)

topX[["docid","spam"]].to_csv("spam_bm25_top" + str(X) + ".txt", index=False, header=True)

