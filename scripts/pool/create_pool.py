from trectools import misc, TrecRun, TrecPool
import numpy as np
from glob import glob

class CLEFTrecRun(TrecRun):
    def modify_query_ids(self):
        self.run_data["query"] = self.run_data["query"].apply(lambda x: int(str(x)[0:3]))

def createCLEFTrecRun(r):
    tr = TrecRun(r)
    tr.__class__ = CLEFTrecRun
    tr.modify_query_ids()
    return tr

def create_pool_from_filenames(files):
    runs = []
    for r in files:
        tr = createCLEFTrecRun(r)
        runs.append(tr)

    return misc.make_pool(runs, strategy='rbp', topX=1000, rbp_strategy='sum', rbp_p=0.8)

runs = {"task1":[], "task2":[], "task3": []}
for t in ["CUNI", "ecnu", "GUIR", "Infolab", "KDEIR", "KISTI", "MayoNLPTeam", "MRIM", "ub-botswana", "WHUIRGroup"]:
    runs["task1"].extend(glob("/home/palotti/clef2016_submissions/" + t + "/IRTask1/*Run[123].txt.gz"))
    runs["task2"].extend(glob("/home/palotti/clef2016_submissions/" + t + "/IRTask2/*Run[123].txt.gz"))
    #runs["task3"].extend(glob("/home/palotti/clef2016_submissions/" + t + "/IRTask3/*Run[123].txt.gz"))

runs["bl_terrier_task1"] = glob("/home/palotti/baselines_clef_ehalth_2016_irtask/irtask1/terrier/*Run[123].txt.gz")
runs["bl_indri_task1"] = glob("/home/palotti/baselines_clef_ehalth_2016_irtask/irtask1/indri/*Run[123].txt.gz")
runs["bl_terrier_task2"] = glob("/home/palotti/baselines_clef_ehalth_2016_irtask/irtask2/terrier/*Run[123].txt.gz")
runs["bl_indri_task2"] = glob("/home/palotti/baselines_clef_ehalth_2016_irtask/irtask2/indri/*Run[123].txt.gz")

runs["readability"] = glob("/home/palotti/baselines_clef_ehalth_2016_irtask/irtask1/readability/*Run[123].txt.gz")
runs["spam"] = glob("/home/palotti/baselines_clef_ehalth_2016_irtask/irtask1/spam/*Run[123].txt.gz")


run_list = []
for l in runs.values():
    run_list.extend(l)

pool = create_pool_from_filenames(run_list)

def check_cov(run_list, pool, topX=10):
    covs = []
    for r in run_list:
        tr = createCLEFTrecRun(r)
        covs.append(pool.check_coverage(tr, topX=topX))
    return covs

def who(value, cov_list, run_list):
    return run_list[cov_list.index(value)]


