#!/usr/bin/env python

import os,sys,time,math,datetime,itertools
from ROOT import gROOT,TFile,TH1F
import CombineHarvester.CombineTools.ch as ch
parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
from utils import *
gROOT.SetBatch(1)
Sig = 'X53H'
if Sig == 'X53H': prefix_ = 'X53M'
else: prefix_ = 'X53MRH'
def add_processes_and_observations(cb, prefix=prefix_):
	print '>> Creating processes and observations...'
	if prefix!='tttt' and not prefix.endswith('M'): prefix+='M'
	for chn in chns:
		cats_chn = cats[chn]
		cb.AddObservations(  ['*'],  [prefix], [era], [chn],                 cats_chn      )
		cb.AddProcesses(     ['*'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )
		cb.AddProcesses(     [''], [prefix], [era], [chn], sig_procs,      cats_chn, True   )


def add_shapes(cb, prefix=prefix_):
        print '------------------------------------------------------------------------'
	print '>> Extracting histograms from input root files...prefix:',prefix
	for chn in chns:
                print '>>>> \t Extracting histos for channel:',chn
		CRbkg_pattern = iPlot+'_'+lumiStr+'_%s$BIN__$PROCESS' % chn
		if Sig == 'X53H': SRsig_pattern = iPlot+'_'+lumiStr+'_%s$BIN__$PROCESS$MASSMH'% chn + massH 
		else: SRsig_pattern = iPlot+'_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn
		SRbkg_pattern = CRbkg_pattern
		CRsig_pattern = SRsig_pattern 
		if 'isCR' in chn: 
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(rfile, CRbkg_pattern, CRbkg_pattern + '__$SYSTEMATIC')
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(rfile, CRsig_pattern, CRsig_pattern + '__$SYSTEMATIC')
		else:
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(rfile, SRbkg_pattern, SRbkg_pattern + '__$SYSTEMATIC')
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(rfile, SRsig_pattern, SRsig_pattern + '__$SYSTEMATIC')
		        

def add_bbb(cb):
	print '>> Merging bin errors and generating bbb uncertainties...'
	bbb = ch.BinByBinFactory()
	bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(False)
	
	for chn in chns:
		cb_chn = cb.cp().channel([chn])
		if 'isCR' in chn:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(sig_procs), cb)
		else:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(sig_procs), cb)


def rename_and_write(cb):
	print '>> Setting standardised bin names...'
	ch.SetStandardBinNames(cb)
	
	writer = ch.CardWriter('limits_'+signal+'_'+template+saveKey+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
						   'limits_'+signal+'_'+template+saveKey+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')
	writer.SetVerbosity(1)
	writer.WriteCards('cmb', cb)
	for chn in chns:
		print chn
		writer.WriteCards(chn, cb.cp().channel([chn]))
	print '>> Done!'

def print_cb(cb):
	for s in ['Obs', 'Procs', 'Systs', 'Params']:
		print '* %s *' % s
		getattr(cb, 'Print%s' % s)()
		print

#update ele and mu ID iso and trig, include prefire,muRF,isr,fsr!
def add_standard_systematics(cb):
	print '>> Adding standard systematic uncertainties...'
	
	signal = cb.cp().signals().process_set()

	
        cb.cp().process(signal).channel(chns).AddSyst(cb, 'signalScale', 'rateParam', ch.SystMap()(0.01)) # 1000fb --> 10fb

        cb.GetParameter("signalScale").set_frozen(True)
        #print (cb.GetParameter("signalShape").frozen())

	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['R16'], 1.01)(['R16APV'], 1.01)(['R17'], 1.02)(['R18'], 1.015)) # Uncorrelated part
	if era!='R16' or  era!='R16APV': cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi_R1718', 'lnN', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.006)(['R18'], 1.002)) # 2017 and 2018 correlated part
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi_Run2', 'lnN', ch.SystMap('era')(['R16'], 1.006)(['R16APV'], 1.006)(['R17'], 1.009)(['R18'], 1.02)) # Full correlated part
	cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'SFel_$ERA', 'lnN', ch.SystMap()(1.06))#('era')(['R16'], 1.06)(['R16APV'], 1.06)(['R17'], 1.06)(['R18'], 1.06)) # 1.5% el id, 2.5%** iso + 5% trigger ~ 3%, doubled trigger uncertainty during OR
	cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'SFmu_$ERA', 'lnN', ch.SystMap()(1.06))#('era')(['R16'], 1.06)(['R16APV'], 1.06)(['R17'], 1.06)(['R18'], 1.06)) # 1% mu id, 2.5%** iso + 2.5% trigger ~ 5%, doubled trigger uncertainty during OR
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'jec_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # This one is being studied in B2G-19-001/AN2018_322_v7 (take the uncorrelated one to be conservative!)
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'jer_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7#should be fully correlated?
	if era!='R18':
		cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'prefire_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'pileup', 'shape', ch.SystMap()(1.0)) # Correlated: https://hypernews.cern.ch/HyperNews/CMS/get/b2g/1381.html
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'LF_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # B-tagging reweighting systematics, LF
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'LF_$ERA', 'shape', ch.SystMap()( 1.0 )) # B-tagging reweighting systematics, LF

#        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'HF_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) #B-tagging reweighting systematics, HF
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'HF_$ERA', 'shape', ch.SystMap()( 1.0 )) #B-tagging reweighting systematics, HF

	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'LFstat1_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'LFstat2_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'HFstat1_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'HFstat2_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'CFerr1_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'CFerr2_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'CFerr1_$ERA', 'shape', ch.SystMap()( 1.0 ))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'CFerr2_$ERA', 'shape', ch.SystMap()( 1.0 ))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'DJjes_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
#For each JES source used in your analysis the respective up/down_jesXXX varied SF is to be applied to the JES-varied template instead of the nominal one
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'PNT', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'PNW', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R16APV'], 1.0)(['R17'], 1.0)(['R18'], 1.0))

	for proc in allbkgs:
		if proc in ttbkgs: 
			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'muRF_tt', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'isr_tt', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'fsr_tt', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
		else: 
			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'muRF_'+proc, 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'isr_'+proc, 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'fsr_'+proc, 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'pdf', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7
	#cb.cp().process(signal).channel(chns).AddSyst(cb, smoothAlgo+'muRF_'+signal, 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
	#cb.cp().process(signal).channel(chns).AddSyst(cb, smoothAlgo+'isr_'+signal, 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
	#cb.cp().process(signal).channel(chns).AddSyst(cb, smoothAlgo+'fsr_'+signal, 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
	#cb.cp().process( ttbkgs).channel(chns).AddSyst(cb, 'xsec_ttbar', 'lnN', ch.SystMap()([0.945,1.048])) # (scale and pdf added in quadrature) from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO; Ex: HIG-18-004/AN2017_090_v12/Table13 and HIG-19-011/AN2019_094_v10/Table79-80
	#cb.cp().process( ttbkgs).channel(chns).AddSyst(cb, 'xsec_ttbar', 'lnN', ch.SystMap()([0.91,1.11])) # hDamp uncertainty of +10/-7% added in quadrature with the x-sec uncertainty (+4.8/-5.5%)
	#cb.cp().process(['ewk']).channel(chns).AddSyst(cb, 'xsec_ewk', 'lnN', ch.SystMap()(1.038)) # (scale and pdf added in quadrature) from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV; Ex: HIG-18-004/AN2017_090_v12/Table13 and HIG-19-011/AN2019_094_v10/Table79-80
	#cb.cp().process(['top']).channel(chns).AddSyst(cb, 'xsec_top', 'lnN', ch.SystMap()(1.04)) # ttV,ttH, and tt+XY uncertainties are 50% in OSDL and SSDL analyses, so aligning it with this inflated uncertainty.
	cb.cp().process( ttbkgs).channel(chns).AddSyst(cb, 'xsec_ttbar', 'lnN', ch.SystMap()([0.945,1.048])) #4TOP +4.8, -5.5 mine:+29.3 -36.6(scale and pdf added in quadrature) from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO; Ex: HIG-18-004/AN2017_090_v12/Table13 and HIG-19-011/AN2019_094_v10/Table79-80
	cb.cp().process(['ewk']).channel(chns).AddSyst(cb, 'xsec_ewk', 'lnN', ch.SystMap()(1.038)) # (scale and pdf added in quadrature) from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV; Ex: HIG-18-004/AN2017_090_v12/Table13 and HIG-19-011/AN2019_094_v10/Table79-80
	cb.cp().process(['top']).channel(chns).AddSyst(cb, 'xsec_top', 'lnN', ch.SystMap()(1.04)) #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec ttV,ttH, and tt+XY uncertainties are 50% in OSDL and SSDL analyses, so aligning it with this inflated uncertainty.
	
	cb.cp().process(['ttH']).channel(chns).AddSyst(cb, 'xsec_ttH', 'lnN', ch.SystMap()(1.2)) # Based on agreement with others in 15APR21 4tops meeting
def add_HF_systematics(cb):
	print '>> Adding HF systematic uncertainties...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(['ttbb']).channel(chns).AddSyst(cb, 'ttHF', 'lnN', ch.SystMap()(1.13)) # Uncorrelated; from TOP-18-002 (v34) Table 4, sqrt(0.2^2+0.6^2)/4.7 ~ 0.134565 ~ 0.13 4%**


def add_autoMCstat(cb):
	print '>> Adding autoMCstats...'
	cb.AddDatacardLineAtEnd('* autoMCStats 1.')


def create_workspace(cb):
	print '>> Creating workspace...'
	
	for chn in ['cmb']:#+chns:
		chnDir = os.getcwd()+'/limits_'+signal+'_'+template+saveKey+'/'+chn+'/'
		cmd = 'combineTool.py -M T2W -i '+chnDir+' -o workspace.root --parallel 4 --channel-masks'
		os.system(cmd)


def go(cb):
	add_processes_and_observations(cb)
	add_standard_systematics(cb)
	#add_HF_systematics(cb)
	#add_Njet4to9p_systematics(cb)
	add_shapes(cb)
	#add_bbb(cb)
	add_autoMCstat(cb)
	rename_and_write(cb)
	create_workspace(cb)
	#print_cb(cb)


if __name__ == '__main__':
	cb = ch.CombineHarvester()
	#cb.SetVerbosity(20)
	
	if Sig =='X53H': massH = sys.argv[5]
	iPlot= sys.argv[3]#'HT'
	era = sys.argv[2]#'R18'
	erajec = era.replace('R','20')
	if era=='R16': lumiStr = '16p81fb'
	elif era=='R16APV': lumiStr = '19p52fb'
	elif era=='R17': lumiStr = '41p48fb'
	elif era=='R18': lumiStr = '59p83fb'
	if Sig=='X53H':pre = 'X53'#'X53RH' or MH: 'X53'	
	else:pre = 'X53RH'	
	signal = pre+'M'+sys.argv[4]

	smoothAlgo = '' #leave empty if smoothed shapes are not wanted, else enter 'lowess', 'super', or 'kern'
	tag = '_wNegBinsCorrec__rebinned_stat0p2'#_ifsr'
	if Sig=='X53H': saveKey = ''+'MH'+massH
	else: saveKey = ''
	fileDir = '/uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_11_3_4/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates/'
	template = sys.argv[1]#nonjetsf_lepPt20_2020_9_3'
	cutString = ''#sys.argv[4]

	if not os.path.exists('./limits_'+signal+'_'+template+saveKey): os.system('mkdir ./limits_'+signal+'_'+template+saveKey)
	os.system('cp '+fileDir+template+'/templates_'+iPlot+'_'+lumiStr+tag+'.root ./limits_'+signal+'_'+template+saveKey+'/')
	rfile = './limits_'+signal+'_'+template+saveKey+'/templates_'+iPlot+'_'+lumiStr+tag+'.root'
	
	ttbkgs = ['ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
	notqcdbkgs = ['top','ewk']
	allbkgs = ttbkgs +['top','ewk','qcd']
	dataName = 'data_obs'
	tfile = TFile(rfile)
	allHistNames = [k.GetName() for k in tfile.GetListOfKeys() if not (k.GetName().endswith('Up') or k.GetName().endswith('Down'))]
	tfile.Close()
	chns = [hist[hist.find('fb_')+3:hist.find('__')] for hist in allHistNames if '__'+dataName in hist]
	chnsE = [chn for chn in chns if 'isE_' in chn]
	chnsM = [chn for chn in chns if 'isM_' in chn]
	#chns_njet = {}
	#for i in range(4,11):
	#	chns_njet[i]=[chn for chn in chns if 'nJ'+str(i) in chn]
	bkg_procs = {chn:[hist.split('__')[-1] for hist in allHistNames if '_'+chn+'_' in hist and not (hist.endswith('Up') or hist.endswith('Down') or hist.endswith(dataName) or ('_X53' in hist))] for chn in chns}
	for cat in sorted(bkg_procs.keys()):
		print cat,bkg_procs[cat]
	sig_procs = [signal]
	
	cats = {}
	for chn in chns: cats[chn] = [(0, '')]
	masses = ch.ValsFromRange('690')
	go(cb)
