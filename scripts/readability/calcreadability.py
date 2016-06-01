import sys
import os
import csv
import codecs
import warc
import justext
from glob import glob
from readcalc import readcalc

fname = sys.argv[1] # a simple list with one file per row
outfile = fname + ".csv"

def get_list_of_readability(calc):
    return [len(calc.get_words()), len(calc.get_sentences()),calc.get_flesch_reading_ease(), calc.get_flesch_kincaid_grade_level(),\
	    calc.get_coleman_liau_index(), calc.get_gunning_fog_index(), calc.get_smog_index(), calc.get_ari_index(),
	    calc.get_lix_index(), calc.get_dale_chall_score()]

def get_text(html):
    paragraphs = justext.justext(html, justext.get_stoplist('English'))
    text = ""
    for paragraph in paragraphs:
    	if not paragraph.is_boilerplate: # and not paragraph.is_header:
            text = text + paragraph.text + ". "
    return text

csv_file = open(outfile, 'wb')
csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerow(["filename", "nwords", "nsentences", "flesch_reading_ease", "flesch_kincaid_grade_level", "coleman_liau_index",\
                     "gunning_fog_index", "smog_index", "ari_index", "lix_index", "dale_chall_score"])


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
        html = find_file(filename)
        text = get_text(html.decode("utf-8", 'ignore'))
        rc = readcalc.ReadCalc(text)
        row = get_list_of_readability(rc)
	csv_writer.writerow([filename] + row)

csv_file.close()

