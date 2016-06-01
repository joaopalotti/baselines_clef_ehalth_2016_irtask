from trectools import TrecRun
import sys

participant_run=sys.argv[1]
outfilename=sys.argv[2]
X=int(sys.argv[3])

run = TrecRun(participant_run)
df = run.run_data
top = df.groupby(["query"])["docid"].head(X)

top.drop_duplicates().to_csv(outfilename, index=False)


