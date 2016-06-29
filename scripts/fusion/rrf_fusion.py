from trectools import TrecRun
# Reciprocal rank fusion outperforms condorcet and individual rank learning methods
# http://dl.acm.org/citation.cfm?id=1572114

import sys

if len(sys.argv) < 3:
    print "Usage: python rrf_fusion.py <input_run> <outputname> <rrf_k>"
    print "<input_run> can be a compressed file (bz2 or gzip) if you want to."
    sys.exit(0)

inputfile = sys.argv[1]
outfilename = sys.argv[2]
rrf_k = float(sys.argv[3])

# Reads a run and save it in a pandas dataframe
run = TrecRun(inputfile)
df = run.run_data

# Get the qid for each group
df["qid"]  = df["query"].apply(lambda x: str(x)[0:3])

# Applies the rrf function to score documents for each qid group
df["rrf_value"] = 1.0 / (rrf_k + df["rank"])
grouped_by_docid = df.groupby(["qid","docid"])["rrf_value"].sum().reset_index()

# Sort documents by rrf value inside each qid group
grouped_by_docid.sort_values(by=["qid","rrf_value"], ascending=[True,False], inplace=True)

# Add order field and retain only the top1000 for each group
grouped_by_docid["order"] = 1
grouped_by_docid["order"] = grouped_by_docid.groupby("qid")["order"].cumsum()
grouped_by_docid = grouped_by_docid[grouped_by_docid["order"] < 1001]

# Add Q0 field
grouped_by_docid["q0"] = "Q0"

# Add a run name
grouped_by_docid["runname"] = df["system"][0] + ".rrf_k%d_merged" % (rrf_k)

# Print results
grouped_by_docid[["qid","q0","docid","order","rrf_value","runname"]].to_csv(outfilename, index=False, sep=" ", header=False)
