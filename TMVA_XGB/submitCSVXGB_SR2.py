import os,shutil,datetime,time
import getpass
import varsList
from ROOT import *
from XRootD import client

###############################################

runDir = os.getcwd()
start_time = time.time()

inputDir='/isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_CSV/SR2'#'/eos/uscms/store/user/lpcbril/MC_test/FWLJMET106X_1lep2017_UL_step2_CSV_SR2_added'
outputDir= '/isilon/hadoop/users/jluo48/CHiggs/UL17/XGB_models/SR2' 
condorDir= runDir+'/condor_logs_CSVtoXGB_SR2_added_new/'

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

Masses = [200, 220, 250, 300, 350, 400, 500, 600, 700, 800, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
#Masses = [500]#[800, 1000, 1250, 1500, 1750, 2000, 2500, 3000]

for mass in Masses:
    #if not 'TTToSemiLeptonic' in file: continue
    #if not 'ttjj' in file: continue
#    if 'TTTo' in file: continue
    dict={'RUNDIR':runDir, 'CONDORDIR':condorDir, 'INPUTDIR':inputDir, 'MASS':mass, 'OUTPUTDIR':outputDir}
    jdfName=condorDir+'/M%(MASS)s.job'%dict
    print jdfName
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/submitCSVXGB.sh
Request_memory = 8000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/CSVXGB.py
Output = M%(MASS)s.out
Error = M%(MASS)s.err
Log = M%(MASS)s.log
Notification = Never
Arguments =  %(INPUTDIR)s   %(OUTPUTDIR)s  %(MASS)s      

Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit M%(MASS)s.job'%dict)
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
#            os.system('sleep 0.5')
#            os.chdir('%s'%(runDir))
