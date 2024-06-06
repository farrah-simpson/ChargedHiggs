import os,sys,shutil,datetime,time,random
from ROOT import *

execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

start_time = time.time()

#IO directories must be full paths
outputDir='/eos/uscms/store/user/fsimpson/Combine_Injection' ## CHANGE MY PATH!
condorDir='/uscms_data/d3/fsimpson/combinejobs_Injection/' ## CHANGE MY PATH!
tarfile = '/uscms_data/d3/jmanagan/combine10213.tar' ## LEAVE ME! -- don't change to your folder

runDir=os.getcwd()
whichjob = sys.argv[1]
limitdir = sys.argv[2]
mass = sys.argv[3]
sig = 'X53'
if whichjob == 'inject':
    rInj = float(sys.argv[4])
    nToys = int(sys.argv[5])
    executable = 'condorToyFitting.sh'
elif whichjob == 'gof':
    rInj = 0
    nToys = int(sys.argv[4])
    executable = 'condorGofFitting.sh'
    outputDir = outputDir.replace('Injection','GOF')
    condorDir = condorDir.replace('Injection','GOF')

if whichjob == 'inject':
    name = limitdir.replace('limits_combine_X53','').replace('limits_CR_combine_X53','')+'InjR'+str(rInj).replace('.','p')+'CDMS0'
else:
    name = limitdir.replace('limits_combine_X53','').replace('limits_combine_X53','')+'GOF'
path = limitdir+'/cmb/'+mass
outDir=outputDir[10:]+'/'+limitdir+'_'+mass
condorDir += limitdir+'_'+mass

isSR = True
if 'CR' in limitdir: isSR = False
if isSR:
    toysperjob = 5
    filename = 'morphedWorkspace.root'
    if sig=='X53': maskstring = '--setParameters mask_R16APV_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'
    if sig=='X53H': maskstring = '--setParameters mask_R16APV_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'

    maskstring = maskstring+',signalScale=0.01' # reset 1fb after CR-only fit
    
else:
    toysperjob = 5
    filename = 'initialFitWorkspace.root'
    maskstring = ''

if whichjob == 'gof': filename = 'workspace.root'

print 'Starting submission'
count=0

os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir)
os.system('mkdir -p '+condorDir)

ijob = 0
for i in range(0,nToys,toysperjob):  
    ijob += 1

    seed = random.randrange(100000,999999)
    print 'Job',ijob,'using seed',seed

    count+=1
    dict={'RUNDIR':runDir, 'EXEC':executable, 'CONDORDIR':condorDir, 'OUTPUTDIR':outDir, 'PATH':path, 'WORKSPACE':filename, 'NTOYS':toysperjob, 'RINJ':rInj, 'RMIN':rInj-10, 'RMAX':rInj+10, 
          'NAME':name, 'MASKS':maskstring, 'TARBALL':tarfile, 'INDEX':ijob, 'SEED':seed}
    jdfName=condorDir+'/%(NAME)s_%(INDEX)s.job'%dict
    print "jdfname: ",jdfName
    jdf=open(jdfName,'w')
    jdf.write(
        """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/%(EXEC)s
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(TARBALL)s, %(RUNDIR)s/%(PATH)s/%(WORKSPACE)s
Output = %(NAME)s_%(INDEX)s.out
Error = %(NAME)s_%(INDEX)s.err
Log = %(NAME)s_%(INDEX)s.log
Notification = Never
Arguments = "%(OUTPUTDIR)s %(WORKSPACE)s %(NTOYS)s %(RINJ)s %(RMIN)s %(RMAX)s %(NAME)s %(SEED)s '%(MASKS)s' %(INDEX)s"

Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit %(NAME)s_%(INDEX)s.job'%dict)
    os.system('sleep 0.5')                                
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"


print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))
