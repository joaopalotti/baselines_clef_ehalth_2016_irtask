from trectools import TrecRun

import sys

if len(sys.argv) < 3:
    print "Usage: python rbp_fusion.py <input_run> <outputname> <rbp_p>"
    print "<input_run> can be a compressed file (bz2 or gzip) if you want to."
    sys.exit(0)

inputfile = sys.argv[1]
outfilename = sys.argv[2]
rbp_p = float(sys.argv[3])

# Reads a run and save it in a pandas dataframe
run = TrecRun(inputfile)
df = run.run_data

# Get the qid for each group
df["qid"]  = df["query"].apply(lambda x: str(x)[0:3])

# Applies the rbp function to score documents for each qid group
df["rbp_value"] = (1-rbp_p) * (rbp_p) ** (df["rank"]-1)
grouped_by_docid = df.groupby(["qid","docid"])["rbp_value"].sum().reset_index()

# Sort documents by rbp value inside each qid group
grouped_by_docid.sort_values(by=["qid","rbp_value"], ascending=[True,False], inplace=True)

# Add order field and retain only the top1000 for each group
grouped_by_docid["order"] = 1
grouped_by_docid["order"] = grouped_by_docid.groupby("qid")["order"].cumsum()
grouped_by_docid = grouped_by_docid[grouped_by_docid["order"] < 1001]

# Add Q0 field
grouped_by_docid["q0"] = "Q0"

# Add a run name
grouped_by_docid["runname"] = df["system"][0] + ".rbpmerged"

# Print results
grouped_by_docid[["qid","q0","docid","order","rbp_value","runname"]].to_csv(outfilename, index=False, sep=" ", header=False)
