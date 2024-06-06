import os,sys
from ROOT import TFile, TObject, RooArgSet

## Arguments: limit directory name; mass point; signal amount to inject; number of toys

## Make a datacard first with datacard.py!

limitdir = sys.argv[1]
mass = sys.argv[2]
#rInj = int(sys.argv[3])
#nToys = int(sys.argv[4])
sig='X53'
#name = limitdir+'InjR'+str(rInj)#.replace('limits_templatesCR_Nov2021_','').replace('limits_templatesSRCR_Nov2021_','')+'InjR'+str(rInj)
path = limitdir+'/cmb/'+mass

isSR = True#False
if 'CR' in limitdir: isSR = False
if 'SR' in limitdir: isSR = True
os.chdir(path)

filename = 'initialFitWorkspace.root'
if isSR: 
    filename = 'morphedWorkspace.root'
    refitname = 'fitDiagnosticsFitMorphed.root'

if not isSR and not os.path.exists(filename):

    print "Running Fit Diagnostics for initial workspace"
    print 'Command = combine -M FitDiagnostics -d workspace.root --saveWorkspace' #--saveShapes --plots' #--setParameters signalScale=1'
    os.system('combine -M FitDiagnostics -d workspace.root --saveWorkspace --cminDefaultMinimizerStrategy 0 --setParameters signalScale=0.1') #--saveShapes --plots')# --setParameters signalScale=1')
    
    print "Creating initialFit snapshot file: initialFitWorkspace.root"
    w_f = TFile.Open('higgsCombineTest.FitDiagnostics.mH120.root')
    w = w_f.Get('w')
    fr_f = TFile.Open('fitDiagnosticsTest.root')#('fitDiagnostics.root')
    fr = fr_f.Get('fit_b')
    myargs = RooArgSet(fr.floatParsFinal())
    w.saveSnapshot('initialFit',myargs,True)
    fout = TFile('initialFitWorkspace.root',"recreate")
    fout.WriteTObject(w,'w')
    fout.Close()

if isSR and (not os.path.exists(filename) or not os.path.exists(refitname)):
    if sig=='X53': masks = 'mask_R16APV_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=1,mask_R16APV_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=1,mask_R16_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=1,mask_R16_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=1,mask_R17_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=1,mask_R17_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=1,mask_R18_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=1,mask_R18_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=1'
    if sig=='X53H': masks = 'mask_R16APV_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=1,mask_R16APV_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=1,mask_R16_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=1,mask_R16_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=1,mask_R17_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=1,mask_R17_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=1,mask_R18_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=1,mask_R18_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=1'

    #masks = masks+',signalScale=0.1' # 100fb for CR-only fit

    if not os.path.exists(filename):
        print "Running Fit Diagnostics for initial workspace with SR channels masked: Mass =",mass
        print 'Command = combine -M FitDiagnostics -d workspace.root --saveWorkspace --cminDefaultMinimizerStrategy 0 -n Masked --setParameters '+masks #--cminDefaultMinimizerStrategy 0
        os.system('combine -M FitDiagnostics -d workspace.root --cminDefaultMinimizerStrategy 0 --saveWorkspace -n Masked --setParameters '+masks)#--cminDefaultMinimizerStrategy 0
        #print 'Command = combine -M FitDiagnostics -d workspace.root --saveWorkspace --saveShapes --plots -n Masked --setParameters '+masks
        #os.system('combine -M FitDiagnostics -d workspace.root --saveWorkspace --saveShapes --plots -n Masked --setParameters '+masks)
        
        print "Creating initialFit snapshot file: morphedWorkspace.root"
        w_f = TFile.Open('higgsCombineMasked.FitDiagnostics.mH120.root')
        w = w_f.Get('w')
        fr_f = TFile.Open('fitDiagnosticsMasked.root')
        fr = fr_f.Get('fit_b')
        myargs = RooArgSet(fr.floatParsFinal())
        w.saveSnapshot('initialFit',myargs,True)
        fout = TFile('morphedWorkspace.root', "recreate")
        fout.WriteTObject(w,'w')
        fout.Close()

	#os.system('python importPars.py morphedWorkspace.root fitDiagnosticsMasked.root')

#    
#    if not os.path.exists(refitname):
#	if sig=='X53': masks = 'mask_R16APV_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'
#	if sig=='X53H': masks = 'mask_R16APV_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'
#
#        print 'Running Fit Diagnostics again on morphedWorkspace.root'
#        print 'Command = combine -M FitDiagnostics -d morphedWorkspace.root -n FitMorphed --snapshotName initialFit --bypassFrequentistFit --expectSignal 0 -t -1 --setParameters '+masks
#        os.system('combine -M FitDiagnostics -d morphedWorkspace.root -n FitMorphed --cminDefaultMinimizerStrategy 0 --snapshotName initialFit --bypassFrequentistFit --expectSignal 0 -t -1 --setParameters '+masks)
#

## Toy generation is SR-safe, it throws toys off fit_b, which will be CR-data-only from masking. --bypassFrequentistFit should be bypassing any re-fitting
#if isSR:
#    if sig=='X53': masks = 'mask_R16APV_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'
#    if sig=='X53H': masks = 'mask_R16APV_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'
#print "Generating toys from fit_b snapshot"
#if isSR:
#    print 'Command = combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name+' --setParameters '+masks
#    os.system('combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name+' --setParameters '+masks)
#else:
#    print 'Command = combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name
#    os.system('combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name)
#
### Toy fits again should be ok, since it's just fitting the previously-made toys
#print "Fitting toys...."
#print 'Command = combineTool.py -M FitDiagnostics -d '+filename+' --parallel 4 --snapshotName initialFit --robustFit=1 --skipBOnlyFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --toysFile higgsCombine'+name+'.GenerateOnly.mH120.123456.root --rMin '+str(rInj-10)+' --rMax '+str(rInj+10)+' -n '+name
#os.system('combineTool.py -M FitDiagnostics -d '+filename+' --parallel 4 --snapshotName initialFit --cminDefaultMinimizerStrategy 0 --robustFit=1 --skipBOnlyFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --toysFile higgsCombine'+name+'.GenerateOnly.mH120.123456.root --rMin '+str(rInj-10)+' --rMax '+str(rInj+10)+' -n '+name)
#
print "Done!"
print "NOW -- Go run runCondorToys.py!"
