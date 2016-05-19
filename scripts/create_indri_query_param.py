import sys
import re

if len(sys.argv) < 2:
    print "Usage: python create_indri_query_param.py <path to queries2016.xml>"
    sys.exit(0)

use_indri_query_language = False

def process_phrase(m):
    s = m.group("exp")[1:-1] # remove the first and last chars as they are "'s
    if use_indri_query_language and len(s.split()) > 1:
        return "#1(" + s + ")"
    return s

def process(query):
    query = re.sub('(?P<exp>"[\w\s]+")', process_phrase, query)

    # remove some punctuation marks
    query = re.sub("[\W]", " ", query)

    if use_indri_query_language:
        return "#combine(" + query + ")"
    return query

inputrun = sys.argv[1]

num_results = 1000
index_path = "/clueweb12b/indri/index"
run_id="baselineIndri"

print "<parameters>"
print "<count>%d</count>" % (num_results)
print "<index>%s</index>" % (index_path)
print "<runID>%s</runID>" % (run_id)
print "<threads>8</threads>"
print "<trecFormat>true</trecFormat>"

with open(inputrun, "r") as f:
    for line in f.readlines():
        if "<id>" in line:
            qid = re.match("<id>(?P<id>\w*)</id>", line.strip(), re.I).group('id')

        elif "<title>" in line:
            title = re.match("<title>(?P<title>[\w\W\s]*)</title>", line.strip(), re.I).group('title')

        elif "</query>" in line:
            print "\t<query>"
            print "\t\t<id>%s</id>" % (qid)
            print "\t\t<text>%s</text>" % (process(title))
            print "\t</query>"


print "</parameters>"




