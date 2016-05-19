from trectools import TrecRun

outfilename="baseline.task2.BM25_EN_run1.dat"

# Reads a run and save it in a pandas dataframe
run = TrecRun("./baseline.BM25_EN_Run1.dat")
df = run.run_data

# Get the qid for each group
df["qid"]  = df["query"].apply(lambda x: str(x)[0:3])

# Applies the rbp function to score documents for each qid group
rbp_p = .80
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
