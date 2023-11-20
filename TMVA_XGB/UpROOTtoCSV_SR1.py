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
#from ROOT import RDataFrame
import xgboost as xgb
from xgboost import XGBClassifier
import sklearn 
from sklearn.datasets import dump_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 

parser = argparse.ArgumentParser(description='Convert pandas dataframe to libsvm')
parser.add_argument("-k", "--varListKey", default="NewVar", help="Input variable list")
parser.add_argument("-l", "--label", default="", help="label for output file")
parser.add_argument("-m", "--mass", default="500", help="The signal mass point")


args = parser.parse_args()


selList = [["NJetsCSV_JetSubCalc", ""],["NJets_JetSubCalc", ""], ["leptonPt_MultiLepCalc", ""],  ["isElectron", ""], ["isMuon", ""], ["isTraining", ""]]
weightList = [["pileupWeight", ""], ["lepIdSF", ""], ["EGammaGsfSF", ""], ["MCWeight_MultiLepCalc", ""]] 
varListKey = args.varListKey
varList = varsList.varList[varListKey]
siginputDir = varsList.siginputDir
bkginputDir = varsList.bkginputDir
infname = "PairVLQ_x53x53_tWtW_narrow_RH_M"+str(args.mass)+"_TuneCP5_13TeV-madgraph-pythia8_hadd.root"

print "Loading Signal Sample"

sig_tree = uproot.open(siginputDir+infname)["ljmet"]
sig_df = sig_tree.pandas.df(branches=(iVar[0] for iVar in varList+selList+weightList))

#Event Selection
 
sig_selected = ((sig_df["isTraining"]==1)|(sig_df["isTraining"]==2))&(sig_df["NJets_JetSubCalc"]>3)&(sig_df["NJetsCSV_JetSubCalc"]>0)&( ((sig_df["leptonPt_MultiLepCalc"]>35)&(sig_df["isElectron"]==True))|((sig_df["leptonPt_MultiLepCalc"]>30)&(sig_df["isMuon"]==True))) 

sig_df = sig_df[sig_selected]

print "Loading Background Samples"
back_dfs = []

bkgList = varsList.bkg
for ibkg in bkgList:
    print ibkg
    bkg_tree = uproot.open(bkginputDir+ibkg)["ljmet"]
    bkg_df = bkg_tree.pandas.df(branches=(iVar[0] for iVar in varList+selList+weightList))
    print bkg_df
    bkg_selected = ((bkg_df["isTraining"]==1)|(bkg_df["isTraining"]==2))&(bkg_df["NJets_JetSubCalc"]>4)&(bkg_df["NJetsCSV_JetSubCalc"]==2)&( ((bkg_df["leptonPt_MultiLepCalc"]>35)&(bkg_df["isElectron"]==True))|((bkg_df["leptonPt_MultiLepCalc"]>30)&(bkg_df["isMuon"]==True)))
    bkg_df = bkg_df[bkg_selected]
    print bkg_df
    back_dfs.append(bkg_df)

#print back_dfs
bkgall_df = pd.concat(back_dfs)
del back_dfs

#compute Weights 
weightSig = sig_df['pileupWeight']*sig_df['lepIdSF']*sig_df['EGammaGsfSF']*sig_df['MCWeight_MultiLepCalc']/(abs(sig_df['MCWeight_MultiLepCalc']))
weightBkg = bkgall_df['pileupWeight']*bkgall_df['lepIdSF']*bkgall_df['EGammaGsfSF']*bkgall_df['MCWeight_MultiLepCalc']/(abs(bkgall_df['MCWeight_MultiLepCalc']))

sigtotalWeight = np.sum(weightSig)
bkgtotalWeight = np.sum(weightBkg)

print "Signal Weights:", weightSig
print "Background Weights:", weightBkg
#compute the weight ratio to balance the training for XGBoost
scale = float(bkgtotalWeight)/float(sigtotalWeight)

print "SCALE", scale

randnum = np.random.rand(sig_df.shape[0]+bkgall_df.shape[0])
isTrain = randnum>0.2

#assign label
sig_df.loc[:,"isSignal"] = np.ones(sig_df.shape[0])
bkgall_df.loc[:, "isSignal"] = np.zeros(bkgall_df.shape[0])

dfall = pd.concat([sig_df, bkgall_df])

weightall = np.append(weightSig, weightBkg)




train_var = ["isSignal"]
varList.sort()
for ivar in varList:
    train_var.append(ivar[0])
#train_var.append("isSignal")
dfall_var = dfall.loc[:, train_var]

print dfall_var

dfall_train = dfall_var[isTrain]
dfall_test = dfall_var[isTrain==False]

#print "Columns:", dfall.columns
#print "dfall_var cloumns:", dfall_var.columns
#d_train = dfall_train[np.setdiff1d(dfall_var.columns, ['idx', 'isSignal'])]
#labels_train = dfall_train['isSignal']

#d_test = dfall_test[np.setdiff1d(dfall_var.columns, ['idx', 'isSignal'])]

#labels_test = dfall_test['isSignal']
dfall_train.to_csv("dtrainM"+args.mass+".csv", index=False)
dfall_test.to_csv("dtestM"+args.mass+".csv", index=False)


#
#NDIM = len(dfall_var.columns)
#dataset = dfall_var.values
#
#X = dataset[:, 0:NDIM-1]
#Y = dataset[:, NDIM-1]
#
#dfall_var.loc[:, "isTrain"] = isTrain
#dfall_var.loc[:, "Weight"] = weightall
#print Y
#
#
##X_train_val, X_test, Y_train_val, Y_test, weight_train_val, weight_test = train_test_split(X, Y, weightall, test_size=0.3, random_state=7)
#
#X_train_val = X[isTrain]
#Y_train_val = Y[isTrain]
#weight_train_val = weightall[isTrain]
#
#X_test = X[isTrain==False]
#Y_test = Y[isTrain==False]
#weight_test = weightall[isTrain==False]
#
#features = train_var[0:NDIM-1]
#print features
#print len(features)
#print X_test.shape[1]
##del isTrain
##del weightall
##del dfall
#
#dall = xgb.DMatrix(X, feature_names=features)
#dtrain = xgb.DMatrix(X_train_val, label=Y_train_val, weight=weight_train_val, feature_names=features)
#dtest = xgb.DMatrix(X_test, label=Y_test, weight=weight_test, feature_names=features)
#watchlist = [(dtrain, 'train'), (dtest, 'eval')]#[(dtest, 'eval'), (dtrain, 'train')]
#param = {
#    'max_depth': 2,  # the maximum depth of each tree
#    'eta': 0.05,  # the training step for each iteration
#    'silent': 0,  # logging mode - quiet
#    'objective': 'binary:logistic',  # error evaluation for classification training
#    'scale_pos_weight': scale,
#    'eval_metric': 'auc',
#    'subsample': 0.8
#    }  # the number of classes that exist in this datset
#num_round = 700  # the number of training iterations
#
#bst = xgb.train(param, dtrain, num_round, watchlist, callbacks=[xgb.callback.print_evaluation()], early_stopping_rounds=10)
##bst = xgb.train(param, dtrain, num_round, nfold=5, metrics={'auc'}, seed=10)
#print bst
#dfall_var.loc[:, 'XGB'] = bst.predict(dall)
#bst.dump_model('dump.raw'+str(num_round)+'iterations'+"_"+str(param['max_depth'])+'depths_'+str(param['eta'])+'signal_region_'+str(args.varListKey)+'_'+args.label+'_M'+args.mass+'.txt')
#bst.save_model('XGB'+str(num_round)+'iterations'+"_"+str(param['max_depth'])+'depths_'+str(param['eta'])+'signal_region_'+str(args.varListKey)+'_'+args.label+'_M'+args.mass+'.model')
##print dfall_var
#
#dfall_var.to_root("test_XGB_classification_"+str(args.varListKey)+"_"+'iterations'+"_"+str(param['max_depth'])+'depths_'+str(param['eta'])+args.label+'_M'+args.mass+".root", key="XGB_Tree")






#
#
#x_sig = np.vstack([data_sig[iVar[0]] for iVar in varList]).T
#
#x_bkg = np.vstack([data_bkg[iVar[0]] for iVar in varList]).T
#
#x = np.vstack([x_sig, x_bkg])
#
#num_sig = x_sig.shape[0]
#num_bkg = x_bkg.shape[0]
#
#y = np.hstack([np.ones(num_sig), np.zeros(num_bkg)])
#
#print "Prepare Training"
#num_all = num_sig + num_bkg
#
#w = np.hstack([np.ones(num_sig) * num_all / num_sig, np.ones(num_bkg) * num_all / num_bkg])
#
#x_train, x_test, y_train, y_test, w_train, w_test = train_test_split(x, y, w, test_size=0.3, random_state=7)
#
#dall = xgb.DMatrix(x, label=y, weight=w)
#dtrain = xgb.DMatrix(x_train, label=y_train, weight=w_train)
#dtest = xgb.DMatrix(x_test, label=y_test, weight=w_test)
#watchlist = [(dtest, 'eval'), (dtrain, 'train')]
#
#param = { 
#    'max_depth': 3,  # the maximum depth of each tree
#    'eta': 0.1,  # the training step for each iteration
#    'silent': 0,  # logging mode - quiet
#    'objective': 'binary:logistic',  # error evaluation for multiclass training
#    #'scale_pos_weight': 1/weight,
#    'eval_metric': 'auc',
#    'subsample': 0.6 
#    }  # the number of classes that exist in this datset
#num_round = 600  # the number of training iterations
#bst = xgb.train(param, dtrain, num_round, watchlist, callbacks=[xgb.callback.print_evaluation()], early_stopping_rounds=30)


#bdt = XGBClassifier(max_depth=3, n_estimators=500, verbosity=2)
#print "Start Training"
#bdt.fit(x, y, w)
#TMVA.Experimental.SaveXGBoost(bdt, "myBDT", "tmva101.root")
