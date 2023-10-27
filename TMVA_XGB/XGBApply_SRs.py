import os, sys
import time
import getopt
import argparse
import ROOT
import array
import varsList
import numpy as np
import uproot
import pandas as pd
import math 
from math import sqrt
#import root_pandas
#from root_pandas import to_root
#from ROOT import TMVA
#from ROOT import RDataFrame
import xgboost as xgb
from xgboost import XGBClassifier
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

############################################################
# Copy the entire step-2 TTree, add XGB, save to a new TTree
############################################################

parser = argparse.ArgumentParser(description='Apply XGB for charged Higgs search')
parser.add_argument("-l", "--varListKey", default="NewVar", help="Input variable list")
parser.add_argument("-f", "--file", default="ChargedHiggs_HplusTB_HplusToTB_M-1000_13TeV_amcatnlo_pythia8_hadd.root", help="The name of the input file")
#parser.add_argument("-m", "--model", default=""),
parser.add_argument("-o", "--output", default="NewOutput", help="The label for the output file")

args = parser.parse_args()

varListKey = args.varListKey
varList = varsList.varList[varListKey]
inputDir = varsList.bkginputDir
infname = args.file

def Reshape(x):
   y = 0.5*(sqrt( (x+1)/2 ) + math.pow((x+1)/2, 12))
   return y 

print("Load Input File")

#bst200 = xgb.Booster()
#bst200.load_model("XGB_M200_SRAll.model")
#
#bst220 = xgb.Booster()
#bst220.load_model("XGB_M220_SRAll.model")
#
#bst250 = xgb.Booster()
#bst250.load_model("XGB_M250_SRAll.model")
#
#bst300 = xgb.Booster()
#bst300.load_model("XGB_M300_SRAll.model")
#
#bst350 = xgb.Booster()
#bst350.load_model("XGB_M350_SRAll.model")
#
#bst400 = xgb.Booster()
#bst400.load_model("XGB_M400_SRAll.model")
#
#bst500 = xgb.Booster()
#bst500.load_model("XGB_M500_SRAll.model")
#
#bst600 = xgb.Booster()
#bst600.load_model("XGB_M600_SRAll.model")
#
#bst700 = xgb.Booster()
#bst700.load_model("XGB_M700_SRAll.model")
#
#bst800 = xgb.Booster()
#bst800.load_model("XGB_M800_SRAll.model")
#
#bst1000 = xgb.Booster()
#bst1000.load_model("XGB_M1000_SRAll.model")
#
#bst1250 = xgb.Booster()
#bst1250.load_model("XGB_M1250_SRAll.model")
#
#bst1500 = xgb.Booster()
#bst1500.load_model("XGB_M1500_SRAll.model")
#
#bst1750 = xgb.Booster()
#bst1750.load_model("XGB_M1750_SRAll.model")
#
#bst2000 = xgb.Booster()
#bst2000.load_model("XGB_M2000_SRAll.model")
#
#bst2500 = xgb.Booster()
#bst2500.load_model("XGB_M2500_SRAll.model")
#
#bst3000 = xgb.Booster()
#bst3000.load_model("XGB_M3000_SRAll.model")

bst200_SR1 = xgb.Booster()
bst200_SR1.load_model("XGB_M200_SR1.model")

bst220_SR1 = xgb.Booster()
bst220_SR1.load_model("XGB_M220_SR1.model")

bst250_SR1 = xgb.Booster()
bst250_SR1.load_model("XGB_M250_SR1.model")

bst300_SR1 = xgb.Booster()
bst300_SR1.load_model("XGB_M300_SR1.model")

bst350_SR1 = xgb.Booster()
bst350_SR1.load_model("XGB_M350_SR1.model")

bst400_SR1 = xgb.Booster()
bst400_SR1.load_model("XGB_M400_SR1.model")

bst500_SR1 = xgb.Booster()
bst500_SR1.load_model("XGB_M500_SR1.model")

bst600_SR1 = xgb.Booster()
bst600_SR1.load_model("XGB_M600_SR1.model")

bst700_SR1 = xgb.Booster()
bst700_SR1.load_model("XGB_M700_SR1.model")

bst800_SR1 = xgb.Booster()
bst800_SR1.load_model("XGB_M800_SR1.model")

bst1000_SR1 = xgb.Booster()
bst1000_SR1.load_model("XGB_M1000_SR1.model")

bst1250_SR1 = xgb.Booster()
bst1250_SR1.load_model("XGB_M1250_SR1.model")

bst1500_SR1 = xgb.Booster()
bst1500_SR1.load_model("XGB_M1500_SR1.model")

bst1750_SR1 = xgb.Booster()
bst1750_SR1.load_model("XGB_M1750_SR1.model")

bst2000_SR1 = xgb.Booster()
bst2000_SR1.load_model("XGB_M2000_SR1.model")

bst2500_SR1 = xgb.Booster()
bst2500_SR1.load_model("XGB_M2500_SR1.model")

bst3000_SR1 = xgb.Booster()
bst3000_SR1.load_model("XGB_M3000_SR1.model")

bst200_SR2 = xgb.Booster()
bst200_SR2.load_model("XGB_M200_SR2.model")

bst220_SR2 = xgb.Booster()
bst220_SR2.load_model("XGB_M220_SR2.model")

bst250_SR2 = xgb.Booster()
bst250_SR2.load_model("XGB_M250_SR2.model")

bst300_SR2 = xgb.Booster()
bst300_SR2.load_model("XGB_M300_SR2.model")

bst350_SR2 = xgb.Booster()
bst350_SR2.load_model("XGB_M350_SR2.model")

bst400_SR2 = xgb.Booster()
bst400_SR2.load_model("XGB_M400_SR2.model")

bst500_SR2 = xgb.Booster()
bst500_SR2.load_model("XGB_M500_SR2.model")

bst600_SR2 = xgb.Booster()
bst600_SR2.load_model("XGB_M600_SR2.model")

bst700_SR2 = xgb.Booster()
bst700_SR2.load_model("XGB_M700_SR2.model")

bst800_SR2 = xgb.Booster()
bst800_SR2.load_model("XGB_M800_SR2.model")

bst1000_SR2 = xgb.Booster()
bst1000_SR2.load_model("XGB_M1000_SR2.model")

bst1250_SR2 = xgb.Booster()
bst1250_SR2.load_model("XGB_M1250_SR2.model")

bst1500_SR2 = xgb.Booster()
bst1500_SR2.load_model("XGB_M1500_SR2.model")

bst1750_SR2 = xgb.Booster()
bst1750_SR2.load_model("XGB_M1750_SR2.model")

bst2000_SR2 = xgb.Booster()
bst2000_SR2.load_model("XGB_M2000_SR2.model")

bst2500_SR2 = xgb.Booster()
bst2500_SR2.load_model("XGB_M2500_SR2.model")

bst3000_SR2 = xgb.Booster()
bst3000_SR2.load_model("XGB_M3000_SR2.model")

bst200_SR3 = xgb.Booster()
bst200_SR3.load_model("XGB_M200_SR3.model")

bst220_SR3 = xgb.Booster()
bst220_SR3.load_model("XGB_M220_SR3.model")

bst250_SR3 = xgb.Booster()
bst250_SR3.load_model("XGB_M250_SR3.model")

bst300_SR3 = xgb.Booster()
bst300_SR3.load_model("XGB_M300_SR3.model")

bst350_SR3 = xgb.Booster()
bst350_SR3.load_model("XGB_M350_SR3.model")

bst400_SR3 = xgb.Booster()
bst400_SR3.load_model("XGB_M400_SR3.model")

bst500_SR3 = xgb.Booster()
bst500_SR3.load_model("XGB_M500_SR3.model")

bst600_SR3 = xgb.Booster()
bst600_SR3.load_model("XGB_M600_SR3.model")

bst700_SR3 = xgb.Booster()
bst700_SR3.load_model("XGB_M700_SR3.model")

bst800_SR3 = xgb.Booster()
bst800_SR3.load_model("XGB_M800_SR3.model")

bst1000_SR3 = xgb.Booster()
bst1000_SR3.load_model("XGB_M1000_SR3.model")

bst1250_SR3 = xgb.Booster()
bst1250_SR3.load_model("XGB_M1250_SR3.model")

bst1500_SR3 = xgb.Booster()
bst1500_SR3.load_model("XGB_M1500_SR3.model")

bst1750_SR3 = xgb.Booster()
bst1750_SR3.load_model("XGB_M1750_SR3.model")

bst2000_SR3 = xgb.Booster()
bst2000_SR3.load_model("XGB_M2000_SR3.model")

bst2500_SR3 = xgb.Booster()
bst2500_SR3.load_model("XGB_M2500_SR3.model")

bst3000_SR3 = xgb.Booster()
bst3000_SR3.load_model("XGB_M3000_SR3.model")



train_var = []
varList.sort()
for ivar in varList:
    train_var.append(ivar[0])
#sig_tree = uproot.open(inputDir+infname)["ljmet"]
sig_tree = uproot.open(infname)["ljmet"]
numentries = sig_tree.numentries

tfile = ROOT.TFile.Open(infname)
ttree = tfile.Get("ljmet")

outputname = args.output+".root"
newfile = ROOT.TFile(outputname, "RECREATE")
newfile.cd()

newtree = ttree.CloneTree(0)
 
#XGB200 = array.array('d', [0])
#XGB220 = array.array('d', [0])
#XGB250 = array.array('d', [0])
#XGB300 = array.array('d', [0])
#XGB350 = array.array('d', [0])
#XGB400 = array.array('d', [0])
#XGB500 = array.array('d', [0])
#XGB600 = array.array('d', [0])
#XGB700 = array.array('d', [0])
#XGB800 = array.array('d', [0])
#XGB1000 = array.array('d', [0])
#XGB1250 = array.array('d', [0])
#XGB1500 = array.array('d', [0])
#XGB1750 = array.array('d', [0])
#XGB2000 = array.array('d', [0])
#XGB2500 = array.array('d', [0])
#XGB3000 = array.array('d', [0])

XGB200_SR1 = array.array('d', [0])
XGB220_SR1 = array.array('d', [0])
XGB250_SR1 = array.array('d', [0])
XGB300_SR1 = array.array('d', [0])
XGB350_SR1 = array.array('d', [0])
XGB400_SR1 = array.array('d', [0])
XGB500_SR1 = array.array('d', [0])
XGB600_SR1 = array.array('d', [0])
XGB700_SR1 = array.array('d', [0])
XGB800_SR1 = array.array('d', [0])
XGB1000_SR1 = array.array('d', [0])
XGB1250_SR1 = array.array('d', [0])
XGB1500_SR1 = array.array('d', [0])
XGB1750_SR1 = array.array('d', [0])
XGB2000_SR1 = array.array('d', [0])
XGB2500_SR1 = array.array('d', [0])
XGB3000_SR1 = array.array('d', [0])

XGB200_SR2 = array.array('d', [0])
XGB220_SR2 = array.array('d', [0])
XGB250_SR2 = array.array('d', [0])
XGB300_SR2 = array.array('d', [0])
XGB350_SR2 = array.array('d', [0])
XGB400_SR2 = array.array('d', [0])
XGB500_SR2 = array.array('d', [0])
XGB600_SR2 = array.array('d', [0])
XGB700_SR2 = array.array('d', [0])
XGB800_SR2 = array.array('d', [0])
XGB1000_SR2 = array.array('d', [0])
XGB1250_SR2 = array.array('d', [0])
XGB1500_SR2 = array.array('d', [0])
XGB1750_SR2 = array.array('d', [0])
XGB2000_SR2 = array.array('d', [0])
XGB2500_SR2 = array.array('d', [0])
XGB3000_SR2 = array.array('d', [0])

XGB200_SR3 = array.array('d', [0])
XGB220_SR3 = array.array('d', [0])
XGB250_SR3 = array.array('d', [0])
XGB300_SR3 = array.array('d', [0])
XGB350_SR3 = array.array('d', [0])
XGB400_SR3 = array.array('d', [0])
XGB500_SR3 = array.array('d', [0])
XGB600_SR3 = array.array('d', [0])
XGB700_SR3 = array.array('d', [0])
XGB800_SR3 = array.array('d', [0])
XGB1000_SR3 = array.array('d', [0])
XGB1250_SR3 = array.array('d', [0])
XGB1500_SR3 = array.array('d', [0])
XGB1750_SR3 = array.array('d', [0])
XGB2000_SR3 = array.array('d', [0])
XGB2500_SR3 = array.array('d', [0])
XGB3000_SR3 = array.array('d', [0])

#newtree.Branch("XGB200", XGB200, "XGB200/D")
#newtree.Branch("XGB220", XGB220, "XGB220/D")
#newtree.Branch("XGB250", XGB250, "XGB250/D")
#newtree.Branch("XGB300", XGB300, "XGB300/D")
#newtree.Branch("XGB350", XGB350, "XGB350/D")
#newtree.Branch("XGB400", XGB400, "XGB400/D")
#newtree.Branch("XGB500", XGB500, "XGB500/D")
#newtree.Branch("XGB600", XGB600, "XGB600/D")
#newtree.Branch("XGB700", XGB700, "XGB700/D")
#newtree.Branch("XGB800", XGB800, "XGB800/D")
#newtree.Branch("XGB1000", XGB1000, "XGB1000/D")
#newtree.Branch("XGB1250", XGB1250, "XGB1250/D")
#newtree.Branch("XGB1500", XGB1500, "XGB1500/D")
#newtree.Branch("XGB1750", XGB1750, "XGB1750/D")
#newtree.Branch("XGB2000", XGB2000, "XGB2000/D")
#newtree.Branch("XGB2500", XGB2500, "XGB2500/D")
#newtree.Branch("XGB3000", XGB3000, "XGB3000/D")

newtree.Branch("XGB200_SR1", XGB200_SR1, "XGB200_SR1/D")
newtree.Branch("XGB220_SR1", XGB220_SR1, "XGB220_SR1/D")
newtree.Branch("XGB250_SR1", XGB250_SR1, "XGB250_SR1/D")
newtree.Branch("XGB300_SR1", XGB300_SR1, "XGB300_SR1/D")
newtree.Branch("XGB350_SR1", XGB350_SR1, "XGB350_SR1/D")
newtree.Branch("XGB400_SR1", XGB400_SR1, "XGB400_SR1/D")
newtree.Branch("XGB500_SR1", XGB500_SR1, "XGB500_SR1/D")
newtree.Branch("XGB600_SR1", XGB600_SR1, "XGB600_SR1/D")
newtree.Branch("XGB700_SR1", XGB700_SR1, "XGB700_SR1/D")
newtree.Branch("XGB800_SR1", XGB800_SR1, "XGB800_SR1/D")
newtree.Branch("XGB1000_SR1", XGB1000_SR1, "XGB1000_SR1/D")
newtree.Branch("XGB1250_SR1", XGB1250_SR1, "XGB1250_SR1/D")
newtree.Branch("XGB1500_SR1", XGB1500_SR1, "XGB1500_SR1/D")
newtree.Branch("XGB1750_SR1", XGB1750_SR1, "XGB1750_SR1/D")
newtree.Branch("XGB2000_SR1", XGB2000_SR1, "XGB2000_SR1/D")
newtree.Branch("XGB2500_SR1", XGB2500_SR1, "XGB2500_SR1/D")
newtree.Branch("XGB3000_SR1", XGB3000_SR1, "XGB3000_SR1/D")


newtree.Branch("XGB200_SR2", XGB200_SR2, "XGB200_SR2/D")
newtree.Branch("XGB220_SR2", XGB220_SR2, "XGB220_SR2/D")
newtree.Branch("XGB250_SR2", XGB250_SR2, "XGB250_SR2/D")
newtree.Branch("XGB300_SR2", XGB300_SR2, "XGB300_SR2/D")
newtree.Branch("XGB350_SR2", XGB350_SR2, "XGB350_SR2/D")
newtree.Branch("XGB400_SR2", XGB400_SR2, "XGB400_SR2/D")
newtree.Branch("XGB500_SR2", XGB500_SR2, "XGB500_SR2/D")
newtree.Branch("XGB600_SR2", XGB600_SR2, "XGB600_SR2/D")
newtree.Branch("XGB700_SR2", XGB700_SR2, "XGB700_SR2/D")
newtree.Branch("XGB800_SR2", XGB800_SR2, "XGB800_SR2/D")
newtree.Branch("XGB1000_SR2", XGB1000_SR2, "XGB1000_SR2/D")
newtree.Branch("XGB1250_SR2", XGB1250_SR2, "XGB1250_SR2/D")
newtree.Branch("XGB1500_SR2", XGB1500_SR2, "XGB1500_SR2/D")
newtree.Branch("XGB1750_SR2", XGB1750_SR2, "XGB1750_SR2/D")
newtree.Branch("XGB2000_SR2", XGB2000_SR2, "XGB2000_SR2/D")
newtree.Branch("XGB2500_SR2", XGB2500_SR2, "XGB2500_SR2/D")
newtree.Branch("XGB3000_SR2", XGB3000_SR2, "XGB3000_SR2/D")


newtree.Branch("XGB200_SR3", XGB200_SR3, "XGB200_SR3/D")
newtree.Branch("XGB220_SR3", XGB220_SR3, "XGB220_SR3/D")
newtree.Branch("XGB250_SR3", XGB250_SR3, "XGB250_SR3/D")
newtree.Branch("XGB300_SR3", XGB300_SR3, "XGB300_SR3/D")
newtree.Branch("XGB350_SR3", XGB350_SR3, "XGB350_SR3/D")
newtree.Branch("XGB400_SR3", XGB400_SR3, "XGB400_SR3/D")
newtree.Branch("XGB500_SR3", XGB500_SR3, "XGB500_SR3/D")
newtree.Branch("XGB600_SR3", XGB600_SR3, "XGB600_SR3/D")
newtree.Branch("XGB700_SR3", XGB700_SR3, "XGB700_SR3/D")
newtree.Branch("XGB800_SR3", XGB800_SR3, "XGB800_SR3/D")
newtree.Branch("XGB1000_SR3", XGB1000_SR3, "XGB1000_SR3/D")
newtree.Branch("XGB1250_SR3", XGB1250_SR3, "XGB1250_SR3/D")
newtree.Branch("XGB1500_SR3", XGB1500_SR3, "XGB1500_SR3/D")
newtree.Branch("XGB1750_SR3", XGB1750_SR3, "XGB1750_SR3/D")
newtree.Branch("XGB2000_SR3", XGB2000_SR3, "XGB2000_SR3/D")
newtree.Branch("XGB2500_SR3", XGB2500_SR3, "XGB2500_SR3/D")
newtree.Branch("XGB3000_SR3", XGB3000_SR3, "XGB3000_SR3/D")


iev=0
#XGB300_arrays = []
#XGB500_arrays = []
#XGB800_arrays = []
#XGB1000_arrays = []

print "Compute XGB"

#for chunk in sig_tree.iterate("*", entrysteps=1000, namedecode="utf-8"):
for chunk in sig_tree.iterate("*", entrysteps=1000):
    array_var=[]
    for var in train_var:
        array_var.append(chunk[var])
    dataset = np.column_stack(array_var)
    dX = xgb.DMatrix(dataset, feature_names=train_var)
    #XGB200_pred = bst200.predict(dX)
    #XGB220_pred = bst220.predict(dX)
    #XGB250_pred = bst250.predict(dX)
    #XGB300_pred = bst300.predict(dX)
    #XGB350_pred = bst350.predict(dX)
    #XGB400_pred = bst400.predict(dX)
    #XGB500_pred = bst500.predict(dX)
    #XGB600_pred = bst600.predict(dX)
    #XGB700_pred = bst700.predict(dX)
    #XGB800_pred = bst800.predict(dX)
    #XGB1000_pred = bst1000.predict(dX)
    #XGB1250_pred = bst1250.predict(dX)
    #XGB1500_pred = bst1500.predict(dX)
    #XGB1750_pred = bst1750.predict(dX)
    #XGB2000_pred = bst2000.predict(dX)
    #XGB2500_pred = bst2500.predict(dX)
    #XGB3000_pred = bst3000.predict(dX)

    XGB200_SR1_pred = bst200_SR1.predict(dX)
    XGB220_SR1_pred = bst220_SR1.predict(dX)
    XGB250_SR1_pred = bst250_SR1.predict(dX)
    XGB300_SR1_pred = bst300_SR1.predict(dX)
    XGB350_SR1_pred = bst350_SR1.predict(dX)
    XGB400_SR1_pred = bst400_SR1.predict(dX)
    XGB500_SR1_pred = bst500_SR1.predict(dX)
    XGB600_SR1_pred = bst600_SR1.predict(dX)
    XGB700_SR1_pred = bst700_SR1.predict(dX)
    XGB800_SR1_pred = bst800_SR1.predict(dX)
    XGB1000_SR1_pred = bst1000_SR1.predict(dX)
    XGB1250_SR1_pred = bst1250_SR1.predict(dX)
    XGB1500_SR1_pred = bst1500_SR1.predict(dX)
    XGB1750_SR1_pred = bst1750_SR1.predict(dX)
    XGB2000_SR1_pred = bst2000_SR1.predict(dX)
    XGB2500_SR1_pred = bst2500_SR1.predict(dX)
    XGB3000_SR1_pred = bst3000_SR1.predict(dX)

    XGB200_SR2_pred = bst200_SR2.predict(dX)
    XGB220_SR2_pred = bst220_SR2.predict(dX)
    XGB250_SR2_pred = bst250_SR2.predict(dX)
    XGB300_SR2_pred = bst300_SR2.predict(dX)
    XGB350_SR2_pred = bst350_SR2.predict(dX)
    XGB400_SR2_pred = bst400_SR2.predict(dX)
    XGB500_SR2_pred = bst500_SR2.predict(dX)
    XGB600_SR2_pred = bst600_SR2.predict(dX)
    XGB700_SR2_pred = bst700_SR2.predict(dX)
    XGB800_SR2_pred = bst800_SR2.predict(dX)
    XGB1000_SR2_pred = bst1000_SR2.predict(dX)
    XGB1250_SR2_pred = bst1250_SR2.predict(dX)
    XGB1500_SR2_pred = bst1500_SR2.predict(dX)
    XGB1750_SR2_pred = bst1750_SR2.predict(dX)
    XGB2000_SR2_pred = bst2000_SR2.predict(dX)
    XGB2500_SR2_pred = bst2500_SR2.predict(dX)
    XGB3000_SR2_pred = bst3000_SR2.predict(dX)

    XGB200_SR3_pred = bst200_SR3.predict(dX)
    XGB220_SR3_pred = bst220_SR3.predict(dX)
    XGB250_SR3_pred = bst250_SR3.predict(dX)
    XGB300_SR3_pred = bst300_SR3.predict(dX)
    XGB350_SR3_pred = bst350_SR3.predict(dX)
    XGB400_SR3_pred = bst400_SR3.predict(dX)
    XGB500_SR3_pred = bst500_SR3.predict(dX)
    XGB600_SR3_pred = bst600_SR3.predict(dX)
    XGB700_SR3_pred = bst700_SR3.predict(dX)
    XGB800_SR3_pred = bst800_SR3.predict(dX)
    XGB1000_SR3_pred = bst1000_SR3.predict(dX)
    XGB1250_SR3_pred = bst1250_SR3.predict(dX)
    XGB1500_SR3_pred = bst1500_SR3.predict(dX)
    XGB1750_SR3_pred = bst1750_SR3.predict(dX)
    XGB2000_SR3_pred = bst2000_SR3.predict(dX)
    XGB2500_SR3_pred = bst2500_SR3.predict(dX)
    XGB3000_SR3_pred = bst3000_SR3.predict(dX)

    #ichunk+=1
    chunck_size = len(XGB300_SR1_pred)
    for k in range(chunck_size):
        if iev%100000==0:
            print(iev)
        #XGB200[0] = XGB200_pred[k]
        #XGB220[0] = XGB220_pred[k]
        #XGB250[0] = XGB250_pred[k]
        #XGB300[0] = XGB300_pred[k]
        #XGB350[0] = XGB350_pred[k]
        #XGB400[0] = XGB400_pred[k]
        #XGB500[0] = XGB500_pred[k]
        #XGB600[0] = XGB600_pred[k]
        #XGB700[0] = XGB700_pred[k]
        #XGB800[0] = XGB800_pred[k]
        #XGB1000[0] = XGB1000_pred[k]
        #XGB1250[0] = XGB1250_pred[k]
        #XGB1500[0] = XGB1500_pred[k]
        #XGB1750[0] = XGB1750_pred[k]
        #XGB2000[0] = XGB2000_pred[k]
        #XGB2500[0] = XGB2500_pred[k]
        #XGB3000[0] = XGB3000_pred[k]

        XGB200_SR1[0] = XGB200_SR1_pred[k]
        XGB220_SR1[0] = XGB220_SR1_pred[k]
        XGB250_SR1[0] = XGB250_SR1_pred[k]
        XGB300_SR1[0] = XGB300_SR1_pred[k]
        XGB350_SR1[0] = XGB350_SR1_pred[k]
        XGB400_SR1[0] = XGB400_SR1_pred[k]
        XGB500_SR1[0] = XGB500_SR1_pred[k]
        XGB600_SR1[0] = XGB600_SR1_pred[k]
        XGB700_SR1[0] = XGB700_SR1_pred[k]
        XGB800_SR1[0] = XGB800_SR1_pred[k]
        XGB1000_SR1[0] = XGB1000_SR1_pred[k]
        XGB1250_SR1[0] = XGB1250_SR1_pred[k]
        XGB1500_SR1[0] = XGB1500_SR1_pred[k]
        XGB1750_SR1[0] = XGB1750_SR1_pred[k]
        XGB2000_SR1[0] = XGB2000_SR1_pred[k]
        XGB2500_SR1[0] = XGB2500_SR1_pred[k]
        XGB3000_SR1[0] = XGB3000_SR1_pred[k]

        XGB200_SR2[0] = XGB200_SR2_pred[k]
        XGB220_SR2[0] = XGB220_SR2_pred[k]
        XGB250_SR2[0] = XGB250_SR2_pred[k]
        XGB300_SR2[0] = XGB300_SR2_pred[k]
        XGB350_SR2[0] = XGB350_SR2_pred[k]
        XGB400_SR2[0] = XGB400_SR2_pred[k]
        XGB500_SR2[0] = XGB500_SR2_pred[k]
        XGB600_SR2[0] = XGB600_SR2_pred[k]
        XGB700_SR2[0] = XGB700_SR2_pred[k]
        XGB800_SR2[0] = XGB800_SR2_pred[k]
        XGB1000_SR2[0] = XGB1000_SR2_pred[k]
        XGB1250_SR2[0] = XGB1250_SR2_pred[k]
        XGB1500_SR2[0] = XGB1500_SR2_pred[k]
        XGB1750_SR2[0] = XGB1750_SR2_pred[k]
        XGB2000_SR2[0] = XGB2000_SR2_pred[k]
        XGB2500_SR2[0] = XGB2500_SR2_pred[k]
        XGB3000_SR2[0] = XGB3000_SR2_pred[k]

        XGB200_SR3[0] = XGB200_SR3_pred[k]
        XGB220_SR3[0] = XGB220_SR3_pred[k]
        XGB250_SR3[0] = XGB250_SR3_pred[k]
        XGB300_SR3[0] = XGB300_SR3_pred[k]
        XGB350_SR3[0] = XGB350_SR3_pred[k]
        XGB400_SR3[0] = XGB400_SR3_pred[k]
        XGB500_SR3[0] = XGB500_SR3_pred[k]
        XGB600_SR3[0] = XGB600_SR3_pred[k]
        XGB700_SR3[0] = XGB700_SR3_pred[k]
        XGB800_SR3[0] = XGB800_SR3_pred[k]
        XGB1000_SR3[0] = XGB1000_SR3_pred[k]
        XGB1250_SR3[0] = XGB1250_SR3_pred[k]
        XGB1500_SR3[0] = XGB1500_SR3_pred[k]
        XGB1750_SR3[0] = XGB1750_SR3_pred[k]
        XGB2000_SR3[0] = XGB2000_SR3_pred[k]
        XGB2500_SR3[0] = XGB2500_SR3_pred[k]
        XGB3000_SR3[0] = XGB3000_SR3_pred[k]



        ttree.GetEntry(iev)
        newtree.Fill()
        iev+=1

#nentries = ttree.GetEntries()
#
#    idx = iev%10000
#    XGB800[0] = XGB800_arrays[nchunk][idx]
#    XGB1000[0] = XGB1000_arrays[nchunk][idx]
#    newtree.Fill()

print newtree.GetEntries()
newfile.WriteTObject(newtree, "ljmet")
newfile.Close()

