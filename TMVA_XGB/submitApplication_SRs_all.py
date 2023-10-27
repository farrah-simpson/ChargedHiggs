import os,shutil,datetime,time
import getpass
import varsList
import sys
from ROOT import *
from XRootD import client
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-y", "--year",  help = "Options: 16APV, 16, 17, 18" )
parser.add_argument("-s", "--shift", help="Nominal, JECup, JECdown, JERup, JERdown")
parser.add_argument("-sig", "--signal", default=False, help="Run on signal instead of background?")
args = parser.parse_args()

if args.year not in ['16', '17', '18', '16APV']: quit( "[ERR] Invalid option used for -y (--year). Quitting." )
###############################################

runDir = os.getcwd()
start_time = time.time()

inputDir='/isilon/hadoop/store/user/dali/FWLJMET106XUL_singleLep20{}UL_RunIISummer20_3t_step2/{}/'.format(args.year, args.shift)
siginputDir='/isilon/hadoop/store/group/bruxljm/FWLJMET106XUL_singleLep20{}UL_RunIISummer20_3t_step2/{}/'.format(args.year, args.shift)
outputDir= '/isilon/hadoop/store/group/bruxljm/trussel1/UL{}/step3_XGB/{}/'.format(args.year, args.shift)
condorDir= runDir+'/logs/condor_logs_XGBSRs_20{}UL_sys_added_{}/'.format(args.year, args.shift)
if args.signal: inputDir = siginputDir
print 'Starting submission'
count=0

#inDir=inputDir[10:]
#outDir=outputDir[10:]

rootfiles = os.popen('ls '+inputDir)
os.system('mkdir -p '+outputDir)
os.system('mkdir -p '+condorDir)
#eosindir = inputDir[inputDir.find("/store"):]
#eosindir = "root://cmseos.fnal.gov/"+eosindir

#eosoutdir = outputDir[outputDir.find("/store"):]
#eosoutdir = "root://cmseos.fnal.gov/"+eosoutdir

for file in rootfiles:
    if 'root' not in file: continue
    #if not 'TTToSemiLeptonic' in file: continue
    #if not 'ttjj' in file: continue
#    if 'TTTo' in file: continue
    rawname = file[:-6]
    count+=1
    dict={'RUNDIR':runDir, 'CONDORDIR':condorDir, 'INPUTDIR':inputDir, 'FILENAME':rawname, 'OUTPUTDIR':outputDir, 'YEAR':args.year}
    jdfName=condorDir+'/%(FILENAME)s.job'%dict
    print jdfName
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/submitApplication_SRs_all.sh
Request_memory = 8000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/XGBApply_SRs.py, %(RUNDIR)s/varsList.py 
Output = %(FILENAME)s.out
Error = %(FILENAME)s.err
Log = %(FILENAME)s.log
Notification = Never
Arguments =  %(INPUTDIR)s/%(FILENAME)s.root  %(OUTPUTDIR)s  %(FILENAME)s  NewVar_added  %(YEAR)s

Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit %(FILENAME)s.job'%dict)
    os.system('sleep 0.5')
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


#BDTlist = ['BDT']
#varListKeys = ['NewVar']#['2016AN']
#massList = ['200','250','300','350','400','500','800','1000','1500','2000','2500','3000']
##massList = ['200','500','2000']
#nIts = '100'
#
#############################################
#
#os.system('mkdir -p '+condorDir)
#
#for mass in massList:
#    note = 'M-'+mass
#    #for method in methodList:
#    for mDepth in ['2']:
#        for vListKey in varListKeys:
#            fileName = 'XGB_'+vListKey+'_'+str(len(varsList.varList[vListKey]))+'vars_mDepth'+mDepth+'_'+note
#            dict={'RUNDIR':runDir,'FILENAME':fileName,'vListKey':vListKey,'mDepth':mDepth,'nIts':nIts,'sigMass':'M-'+mass}
#            jdfName=condorDir+'/%(FILENAME)s.job'%dict
#            print jdfName
#            jdf=open(jdfName,'w')
#            jdf.write(
#            """use_x509userproxy = true
#universe = vanilla
#Executable = %(RUNDIR)s/submitTraining.sh
#Should_Transfer_Files = YES
#WhenToTransferOutput = ON_EXIT
#Transfer_Input_Files = %(RUNDIR)s/UpROOTXGB.py, %(RUNDIR)s/varsList.py
#request_memory = 8000
#Output = %(FILENAME)s.out
#Error = %(FILENAME)s.err
#Log = %(FILENAME)s.log
#Notification = Never
#stream_output = True
#Arguments = %(RUNDIR)s %(FILENAME)s %(vListKey)s %(nIts)s %(mDepth)s %(sigMass)s
#Queue 1"""%dict)
#            jdf.close()
#            os.chdir('%s/'%(condorDir))
#            os.system('condor_submit %(FILENAME)s.job'%dict)
#            os.system('sleep 0.')
#            os.chdir('%s'%(runDir))
