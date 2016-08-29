import sys
import re

if len(sys.argv) < 2:
    print "Usage: python map_indri_qid.py <input_run>"
    sys.exit(0)

inputrun = sys.argv[1]

id_map = {}
qid_base = 100
for i in range(0,300):
    variable = i % 6
    if variable == 0:
        qid_base += 1

    new_id = "%s%03d" % (str(qid_base), variable + 1)
    id_map[str(i)] = new_id

with open(inputrun, "r") as f:
    for line in f.readlines():
        fields = re.split("\s+", line.strip())
        #print fields
        fields[0] = id_map[fields[0]]
        print " ".join(fields)






