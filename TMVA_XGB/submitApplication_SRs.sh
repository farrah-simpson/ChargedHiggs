#!/bin/bash

inputfile=${1}
outputDir=${2}
fileName=${3}
vListKey=${4}
scratch=${PWD}

source /cvmfs/cms.cern.ch/cmsset_default.sh

export SCRAM_ARCH=slc7_amd64_gcc820

scramv1 project CMSSW CMSSW_11_1_0_pre7
cd CMSSW_11_1_0_pre7
eval `scramv1 runtime -sh`
cd -

macroDir=${PWD}
export PATH=$PATH:$macroDir

#source /cvmfs/sft.cern.ch/lcg/contrib/gcc/7.3.0/x86_64-centos7-gcc7-opt/setup.sh
#source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.16.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh
#xrdcp -f ${haddFile} root://cmseos.fnal.gov/${outputDir//$NOM/$SHIFT}/${haddFile//${SHIFT}_hadd/} 2>&1

#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M200_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M220_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M250_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M300_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M350_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M400_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M500_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M600_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M700_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M800_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M1000_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M1250_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M1500_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M1750_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M2000_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M2500_SRAll.model .
#cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SRAll/XGB_M3000_SRAll.model .

cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M200_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M220_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M250_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M300_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M350_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M400_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M500_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M600_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M700_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M800_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M1000_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M1250_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M1500_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M1750_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M2000_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M2500_SR1.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR1/XGB_M3000_SR1.model .

cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M200_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M220_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M250_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M300_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M350_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M400_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M500_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M600_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M700_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M800_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M1000_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M1250_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M1500_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M1750_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M2000_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M2500_SR2.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2/XGB_M3000_SR2.model .

cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M200_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M220_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M250_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M300_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M350_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M400_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M500_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M600_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M700_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M800_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M1000_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M1250_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M1500_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M1750_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M2000_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M2500_SR3.model .
cp /isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR3/XGB_M3000_SR3.model .


python XGBApply_SRs.py  -l $vListKey -f $inputfile -o $fileName

cp -f ${fileName}.root $outputDir/

rm *model
rm ${fileName}.root
