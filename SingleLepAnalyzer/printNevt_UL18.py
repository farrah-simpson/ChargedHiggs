import ROOT
import sys, os 
import argparse

import json 

from samples import *

parser = argparse.ArgumentParser(description="Print out the number of events for each sample")

#parser.add_argument("-f", "--file", default="", help="The path to the input file")
parser.add_argument("-i", "--inputdir", default="/isilon/hadoop/store/user/dali/FWLJMET106XUL_singleLep2018UL_RunIISummer20_3t_step1hadds/nominal", help="The path to the step1hadds directory (background samples)")
parser.add_argument("-s", "--sigdir", default="/isilon/hadoop/store/group/bruxljmFWLJMET106XUL_singleLep2018UL_RunIISummer20_3t_step1hadds/nominal", help="The path to the step1hadds directory (signal samples)")
parser.add_argument("-y", "--year", default="18")

args = parser.parse_args()


nRun_dict = {}
flavs = ["_tt1b", "_tt2b", "_ttbb", "_ttcc", "_ttjj"]
N = 10

keys = samples.keys()
keys.sort() 

for key in keys:
    if "Data" in key:
        continue

    if "TTTo" in key:
        if "TTToSemiLeptonic" in key:
            inputfile = args.inputdir+"/"+samples[key]+"_HT0Njet0_tt1b_hadd.root"
            tfile = ROOT.TFile(inputfile)
            NevtHist = tfile.Get("NumTrueHist")
            nRun_total = NevtHist.Integral() 
            #nRun_total=0
            #for iflav in flavs:
            #    inputfile_HT500Njet9 = args.inputdir+"/"+samples[key]+"_HT500Njet9"+iflav+"_hadd.root"
            #    tfile_HT500Njet9 = ROOT.TFile(inputfile_HT500Njet9)
            #    NevtHist = tfile_HT500Njet9.Get("NumTrueHist")
            #    nRun_total+=NevtHist.Integral()
            #    if not iflav=="_ttjj":
            #        inputfile_HT0Njet0 = args.inputdir+"/"+samples[key]+"_HT0Njet0"+iflav+"_hadd.root"
            #        tfile_HT0Njet0 = ROOT.TFile(inputfile_HT0Njet0)
            #        NevtHist = tfile_HT500Njet9.Get("NumTrueHist")
            #        nRun_total+=NevtHist.Integral()
            #    else:
            #        for i in range(1, N+1):
            #            inputfile_HT0Njet0 = args.inputdir+"/"+samples[key]+"_HT0Njet0"+iflav+"_"+str(i)+"_hadd.root"
            #            tfile_HT0Njet0 = ROOT.TFile(inputfile_HT0Njet0)
            #            NevtHist = tfile_HT0Njet0.Get("NumTrueHist")
            #            nRun_total+=NevtHist.Integral()
            nRun_dict[key] = nRun_total
            print(key, nRun_dict[key])

        else:
            nRun_total=0
            #for iflav in flavs:
            inputfile = args.inputdir+"/"+samples[key]+"_tt1b_hadd.root"
            tfile = ROOT.TFile(inputfile)
            NevtHist = tfile.Get("NumTrueHist")
            nRun_total+=NevtHist.Integral()
            nRun_dict[key] = nRun_total
            print(key, nRun_dict[key])
            
    if "Hptb" in key:
        inputfile = args.sigdir+"/"+samples[key]+"_hadd.root"
        tfile = ROOT.TFile(inputfile)
        NevtHist = tfile.Get("NumTrueHist")
        nRun_dict[key] = NevtHist.Integral()
        print(key, nRun_dict[key])

                
            
    if ("TTTo" not in key) and ("Hptb" not in key) :
        print(key)
        inputfile = args.inputdir+"/"+samples[key]+"_hadd.root"
        tfile = ROOT.TFile(inputfile)
        NevtHist = tfile.Get("NumTrueHist")
        nRun_dict[key] = NevtHist.Integral()
        print(key, nRun_dict[key])
        



nRunfile = open("nRun_UL"+args.year+".py", "w")

nRunfile.write("#!/usr/bin/python\n")

keys = nRun_dict.keys()

keys.sort()

for key in keys:

    nRunfile.write('nRun_origin["'+key+'"] = '+str(nRun_dict[key])+'\n')




