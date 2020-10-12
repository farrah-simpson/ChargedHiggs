import os, sys
import time
import getopt
import argparse
import ROOT as r
import varsList
import numpy as np
import uproot
import pandas as pd
import root_pandas
from root_pandas import to_root
from ROOT import TMVA
from ROOT import RDataFrame
import xgboost as xgb
from xgboost import XGBClassifier
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


parser = argparse.ArgumentParser(description='Apply XGB for charged Higgs search')
parser.add_argument("-k", "--varListKey", default="NewVar", help="Input variable list")
parser.add_argument("-f", "--file", default="ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8_hadd.root", help="The name of the input file")
parser.add_argument("-l", "--label", help="The label for the output file")

args = parser.parse_args()

selList = [["NJetsCSV_JetSubCalc", ""],  ["NJets_JetSubCalc", ""], ["isElectron", ""], ["isMuon", ""], ["leptonPt_MultiLepCalc", ""]]
weightList = [["pileupWeight", ""], ["lepIdSF", ""], ["EGammaGsfSF", ""], ["MCWeight_MultiLepCalc", ""]]
varListKey = args.varListKey
varList = varsList.varList[varListKey]
inputDir = varsList.inputDir
infname = args.file#"ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8_hadd.root"

print "Loading Signal Sample"

sig_tree = uproot.open(inputDir+infname)["ljmet"]
sig_df = sig_tree.pandas.df(branches=(iVar[0] for iVar in varList+selList+weightList))

sig_selected = (sig_df["NJets_JetSubCalc"]>4)&(sig_df["NJetsCSV_JetSubCalc"]>1)&( ((sig_df["leptonPt_MultiLepCalc"]>35)&(sig_df["isElectron"]==True))|((sig_df["leptonPt_MultiLepCalc"]>30)&(sig_df["isMuon"]==True)))

sig_df = sig_df[sig_selected]

#print "Loading Background Samples"
#back_dfs = []
#
#bkgList = varsList.bkg
#for ibkg in bkgList:
#    print ibkg
#    bkg_tree = uproot.open(inputDir+ibkg)["ljmet"]
#    bkg_df = bkg_tree.pandas.df(branches=(iVar[0] for iVar in varList+selList+weightList))
#    print bkg_df
#    bkg_selected = (bkg_df["NJets_JetSubCalc"]>4)&(bkg_df["NJetsCSV_JetSubCalc"]>1)&( ((bkg_df["leptonPt_MultiLepCalc"]>35)&(bkg_df["isElectron"]==True))|((bkg_df["leptonPt_MultiLepCalc"]>30)&(bkg_df["isMuon"]==True)))
#    bkg_df = bkg_df[bkg_selected]
#    print bkg_df
#    back_dfs.append(bkg_df)
#
#bkgall_df = pd.concat(back_dfs)
#del back_dfs

sig_df.loc[:,"isSignal"] = np.ones(sig_df.shape[0])
#bkgall_df.loc[:, "isSignal"] = np.zeros(bkgall_df.shape[0])

#dfall = pd.concat([sig_df, bkgall_df])

train_var = []
for ivar in varList:
    train_var.append(ivar[0])
train_var.append("isSignal")
sigdf_var = sig_df.loc[:, train_var]

NDIM = len(sigdf_var.columns)
dataset = sigdf_var.values

X = dataset[:, 0:NDIM-1]
Y = dataset[:, NDIM-1]


features = train_var[0:NDIM-1]

dX = xgb.DMatrix(X, feature_names=features)

bst = xgb.Booster()
bst.load_model("XGB500iterations_4depths_signal_region_NewVar_.model")#("XGB500iterations_4depths_signal_region.model")

sigdf_var.loc[:, "XGB"] = bst.predict(dX)

print sigdf_var

sigdf_var.to_root("XGBTree_"+args.label+".root", key="XGB_Tree")

