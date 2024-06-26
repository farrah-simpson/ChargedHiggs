#!/bin/bash

condorDir=$PWD
theDir=$1
iPlot=$2
region=$3
isCategorized=$4
isEM=$5
nttag=$6
nWtag=$7
nbtag=$8
njets=$9
lepPtCut=${10}
metCut=${11}
drCut=${12}
jet1PtCut=${13}
jet2PtCut=${14}
AK4HTCut=${15}
	
source /cvmfs/cms.cern.ch/cmsset_default.sh
setenv ROOTSYS /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/
scram p CMSSW CMSSW_10_2_10
cd CMSSW_10_2_10
#cmsenv
#cd $theDir
eval `scramv1 runtime -sh`
cd ../
rm -r CMSSW_10_2_10

python doHists.py ./ $iPlot $region $isCategorized $isEM $nttag $nWtag $nbtag $njets $lepPtCut $metCut $drCut $jet1PtCut $jet2PtCut $AK4HTCut
