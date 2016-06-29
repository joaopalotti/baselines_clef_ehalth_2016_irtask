import sys
import codecs
import os
import warc
from glob import glob

fname = sys.argv[1]
outdir = sys.argv[2]

def find_file(filename):
    # E.g. "clueweb12-0002wb-99-19011"
    root = filename.split("-")[1]
    folder = root[0:2]
    warcf = filename.split("-")[2]
    warc_path = "/clueweb12b/DiskB/ClueWeb12_" + folder + "/" + root + "/" + root + "-" + warcf + ".warc.gz"
    w = warc.open(warc_path)
    for reg in w:
        if "warc-trec-id" not in reg.header.keys():
            continue
        if filename == reg.header["warc-trec-id"]:
            return reg.payload.read()
    return filename + "NOT FOUND"

with open(fname, "r") as fin:
    for file in fin:
        filename = file.strip()
        print("Processing " + filename)
        html = find_file(filename)
        # Removes warc boileplate
        html = html[html.find("<html"):]

        #fout = codecs.open(outdir + "/" + filename, "w", encoding="utf-8")
        fout = open(outdir + "/" + filename, "w")

        #fout.write(unicode(html, errors="replace"))
        #fout.write(html.decode("utf-8", "ignore"))
        #fout.write(html.encode("utf-8"))
        fout.write(html)

        fout.close()


