#!/bin/bash

inputDir=${1}
outputDir=${2}
mass=${3}
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

#xrdcp -f $inputDir/dtrainM${mass}.csv ./
#xrdcp -f $inputDir/dtestM${mass}.csv ./
cp $inputDir/dtrainM${mass}.csv ./
cp $inputDir/dtestM${mass}.csv ./


ls

python CSVXGB_SR1.py   -m ${mass}
 

#xrdcp -f *model $outputDir/
#xrdcp -f *txt $outputDir/
cp *model $outputDir/
cp *txt $outputDir/


rm *model
rm *txt
rm *csv
rm *cache*
