#!/usr/bin/env python

import os,sys,time,math,datetime,itertools
from ROOT import gROOT,TFile,TH1F
import CombineHarvester.CombineTools.ch as ch
parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
from utils import *
gROOT.SetBatch(1)

def add_processes_and_observations(cb, prefix='X53RH'):#prefix='X53M'):
	print '>> Creating processes and observations...'
	if prefix!='tttt' and not prefix.endswith('M'): prefix+='M'
	for chn in chns:
		cats_chn = cats[chn]
		if 'isCR' not in chn:
			cb.AddObservations(  ['*'],  [prefix], [era], [chn],                 cats_chn      )
			cb.AddProcesses(     ['*'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )
			cb.AddProcesses(     masses, [prefix], [era], [chn], sig_procs,      cats_chn, True   )
		else:
			cb.AddObservations(  ['all'],  [prefix], [era], [chn],                 cats_chn      )
			cb.AddProcesses(     ['all'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )


def add_shapes(cb):
	print '>> Extracting histograms from input root files...'
	for chn in chns:
		bkg_pattern = iPlot+'_'+lumiStr+'_%s$BIN__$PROCESS' % chn
		cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
			rfile, bkg_pattern, bkg_pattern + '__$SYSTEMATIC')
		
		sig_pattern = iPlot+'_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn #add MH400
		if 'isCR' not in chn:
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(
				rfile, sig_pattern, sig_pattern + '__$SYSTEMATIC')


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
	
	writer = ch.CardWriter('limits_'+template+saveKey+'_'+cutString+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
						   'limits_'+template+saveKey+'_'+cutString+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')
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


def add_standard_systematics(cb):
	print '>> Adding standard systematic uncertainties...'
	
	signal = cb.cp().signals().process_set()
#add b tagging ones?	
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['R16'], 1.025)(['R17'], 1.023)(['R18'], 1.025)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'SFel_$ERA', 'lnN', ch.SystMap('era')(['R16'], 1.03)(['R17'], 1.03)(['R18'], 1.03)) # 1.5% el id/iso + 2.5% trigger ~ 3%
	cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'SFmu_$ERA', 'lnN', ch.SystMap('era')(['R16'], 1.03)(['R17'], 1.03)(['R18'], 1.03)) # 1% mu id/iso + 2.5% trigger ~ 3%
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jec_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # This one is being studied in B2G-19-001/AN2018_322_v7 (take the uncorrelated one to be conservative!)
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jer_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'JEC', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # This one is being studied in B2G-19-001/AN2018_322_v7 (take the uncorrelated one to be conservative!)
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_Total_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # This one is being studied in B2G-19-001/AN2018_322_v7 (take the uncorrelated one to be conservative!)
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_FlavorQCD', 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_RelativeBal', 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_RelativeSample_'+era.replace('R','20'), 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_Absolute', 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_Absolute_'+era.replace('R','20'), 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_HF', 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_HF_'+era.replace('R','20'), 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_EC2', 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_EC2_'+era.replace('R','20'), 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_BBEC1', 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'JEC_BBEC1_'+era.replace('R','20'), 'shape', ch.SystMap()(1.0))
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'JER', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'PNW', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
###!	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'PNWpt', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
###!   	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jmst', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) #same as jmr?? Necessary for PN? 
###!   	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jmsW', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) #same as jmr?? Necessary for PN?
###!	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jmrt', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
###! 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jmrW', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) 
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'DJjes_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	if era=='R17':
		cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'prefire', 'shape', ch.SystMap()(1.0))
# 	if era=='R18':
# 		cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'hem', 'shape', ch.SystMap()(1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pileup', 'shape', ch.SystMap()(1.0)) # Correlated: https://hypernews.cern.ch/HyperNews/CMS/get/b2g/1381.html
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'btag_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'mistag_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
### btagging	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'btag', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
#b tagging	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'mistag', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	if iPlot != 'HT':
		cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'CSVshapelf_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) #assuming uncorrelated, same as nbtag SF
		cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'CSVshapehf_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0))
	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'hotstat_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Use same logic as b-tagging?
	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'hotcspur_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Use same logic as b-tagging?
	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'hotclosure_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) # Uncorrelated; Use same logic as b-tagging?
	for proc in allbkgs:
		if proc in ttbkgs: 
			cb.cp().process([proc]).channel(chns).AddSyst(cb, 'muRF_tt', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
#		if proc in notqcdbkgs:
			cb.cp().process([proc]).channel(chns).AddSyst(cb, 'PNT', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0)) #ALl background no QCD?

###!			cb.cp().process([proc]).channel(chns).AddSyst(cb, 'isr_tt', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
###!			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'fsr_tt', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
#			cb.cp().process([proc]).channel(chns).AddSyst(cb, smoothAlgo+'PSwgt_tt', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
		else: 
			cb.cp().process([proc]).channel(chns).AddSyst(cb, 'muRF', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
###!			cb.cp().process([proc]).channel(chns).AddSyst(cb, 'isr', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
###!			cb.cp().process([proc]).channel(chns).AddSyst(cb, 'fsr', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
#			cb.cp().process([proc]).channel(chns).AddSyst(cb, 'PSwgt_'+proc, 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
###!	cb.cp().process(signal).channel(chns).AddSyst(cb, 'muRFcorrd', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
#	cb.cp().process(signal).channel(chns).AddSyst(cb, smoothAlgo+'PSwgt_tttt', 'shape', ch.SystMap()(1.0)) # Uncorrelated; TOP-18-003/AN2018_062_v17 (derived from different datasets and with respect to different MC samples)
#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, smoothAlgo+'pdf', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7
# 	cb.cp().process(signal).channel(chns).AddSyst(cb, 'xsec_tttt', 'lnN', ch.SystMap()(1.21)) # https://arxiv.org/pdf/1711.02116.pdf (Table 5)
# 	cb.cp().process(ttbkgs).channel(chns).AddSyst(cb, 'ue', 'shape', ch.SystMap()(1.0))
# 	cb.cp().process(ttbkgs).channel(chns).AddSyst(cb, 'hdamp', 'shape', ch.SystMap()(1.0))
 	#cb.cp().process(allbkgs[0]).channel(chns).AddSyst(cb, 'toppt', 'shape', ch.SystMap()(1.0)) # Correlated; Ex: B2G-19-003/AN2015_174_v14 (since it is assumed that the affect of this correction should be consistent across years)
   	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pdfNew', 'shape', ch.SystMap()(1.0)) 

def add_HF_systematics(cb):
	print '>> Adding HF systematic uncertainties...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(['ttbb']).channel(chns).AddSyst(cb, 'ttHF', 'lnN', ch.SystMap()(1.13)) # Uncorrelated; from TOP-18-002 (v34) Table 4, sqrt(0.2^2+0.6^2)/4.7 ~ 0.134565 ~ 0.13


def add_Njet4to6p_systematics(cb):
	print '>> Adding Njet 4-6+ systematic uncertainties with measured priors...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(ttbkgs).channel(chns_njet[6]+chns_njet[7]+chns_njet[8]+chns_njet[9]+chns_njet[10]).AddSyst(cb, "nJet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.075)(['R18'], 1.048))


def add_Njet4to9p_systematics(cb):
	print '>> Adding Njet 4-9+ systematic uncertainties with measured priors...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(ttbkgs).channel(chns_njet[6]).AddSyst(cb, "n6Jet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0517285300268)(['R18'], 1.0442383872209))
	cb.cp().process(ttbkgs).channel(chns_njet[7]).AddSyst(cb, "n7Jet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0587524161036)(['R18'], 1.0480985065135))
	cb.cp().process(ttbkgs).channel(chns_njet[8]).AddSyst(cb, "n8Jet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0662112889662)(['R18'], 1.0538322999767))
	cb.cp().process(ttbkgs).channel(chns_njet[9]+chns_njet[10]).AddSyst(cb, "n9pJet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0800438168504)(['R18'], 1.0622643813546))


def add_Njet4to9p_50p_systematics(cb):
	print '>> Adding Njet 4-9+ systematic uncertainties with 50% priors...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(ttbkgs).channel(chns_njet[6]).AddSyst(cb, "n6Jet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.50)(['R17'], 1.50)(['R18'], 1.50))
	cb.cp().process(ttbkgs).channel(chns_njet[7]).AddSyst(cb, "n7Jet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.50)(['R17'], 1.50)(['R18'], 1.50))
	cb.cp().process(ttbkgs).channel(chns_njet[8]).AddSyst(cb, "n8Jet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.50)(['R17'], 1.50)(['R18'], 1.50))
	cb.cp().process(ttbkgs).channel(chns_njet[9]+chns_njet[10]).AddSyst(cb, "n9pJet_$ERA", "lnN", ch.SystMap('era')(['R16'], 1.50)(['R17'], 1.50)(['R18'], 1.50))


def add_Njet4to9p_Delta_systematics(cb):
	print '>> Adding Njet 4-9+ systematic uncertainties with Delta(SF, noSF) priors...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(ttbkgs).channel(chns).AddSyst(cb, 'njetsf_$ERA', 'shape', ch.SystMap('era')(['R16'], 1.0)(['R17'], 1.0)(['R18'], 1.0))


def add_Njet4to9p_50p_centValSF_systematics(cb): #PLACEHOLDER, IT IS NOT SET UP CORRECTLY YET!!!
	print '>> Adding Njet 4-9+ systematic uncertainties with 50% priors and central value set to Njet scale factors...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(ttbkgs).channel(chns_njet[6]).AddSyst(cb, "n6Jet_$ERA", "lnN", ch.SystMapAsymm('era')(['R16'], 1.0, 1.0)(['R17'], 0.57566620169, 1.57566620169)(['R18'], 0.48448056055, 1.48448056055))
	cb.cp().process(ttbkgs).channel(chns_njet[7]).AddSyst(cb, "n7Jet_$ERA", "lnN", ch.SystMapAsymm('era')(['R16'], 1.0, 1.0)(['R17'], 0.60904592910, 1.60904592910)(['R18'], 0.54462767888, 1.54462767888))
	cb.cp().process(ttbkgs).channel(chns_njet[8]).AddSyst(cb, "n8Jet_$ERA", "lnN", ch.SystMapAsymm('era')(['R16'], 1.0, 1.0)(['R17'], 0.71705307722, 1.71705307722)(['R18'], 0.59013888621, 1.59013888621))
	cb.cp().process(ttbkgs).channel(chns_njet[9]+chns_njet[10]).AddSyst(cb, "n9pJet_$ERA", "lnN", ch.SystMapAsymm('era')(['R16'], 1.0, 1.0)(['R17'], 0.7377932283, 1.7377932283)(['R18'], 0.7000888232, 1.7000888232))


def add_autoMCstat(cb):
	print '>> Adding autoMCstats...'
	cb.AddDatacardLineAtEnd('* autoMCStats 1.')


def create_workspace(cb):
	print '>> Creating workspace...'
	
	for chn in ['cmb']:#+chns:
		for mass in masses:
			chnDir = os.getcwd()+'/limits_'+template+saveKey+'_'+cutString+'/'+chn+'/'+mass #'/$MASS'
			cmd = 'combineTool.py -M T2W -i '+chnDir+' -o workspace.root --parallel 4'
			os.system(cmd)
		

def go(cb):
	add_processes_and_observations(cb)
	add_standard_systematics(cb)
	add_HF_systematics(cb)
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
	
	iPlot= sys.argv[3]#'HT'
	era = sys.argv[2]#'R18'
	erajec = era.replace('R','20')
	if era=='R16': lumiStr = '35p867fb'
	elif era=='R17': lumiStr = '41p53fb'
	elif era=='R18': lumiStr = '59p97fb'
	smoothAlgo = ''#lowess' #leave empty if smoothed shapes are not wanted, else enter 'lowess', 'super', or 'kern'
	tag = '_rebinned_stat0p3'#_ifsr'
	saveKey = ''#_ifsr_smoothed_'+iPlot
	fileDir = '/uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_10_2_10/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates/'
	template = sys.argv[1]#nonjetsf_lepPt20_2020_9_3'
	cutString = ''#sys.argv[4]

	if not os.path.exists('./limits_'+template+saveKey+'_'+cutString): os.system('mkdir ./limits_'+template+saveKey+'_'+cutString)
	os.system('cp '+fileDir+'templates_'+template+'/'+cutString+'/templates_'+iPlot+'_'+lumiStr+tag+'.root ./limits_'+template+saveKey+'_'+cutString+'/')
	rfile = './limits_'+template+saveKey+'_'+cutString+'/templates_'+iPlot+'_'+lumiStr+tag+'.root'
	
	ttbkgs = []#'ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
	notqcdbkgs = ['top','ewk']
	allbkgs = ['top','ewk','qcd']
	dataName = 'data_obs'
	tfile = TFile(rfile)
	allHistNames = [k.GetName() for k in tfile.GetListOfKeys() if not (k.GetName().endswith('Up') or k.GetName().endswith('Down'))]
	tfile.Close()
	chns = [hist[hist.find('fb_')+3:hist.find('__')] for hist in allHistNames if '__'+dataName in hist]
	chnsE = [chn for chn in chns if 'isE_' in chn]
	chnsM = [chn for chn in chns if 'isM_' in chn]
	chns_njet = {}
	for i in range(4,11):
		chns_njet[i]=[chn for chn in chns if 'nJ'+str(i) in chn]
	bkg_procs = {chn:[hist.split('__')[-1] for hist in allHistNames if '_'+chn+'_' in hist and not (hist.endswith('Up') or hist.endswith('Down') or hist.endswith(dataName) or ('_X53' in hist))] for chn in chns}
	for cat in sorted(bkg_procs.keys()):
		print cat,bkg_procs[cat]
		if 'qcd' in bkg_procs[cat]:
			print '		Removing qcd ...'
			bkg_procs[cat]=bkg_procs[cat][:-1]
# 	if era=='R18':
# 		bkg_procs['isSR_isE_nHOT1p_nT0p_nW0p_nB4p_nJ9']=['ttbb', 'ttcc', 'ttjj', 'top']

	signal = 'X53RH'	
	sig_procs = [signal]
	if signal!='tttt':sig_procs = [signal+'M']#['tttt']
	
	cats = {}
	for chn in chns: cats[chn] = [(0, '')]
	#masses = ch.ValsFromRange('700,800,900,1000,1100,1200,1500')
	masses = ch.ValsFromRange('700:1600|100')
	go(cb)
