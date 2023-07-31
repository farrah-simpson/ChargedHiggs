#!/usr/bin/python

from ROOT import TH1D,TH2D,TTree,TFile
from array import array
from weights import *
from utils import *
from random import randint

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,tTreePkey,process,cutList, doAllSys,doJetRwt,iPlot,plotDetails,category,region,isCategorized):
	print "*****"*20
	print "*****"*20
	plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
	isPlot2D = False
	if len(plotDetails)==4: 
		isPlot2D = True
		ybins=array('d', plotDetails[3])
		yAxisLabel=plotDetails[4]
	
	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5
	# Define categories
	isEM  = category['isEM']
	nttag = category['nttag']
	nWtag = category['nWtag']
	nbtag = category['nbtag']
	njets = category['njets']
	catStr = 'is'+isEM+'_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag+'_nJ'+njets
	
	if iPlot.endswith('pBDT') and isSR(njets,nbtag):# if the category is an SR, set the template to BDT:
		plotTreeName=plotDetails[3]
		xbins=array('d', plotDetails[4])
		xAxisLabel=plotDetails[5]
	if iPlot.endswith('pDNN') and isSR(njets,nbtag):# if the category is an SR, set the template to BDT:
		plotTreeName=plotDetails[3]
		xbins=array('d', plotDetails[4])
		xAxisLabel=plotDetails[5]

	print "DISTRIBUTION:", iPlot
	print "            -name in ljmet trees:", plotTreeName
	print "            -x-axis label is set to:", xAxisLabel
	print "            -using the binning as:", xbins
	
	ljmetCalc = 'JetSubCalc' #JetSubCalc/singleLepCalc switch

	# Define general cuts
	cut  = ' ((leptonPt_MultiLepCalc > '+str(cutList['lepPtCut'])+' && isElectron == 1) || (leptonPt_MultiLepCalc > '+str(cutList['lepPtCut'])+' && isMuon == 1) )' #((leptonPt_MultiLepCalc > 35 && isElectron) || (leptonPt_MultiLepCalc > 30 && isMuon))'
	cut += ' && (MT_lepMet > '+str(cutList['mtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (minDR_lepJet > 0.4)'
	cut += ' && (AK4HT  > '+str(cutList['AK4HTCut'])+')'
	cut += ' && (corr_met_MultiLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_'+ljmetCalc+'_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_'+ljmetCalc+'_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
# 	cut += ' && (isTau_singleLepCalc == 0)'

	#cut += ' && (MCWeight_MultiLepCalc>0)'
	if 'CR' in region: 
		cut += ' && (deltaR_lepJets[1] >= 0.4 && deltaR_lepJets[1] < '+str(cutList['drCut'])+')'
	else: 
		cut += ' && (deltaR_lepJets[1] >= '+str(cutList['drCut'])+')' #PS or SR
    
	if isEM=='E' and isCR(njets,nbtag): cut += ' && (minDPhi_MetJet>0.05)'

	cut += ' && DataPastTriggerX == 1 && MCPastTriggerX == 1'
	# Define weights
	TrigEff = 'triggerXSF'
	jetSFstr = '1'

	#if doJetRwt and ('WJetsMG' in process or 'QCD' in process) and 'JSF' in process: jetSFstr= 'JetSF_80X'

	weightStr = '1'
	weightStrBase = '1'
	trainingSamples=[]#'Tt','Tbt','Ts','TtW','TbtW','TTWl','TTWq','TTZl','TTZq']

# 	if process.startswith('Hptb'):	
# 		cut  += ' && (isTraining == 0)'
# 		weightStr = '2'
# 		weightStrBase = '2'
################################################################################################################
############################  BDT FLIP BINNING APP############## ############## ############## 
# 	if ('BDT' in plotTreeName) and (process.startswith('Hptb')): #Add "or 'TTJetsPH' in process" here
# 		cut += ' && ((isTraining == 1) || (isTraining == 2))'
# 		weightStr = '3/2'
# 		weightStrBase = '3/2'
# 	elif not 'Hptb' in process and not 'TTJets' in process and not 'Data' in process:
# 		cut += ' && ((isTraining == 1) || (isTraining == 2))'
# 		weightStr = '3/2'
# 		weightStrBase = '3/2'
# 	elif ('AK4HT' in plotTreeName) and (process.startswith('Hptb')): #Add "or 'TTJetsPH' in process" here
# 		cut += ' && ((isTraining == 1) || (isTraining == 2))'
# 		weightStr = '3/2'
# 		weightStrBase = '3/2'
############################  BDT FLIP BINNING BUILDING############## ############## ############## 
# 	if ('XGB' in plotTreeName) and (process.startswith('Hptb') 'TTToSemiLeptonic' in process) ): #Add "or 'TTJetsPH' in process" here
# 		cut += ' && (isTraining == 3)'
# 		weightStr = '3'
# 		weightStrBase = '3'
# 	elif not 'Hptb' in process and not 'TTJets' in process and not 'Data' in process:
# 		cut += ' && (isTraining == 3)'
# 		weightStr = '3'
# 		weightStrBase = '3'
# 	elif ('AK4HT' in plotTreeName) and (process.startswith('Hptb')): #Add "or 'TTJetsPH' in process" here
# 		cut += ' && (isTraining == 3)'
# 		weightStr = '3'
# 		weightStrBase = '3'



	CalibReaderRewgt = 'CalibReaderRewgt'
	HTweightStr = '1'
	HTweightStrUp = '1'
	HTweightStrDn = '1'
	DJweightStr = ' btagDeepJetWeight * btagDeepJet2DWeight_HTnj '
      
	if 'WJetsMG' in process:
		HTweightStr   = 'HTSF_Pol'
		HTweightStrUp = 'HTSF_PolUp'
		HTweightStrDn = 'HTSF_PolDn'
#
# 		HTweightStr = str(genHTweight[process])
# 		HTweightStr   = 'HTSF_Pol'
# 		HTweightStrUp = 'HTSF_PolUp'
# 		HTweightStrDn = 'HTSF_PolDn'
# 		HTweightStr   = 'HTSF_Exp'
# 		HTweightStrUp = 'HTSF_ExpUp'
# 		HTweightStrDn = 'HTSF_ExpDn'
	njetsLJMETname = 'NJets_'+ljmetCalc
	topPt13TeVstr = '1'
	if 'TTTo' in process: topPt13TeVstr = 'topPtWeight13TeV'

	njetStr = '1.0'
	njetUpStr = '1.0'
	njetDownStr = '1.0'

# 	topPt13TeVstr = '1'
	if 'Data' not in process:
		#weightStr          += ' * '+topPt13TeVstr+' * '+HTweightStr+' * '+TrigEff+'  * lepIdSF * btagDeepJetWeight * btagDeepJet2DWeight_Pt120 * EGammaGsfSF*(MCWeight_MultiLepCalc/abs(MCWeight_Mu\
#ltiLepCalc))  *'+str(weight[process])
                weightStr          += ' * '+topPt13TeVstr+' * '+HTweightStr+' * '+TrigEff+'  * lepIdSF *'+DJweightStr+'* EGammaGsfSF*(MCWeight_MultiLepCalc/abs(MCWeight_Mu\
ltiLepCalc))  *'+str(weight[process]) 
                #weightTrigEffUpStr  = weightStr.replace(TrigEff,'('+TrigEff+'+'+TrigEff+'Uncert)')
                #weightTrigEffDownStr= weightStr.replace(TrigEff,'('+TrigEff+'-'+TrigEff+'Uncert)')
                weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
                weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
                weightL1NonPFPUpStr  = weightStr.replace('L1NonPrefiringProb_CommonCalc','L1NonPrefiringProbUp_CommonCalc')
                weightL1NonPFPDownStr = weightStr.replace('L1NonPrefiringProb_CommonCalc','L1NonPrefiringProbDown_CommonCalc' )
                weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
                weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
                weightmuRUpStr      = 'renormWeights[4] * '+weightStr
                weightmuRDownStr    = 'renormWeights[2] * '+weightStr
                weightmuFUpStr      = 'renormWeights[1] * '+weightStr
                weightmuFDownStr    = 'renormWeights[0] * '+weightStr
                weighttopptUpStr    = weightStr.replace(topPt13TeVstr,'1')
                weighttopptDownStr  = weightStr
                weighthtUpStr       = weightStr.replace(HTweightStr,HTweightStrUp)
                weighthtDownStr     = weightStr.replace(HTweightStr,HTweightStrDn)

                weightPrefireUpStr   = weightStr.replace('L1NonPrefiringProb_CommonCalc','L1NonPrefiringProbUp_CommonCalc')
                weightPrefireDownStr = weightStr.replace('L1NonPrefiringProb_CommonCalc','L1NonPrefiringProbDown_CommonCalc')
                weightIsrUpStr      = 'renormPSWeights[0] * '+weightStr
                weightIsrDownStr    = 'renormPSWeights[2] * '+weightStr
                weightFsrUpStr      = 'renormPSWeights[1] * '+weightStr
                weightFsrDownStr    = 'renormPSWeights[3] * '+weightStr
                weightNjetUpStr     = njetUpStr + ' * ' + weightStr
                weightNjetDownStr   = njetDownStr + ' * ' + weightStr
                weightNjetSFUpStr   = njetStr + ' * ' + weightStr
                weightNjetSFDownStr = weightStr


		#weightStrBase                     += ' * '+topPt13TeVstr+' * '+HTweightStr+' * '+TrigEff+' * CalibReaderRewgt * pileupWeight * isoSF * lepIdSF * EGammaGsfSF * L1NonPrefiringProb_CommonCalc * (MCWeight_MultiLepCalc/abs(MCWeight_MultiLepCalc)) * '
		#weightStr                         += ' * '+topPt13TeVstr+' * '+HTweightStr+' * '+TrigEff+' * CalibReaderRewgt * pileupWeight * isoSF * lepIdSF * EGammaGsfSF * L1NonPrefiringProb_CommonCalc * (MCWeight_MultiLepCalc/abs(MCWeight_MultiLepCalc)) * '+str(weight[process])
		#weightTrigEffUpStr      = weightStr.replace(TrigEff,'('+TrigEff+'+'+TrigEff+'Uncert)')
		#weightTrigEffDownStr    = weightStr.replace(TrigEff,'('+TrigEff+'-'+TrigEff+'Uncert)')
		#weightPileupUpStr       = weightStr.replace('pileupWeight','pileupWeightDown')
		#weightPileupDownStr     = weightStr.replace('pileupWeight','pileupWeightUp')
		#weightmuRFcorrdUpStr    = 'renormWeights[5] * '+weightStr
		#weightmuRFcorrdDownStr  = 'renormWeights[3] * '+weightStr
		#weightmuRUpStr          = 'renormWeights[4] * '+weightStr
		#weightmuRDownStr        = 'renormWeights[2] * '+weightStr
		#weightmuFUpStr          = 'renormWeights[1] * '+weightStr
		#weightmuFDownStr        = 'renormWeights[0] * '+weightStr
		#weighttopptUpStr        = weightStr.replace(topPt13TeVstr,'1')
		#weighttopptDownStr      = weightStr
		#weighthtUpStr           = weightStr.replace(HTweightStr,HTweightStrUp)
		#weighthtDownStr         = weightStr.replace(HTweightStr,HTweightStrDn)

		#weightjsfJESUpStr          = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESup')
		#weightjsfJESDownStr        = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESdn')
		#weightjsfJESAbsoluteMPFBiasUpStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESAbsoluteMPFBiasup')
		#weightjsfJESAbsoluteMPFBiasDownStr          = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESAbsoluteMPFBiasdn')
		#weightjsfJESAbsoluteScaleUpStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESAbsoluteScaleup')
		#weightjsfJESAbsoluteScaleDownStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESAbsoluteScaledp')
		#weightjsfJESAbsoluteStatUpStr               = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESAbsoluteStatup')
		#weightjsfJESAbsoluteStatDownStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESAbsoluteStatdn')
		#weightjsfJESFlavorQCDupStr                  = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESFlavorQCDup')
		#weightjsfJESFlavorQCDDownStr                = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESFlavorQCDdn')
		#weightjsfJESFragmentationUpStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESFragmentationup')
		#weightjsfJESFragmentationDownStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESFragmentationdn')
		#weightjsfJESPileUpDataMCUpStr               = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpDataMCup')
		#weightjsfJESPileUpDataMCDownStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpDataMCdn')
		#weightjsfJESPileUpPtBBUpStr                 = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtBBup')
		#weightjsfJESPileUpPtBBDownStr               = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtBBdn')
		#weightjsfJESPileUpPtEC1UpStr                = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtEC1up')
		#weightjsfJESPileUpPtEC1DownStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtEC1dn')
		#weightjsfJESPileUpPtEC2UpStr                = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtEC2up')
		#weightjsfJESPileUpPtEC2DownStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtEC2dn')
		#weightjsfJESPileUpPtHFUpStr                 = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtHFup')
		#weightjsfJESPileUpPtHFDownStr               = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtHFdn')
		#weightjsfJESPileUpPtRefUpStr                = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtRefup')
		#weightjsfJESPileUpPtRefDownStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESPileUpPtRefdn')
		#weightjsfJESRelativeBalUpStr                = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeBalup')
		#weightjsfJESRelativeBalDownStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeBaldn')
		#weightjsfJESRelativeFSRUpStr                = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeFSRup')
		#weightjsfJESRelativeFSRDownStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeFSRdn')
		#weightjsfJESRelativeJEREC1UpStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJEREC1up')
		#weightjsfJESRelativeJEREC1DownStr           = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJEREC1dn')
		#weightjsfJESRelativeJEREC2UpStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJEREC2up')
		#weightjsfJESRelativeJEREC2DownStr           = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJEREC2dn')
		#weightjsfJESRelativeJERHFUpStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJERHFup')
		#weightjsfJESRelativeJERHFDownStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJERHFdn')
		#weightjsfJESRelativeJERHFUpStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJERHFup')
		#weightjsfJESRelativeJERHFDownStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeJERHFdn')
		#weightjsfJESRelativePtBBUpStr               = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtBBup')
		#weightjsfJESRelativePtBBDownStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtBBdn')
		#weightjsfJESRelativePtEC1UpStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtEC1up')
		#weightjsfJESRelativePtEC1DownStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtEC1dn')
		#weightjsfJESRelativePtEC2UpStr              = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtEC2up')
		#weightjsfJESRelativePtEC2DownStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtEC2dn')
		#weightjsfJESRelativePtHFUpStr               = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtHFup')
		#weightjsfJESRelativePtHFDownStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativePtHFdn')
		#weightjsfJESRelativeStatECUpStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeStatECup')
		#weightjsfJESRelativeStatECDownStr           = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeStatECdn')
		#weightjsfJESRelativeStatFSRUpStr            = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeStatFSRup')
		#weightjsfJESRelativeStatFSRDownStr          = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeStatFSRdn')
		#weightjsfJESRelativeStatHFUpStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeStatHFup')
		#weightjsfJESRelativeStatHFDownStr           = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESRelativeStatHFdn')
		#weightjsfJESSinglePionECALUpStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESSinglePionECALup')
		#weightjsfJESSinglePionECALDownStr           = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESSinglePionECALdn')
		#weightjsfJESSinglePionHCALUpStr             = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESSinglePionHCALup')
		#weightjsfJESSinglePionHCALDownStr           = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESSinglePionHCALdn')
		#weightjsfJESTimePtEtaUpStr                  = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESTimePtEtaup')
		#weightjsfJESTimePtEtaDownStr                = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_JESTimePtEtadn')


		#
		weightLFUpStr           = weightStr.replace(DJweightStr, ' btagDeepJetWeight_LFup * btagDeepJet2DWeight_HTnj_LFup ')
                weightLFDownStr         = weightStr.replace(DJweightStr, ' btagDeepJetWeight_LFdn * btagDeepJet2DWeight_HTnj_LFdn ')
                weightLFstat1UpStr      = weightStr.replace(DJweightStr, ' btagDeepJetWeight_lfstats1up * btagDeepJet2DWeight_HTnj_lfstats1up ')
                weightLFstat1DownStr      = weightStr.replace(DJweightStr, ' btagDeepJetWeight_lfstats1dn * btagDeepJet2DWeight_HTnj_lfstats1dn ')
                weightLFstat2UpStr        = weightStr.replace(DJweightStr, ' btagDeepJetWeight_lfstats2up * btagDeepJet2DWeight_HTnj_lfstats2up ')
                weightLFstat2DownStr      = weightStr.replace(DJweightStr, ' btagDeepJetWeight_lfstats2dn * btagDeepJet2DWeight_HTnj_lfstats2dn ')
		weightHFUpStr             = weightStr.replace(DJweightStr, ' btagDeepJetWeight_HFup * btagDeepJet2DWeight_HTnj_HFup ')
                weightHFDownStr           = weightStr.replace(DJweightStr, ' btagDeepJetWeight_HFdn * btagDeepJet2DWeight_HTnj_HFdn ')
                weightHFstat1UpStr        = weightStr.replace(DJweightStr, ' btagDeepJetWeight_hfstats1up * btagDeepJet2DWeight_HTnj_hfstats1up ')
                weightHFstat1DownStr      = weightStr.replace(DJweightStr, ' btagDeepJetWeight_hfstats1dn * btagDeepJet2DWeight_HTnj_hfstats1dn ')
                weightHFstat2UpStr        = weightStr.replace(DJweightStr, ' btagDeepJetWeight_hfstats2up * btagDeepJet2DWeight_HTnj_hfstats2up ')
                weightHFstat2DownStr      = weightStr.replace(DJweightStr, ' btagDeepJetWeight_hfstats2dn * btagDeepJet2DWeight_HTnj_hfstats2dn ')
                weightCFerr1UpStr         = weightStr.replace(DJweightStr, ' btagDeepJetWeight_cferr1up * btagDeepJet2DWeight_HTnj_cferr1up ')
                weightCFerr1DownStr         = weightStr.replace(DJweightStr, ' btagDeepJetWeight_cferr1dn * btagDeepJet2DWeight_HTnj_cferr1dn ')
                weightCFerr2UpStr         = weightStr.replace(DJweightStr, ' btagDeepJetWeight_cferr2up * btagDeepJet2DWeight_HTnj_cferr2up ')
                weightCFerr2DownStr         = weightStr.replace(DJweightStr, ' btagDeepJetWeight_cferr2dn * btagDeepJet2DWeight_HTnj_cferr2dn ')
                weightDJjesUpStr          = weightStr.replace(DJweightStr, ' btagDeepJetWeight_jesup * btagDeepJet2DWeight_HTnj_jesup ')
                weightDJjesDownStr        = weightStr.replace(DJweightStr, ' btagDeepJetWeight_jesdn * btagDeepJet2DWeight_HTnj_jesdn ')
    
		#weightLFDownStr         = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_LFdn')
		#weightLFstat1UpStr      = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_LFstat1up')
		#weightLFstat1DownStr    = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_LFstat1dn')
		#weightLFstat2UpStr      = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_LFstat2up')
		#weightLFstat2DownStr    = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_LFstat2dn')
		#weightHFUpStr           = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_HFup')
		#weightHFDownStr         = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_HFdn')
		#weightHFstat1UpStr      = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_HFstat1up')
		#weightHFstat1DownStr    = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_HFstat1dn')
		#weightHFstat2UpStr      = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_HFstat2up')
		#weightHFstat2DownStr    = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_HFstat2dn')
		#weightCFerr1UpStr       = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_CFerr1up')
		#weightCFerr1DownStr     = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_CFerr1dn')
		#weightCFerr2UpStr       = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_CFerr2up')
		#weightCFerr2DownStr     = weightStr.replace(CalibReaderRewgt,'CalibReaderRewgt_CFerr2dn')

	sdmassvar='theJetAK8SoftDropCorr_JetSubCalc_PtOrdered'
	tau21var = 'theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered'
	tau32var = 'theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered'
	if 'SoftDropMassNm1W' in iPlot: cut += ' && ('+tau21var+' < 0.45)'
	if 'SoftDropMassNm1t' in iPlot: cut += ' && ('+tau32var+' < 0.80)'
	if 'Tau21Nm1' in iPlot:  cut += ' && ('+sdmassvar+' > 65 && '+sdmassvar+' < 105)'
	if 'Tau32Nm1' in iPlot:  cut += ' && ('+sdmassvar+' > 105 && '+sdmassvar+' < 220)'



	#weightStr = '1'
	#cut += ' && MCWeight_singleLepCalc < 0'

	# Design the tagging cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'

	nbtagLJMETname = 'NJetsCSV_'+ljmetCalc
	njetsLJMETname = 'NJets_'+ljmetCalc
	nttagLJMETname = 'NJetsTtagged'
	nWtagLJMETname = 'NJetsWtagged'
	nttagCut = ''
	nWtagCut = ''
	nbtagCut = ''
	
	nbjCut = ''	
	if isCategorized:

	    nttagCut = ''
	    if 'p' in nttag: nttagCut+=' && '+nttagLJMETname+'>='+nttag[:-1]
	    else: nttagCut+=' && '+nttagLJMETname+'=='+nttag
	    if nttag=='0p': nttagCut=''

	    nWtagCut = ''
	    if 'p' in nWtag: nWtagCut+=' && '+nWtagLJMETname+'>='+nWtag[:-1]
	    else: nWtagCut+=' && '+nWtagLJMETname+'=='+nWtag
	    if nWtag=='0p': nWtagCut=''
	
	    nbtagCut = ''
	    if 'p' in nbtag: nbtagCut+=' && '+nbtagLJMETname+'>='+nbtag[:-1]
	    else: nbtagCut+=' && '+nbtagLJMETname+'=='+nbtag
	
	    if nbtag=='0' and iPlot=='minMlb': 
			originalLJMETName=plotTreeName
			plotTreeName='minMleppJet'

	    njetsCut = ''
	    if 'p' in njets: njetsCut+=' && '+njetsLJMETname+'>='+njets[:-1]
	    else: njetsCut+=' && '+njetsLJMETname+'=='+njets
	    if njets=='0p': njetsCut=''
		
	    nbjCut += nbtagCut+njetsCut
		
#	else:
#		if 'CR' in region:
#			nbjCut+=' && ( ('+nbtagLJMETname+'==1 && '+njetsLJMETname+'>=4)'
#			nbjCut+=  ' || ('+nbtagLJMETname+'==2 && '+njetsLJMETname+'==4))'
#		if 'SR' in region:
#			nbjCut+=' && ( ('+nbtagLJMETname+'==2 && '+njetsLJMETname+'>=5)'
#			nbjCut+=  ' || ('+nbtagLJMETname+'>=3 && '+njetsLJMETname+'>=4))'
#		if 'BDT' in region:
#			nbjCut+=' && ( ('+nbtagLJMETname+'>=2 && '+njetsLJMETname+'>=5))'
#		if 'C_S_R' in region:
#			nbjCut+=' && ( ('+nbtagLJMETname+'==1 && '+njetsLJMETname+'>=4)'
#			nbjCut+=' || ('+nbtagLJMETname+'==2 && '+njetsLJMETname+'>=4)'
#			nbjCut+=' || ('+nbtagLJMETname+'>=3 && '+njetsLJMETname+'>=4))'
#		if '1B' in region:
#			nbjCut+=' && ( ('+nbtagLJMETname+'==1 && '+njetsLJMETname+'>=4) )'
#		if '2B' in region:
#			nbjCut+=' && ( ('+nbtagLJMETname+'==2 && '+njetsLJMETname+'>=4) )'
#		if '3pB' in region:
#			nbjCut+=' && ( ('+nbtagLJMETname+'>=2 && '+njetsLJMETname+'>=4) )'


		
# 	if 'p' in njets: njetsCut+=' && '+njetsLJMETname+'>='+njets[:-1]
# 	else: njetsCut+=' && '+njetsLJMETname+'=='+njets
# 	if njets=='0p': njetsCut=''
	
# 	nbjCut += nbtagCut+njetsCut 
	
	fullcut = cut+isEMCut+nbjCut+nttagCut+nWtagCut
	if 'TTJets' in process:
		if process.endswith('_tt2b'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==4'
		elif process.endswith('_ttbb'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==3'
		elif process.endswith('_tt1b'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==2'
		elif process.endswith('_ttcc'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==1'
		elif process.endswith('_ttjj'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==0'

	# replace cuts for shifts
	#cut_btagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[0]')
	#cut_btagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[1]')
	#cut_mistagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[2]')
	#cut_mistagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[3]')

	# replace cuts for shifts
	#cut_btagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_bSFup')
	#cut_btagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_bSFdn')
	#cut_mistagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_lSFup')
	#cut_mistagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_lSFdn')
	
	cut_tau21Up = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[0]')
	cut_tau21Dn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[1]')
	cut_jmsWUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[2]')
	cut_jmsWDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[3]')
	cut_jmrWUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[4]')
	cut_jmrWDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[5]')
	cut_tau21ptUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[6]')
	cut_tau21ptDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[7]')
	
	cut_tau32Up = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[0]')
	cut_tau32Dn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[1]')
	cut_jmstUp = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[2]')
	cut_jmstDn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[3]')
	cut_jmrtUp = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[4]')
	cut_jmrtDn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[5]')
	
#	cut_hotstatUp = fullcut.replace(nhottLJMETname,nhottLJMETname+'_shifts[0]')
#	cut_hotstatDn = fullcut.replace(nhottLJMETname,nhottLJMETname+'_shifts[1]')
#	cut_hotcspurUp = fullcut.replace(nhottLJMETname,nhottLJMETname+'_shifts[2]')
#	cut_hotcspurDn = fullcut.replace(nhottLJMETname,nhottLJMETname+'_shifts[3]')
#	cut_hotclosureUp = fullcut.replace(nhottLJMETname,nhottLJMETname+'_shifts[4]')
#	cut_hotclosureDn = fullcut.replace(nhottLJMETname,nhottLJMETname+'_shifts[5]')


	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag+' #jets: '+njets
	print "Weights:",weightStr
	print "Cuts:",fullcut


	# Declare histograms
	hists = {}
	if isPlot2D: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH2D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
	else: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		#systList = ['trigeff','pileup','muRFcorrd','muR','muF','toppt','btag','mistag','jec','jer','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes' ]
		systList = ['isr','fsr', 'tau32', 'jmst', 'jmrt','tau21','jmsW','jmrW','tau21pt',  'njet','njetsf', 'prefire', 'jec', 'jer', 'pileup','muRFcorrd','muR','muF','toppt','ht','LF','LFstat1', 'LFstat2','HF','HFstat1','HFstat2','CFerr1','CFerr2', 'DJjes'] #'btag','mistag',]
		systList_jsf = ['jsfJES','jsfJESAbsoluteMPFBias', 'jsfJESAbsoluteScale', 'jsfJESAbsoluteStat', 'jsfJESFlavorQCD', 'jsfJESFragmentation', 'jsfJESPileUpDataMC',
		'jsfJESPileUpPtBB', 'jsfJESPileUpPtEC1', 'jsfJESPileUpPtEC2', 'jsfJESPileUpPtHF', 'jsfJESPileUpPtRef', 'jsfJESRelativeBal', 'jsfJESRelativeFSR',
		'jsfJESRelativeJEREC1', 'jsfJESRelativeJEREC2', 'jsfJESRelativeJERHF', 'jsfJESRelativeJERHF', 'jsfJESRelativePtBB', 'jsfJESRelativePtEC1',
		'jsfJESRelativePtEC2', 'jsfJESRelativePtHF', 'jsfJESRelativeStatEC', 'jsfJESRelativeStatFSR', 'jsfJESRelativeStatHF', 'jsfJESSinglePionECAL',
		'jsfJESSinglePionHCAL', 'jsfJESTimePtEta']

		for syst in systList:
			for ud in ['Up','Down']:
				if isPlot2D: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH2D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
				else: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 		for i in range(100): 
# 			if isPlot2D: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH2D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
# 			else: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	print tTreePkey
	print plotTreeName+' >> '+iPlot+'_'+lumiStr+'fb_'+catStr+'_' +process+'_'+weightStr+'*('+fullcut+')'
	print "IF there is an error complaining 3 arguments are given but 1 argument is expected"
	print "Check your step1 files. One of the files might fail with 'permission error', run resubmitFailedJobs.py"	
	tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+fullcut+')', 'GOFF')
	if doAllSys:
		#tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffUpStr+'*('+fullcut+')', 'GOFF')
		#tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuRDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'htUp_'         +lumiStr+'fb_'+catStr+'_'+process, weighthtUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'htDown_'       +lumiStr+'fb_'+catStr+'_'+process, weighthtDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'LFUp_'         +lumiStr+'fb_'+catStr+'_'+process, weightLFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'LFDown_'       +lumiStr+'fb_'+catStr+'_'+process, weightLFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'LFstat1Up_'    +lumiStr+'fb_'+catStr+'_'+process, weightLFstat1UpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'LFstat1Down_'  +lumiStr+'fb_'+catStr+'_'+process, weightLFstat1DownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'LFstat2Up_'    +lumiStr+'fb_'+catStr+'_'+process, weightLFstat2UpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'LFstat2Down_'  +lumiStr+'fb_'+catStr+'_'+process, weightLFstat2DownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'HFUp_'         +lumiStr+'fb_'+catStr+'_'+process, weightHFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'HFDown_'       +lumiStr+'fb_'+catStr+'_'+process, weightHFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'HFstat1Up_'    +lumiStr+'fb_'+catStr+'_'+process, weightHFstat1UpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'HFstat1Down_'  +lumiStr+'fb_'+catStr+'_'+process, weightHFstat1DownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'HFstat2Up_'    +lumiStr+'fb_'+catStr+'_'+process, weightHFstat2UpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'HFstat2Down_'  +lumiStr+'fb_'+catStr+'_'+process, weightHFstat2DownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'CFerr1Up_'     +lumiStr+'fb_'+catStr+'_'+process, weightCFerr1UpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'CFerr1Down_'   +lumiStr+'fb_'+catStr+'_'+process, weightCFerr1DownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'CFerr2Up_'     +lumiStr+'fb_'+catStr+'_'+process, weightCFerr2UpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'CFerr2Down_'   +lumiStr+'fb_'+catStr+'_'+process, weightCFerr2DownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'DJjesUp_'      +lumiStr+'fb_'+catStr+'_'+process, weightDJjesUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'DJjesDown_'    +lumiStr+'fb_'+catStr+'_'+process, weightDJjesDownStr+'*('+fullcut+')', 'GOFF')

		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'prefireUp_'   +lumiStr+'fb_'+catStr+'_'+process, weightPrefireUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'prefireDown_' +lumiStr+'fb_'+catStr+'_'+process, weightPrefireDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'isrUp_'       +lumiStr+'fb_'+catStr+'_'+process,    weightIsrUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'isrDown_'     +lumiStr+'fb_'+catStr+'_'+process,    weightIsrDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'fsrUp_'       +lumiStr+'fb_'+catStr+'_'+process,    weightFsrUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'fsrDown_'     +lumiStr+'fb_'+catStr+'_'+process,    weightFsrDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'njetUp_'      +lumiStr+'fb_'+catStr+'_'+process,    weightNjetUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'njetDown_'    +lumiStr+'fb_'+catStr+'_'+process,    weightNjetDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'njetsfUp_'    +lumiStr+'fb_'+catStr+'_'+process,    weightNjetSFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'njetsfDown_'  +lumiStr+'fb_'+catStr+'_'+process,    weightNjetSFDownStr+'*('+fullcut+')', 'GOFF')

		# Change the plot name itself for shifts if needed
		#BTAGupName = plotTreeName#.replace('_lepBJets','_bSFup_lepBJets')
		#BTAGdnName = plotTreeName#.replace('_lepBJets','_bSFdn_lepBJets')
		#MISTAGupName = plotTreeName#.replace('_lepBJets','_lSFup_lepBJets')
		#MISTAGdnName = plotTreeName#.replace('_lepBJets','_lSFdn_lepBJets')

		#if 'CSVwithSF' in BTAGupName or 'Htag' in BTAGupName or 'MleppB' in BTAGupName or 'BJetLead' in BTAGupName or 'minMlb' in BTAGupName: 
		#	BTAGupName = BTAGupName+'_shifts[0]'
		#	BTAGdnName = BTAGdnName+'_shifts[1]'
		#	MISTAGupName = MISTAGupName+'_shifts[2]'
		#	MISTAGdnName = MISTAGdnName+'_shifts[3]'
		#print 'BTAG SHIFT LJMET NAMES',BTAGupName,BTAGdnName,MISTAGupName,MISTAGdnName
		#tTree[tTreePkey].Draw(BTAGupName+' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagUp+')', 'GOFF')
		#tTree[tTreePkey].Draw(BTAGdnName+' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagDn+')', 'GOFF')
		#tTree[tTreePkey].Draw(MISTAGupName+' >> '+iPlot+'mistagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagUp+')', 'GOFF')
		#tTree[tTreePkey].Draw(MISTAGdnName+' >> '+iPlot+'mistagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagDn+')', 'GOFF')

		# t-tagging:
		TAU32upName = plotTreeName
		TAU32dnName = plotTreeName
		JMSTupName  = plotTreeName
		JMSTdnName  = plotTreeName
		JMRTupName  = plotTreeName
		JMRTdnName  = plotTreeName
		if 'Ttagged' in TAU32upName or 'Tjet' in TAU32upName or 'TJet' in TAU32upName: 
			TAU32upName = TAU32upName+'_shifts[0]'
			TAU32dnName = TAU32dnName+'_shifts[1]'
			JMSTupName  = JMSTupName+'_shifts[2]'
			JMSTdnName  = JMSTdnName+'_shifts[3]'
			JMRTupName  = JMRTupName+'_shifts[4]'
			JMRTdnName  = JMRTdnName+'_shifts[5]'
		print 'TTAG SHIFT LJMET NAMES:',TAU32upName,TAU32dnName,JMSTupName,JMSTdnName,JMRTupName,JMRTdnName
		if nttag!='0p':
			tTree[tTreePkey].Draw(TAU32upName+' >> '+iPlot+'tau32Up_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_tau32Up+')', 'GOFF')
			tTree[tTreePkey].Draw(TAU32dnName+' >> '+iPlot+'tau32Down_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_tau32Dn+')', 'GOFF')		
			tTree[tTreePkey].Draw(JMSTupName +' >> '+iPlot+'jmstUp_'   +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmstUp+')', 'GOFF')
			tTree[tTreePkey].Draw(JMSTdnName +' >> '+iPlot+'jmstDown_' +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmstDn+')', 'GOFF')		
			tTree[tTreePkey].Draw(JMRTupName +' >> '+iPlot+'jmrtUp_'   +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmrtUp+')', 'GOFF')
			tTree[tTreePkey].Draw(JMRTdnName +' >> '+iPlot+'jmrtDown_' +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmrtDn+')', 'GOFF')		

		# W-tagging:
		TAU21upName = plotTreeName
		TAU21dnName = plotTreeName
		JMSWupName  = plotTreeName
		JMSWdnName  = plotTreeName
		JMRWupName  = plotTreeName
		JMRWdnName  = plotTreeName
		TAU21PTupName = plotTreeName
		TAU21PTdnName = plotTreeName
		if 'Wtagged' in TAU21upName or 'Wjet' in TAU21upName or 'WJet' in TAU21upName: 
			TAU21upName = TAU21upName+'_shifts[0]'
			TAU21dnName = TAU21dnName+'_shifts[1]'
			JMSWupName  = JMSWupName+'_shifts[2]'
			JMSWdnName  = JMSWdnName+'_shifts[3]'
			JMRWupName  = JMRWupName+'_shifts[4]'
			JMRWdnName  = JMRWdnName+'_shifts[5]'
			TAU21PTupName = TAU21PTupName+'_shifts[6]'
			TAU21PTdnName = TAU21PTdnName+'_shifts[7]'
		print 'WTAG SHIFT LJMET NAMES:',TAU21upName,TAU21dnName,JMSWupName,JMSWdnName,JMRWupName,JMRWdnName,TAU21PTupName,TAU21PTdnName
		if nWtag!='0p':
			tTree[tTreePkey].Draw(TAU21upName+' >> '+iPlot+'tau21Up_'  +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_tau21Up+')', 'GOFF')
			tTree[tTreePkey].Draw(TAU21dnName+' >> '+iPlot+'tau21Down_'+lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_tau21Dn+')', 'GOFF')		
			tTree[tTreePkey].Draw(JMSWupName +' >> '+iPlot+'jmsWUp_'   +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_jmsWUp+')', 'GOFF')
			tTree[tTreePkey].Draw(JMSWdnName +' >> '+iPlot+'jmsWDown_' +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_jmsWDn+')', 'GOFF')		
			tTree[tTreePkey].Draw(JMRWupName +' >> '+iPlot+'jmrWUp_'   +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_jmrWUp+')', 'GOFF')
			tTree[tTreePkey].Draw(JMRWdnName +' >> '+iPlot+'jmrWDown_' +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_jmrWDn+')', 'GOFF')		
			tTree[tTreePkey].Draw(TAU21upName+' >> '+iPlot+'tau21ptUp_'+lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_tau21ptUp+')', 'GOFF')
			tTree[tTreePkey].Draw(TAU21dnName+' >> '+iPlot+'tau21ptDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_tau21ptDn+')', 'GOFF')		

		# b-tagging:
	#	BTAGupName = plotTreeName#.replace('_lepBJets','_bSFup_lepBJets')
	#	BTAGdnName = plotTreeName#.replace('_lepBJets','_bSFdn_lepBJets')
	#	MISTAGupName = plotTreeName#.replace('_lepBJets','_lSFup_lepBJets')
	#	MISTAGdnName = plotTreeName#.replace('_lepBJets','_lSFdn_lepBJets')
	#	if 'CSVwithSF' in BTAGupName or 'Htag' in BTAGupName or 'MleppB' in BTAGupName or 'BJetLead' in BTAGupName or 'minMlb' in BTAGupName: 
	#		BTAGupName = BTAGupName+'_bSFup'
	#		BTAGdnName = BTAGdnName+'_bSFdn'
	#		MISTAGupName = MISTAGupName+'_lSFup'
	#		MISTAGdnName = MISTAGdnName+'_lSFdn'
	#	print 'BTAG SHIFT LJMET NAMES:',BTAGupName,BTAGdnName,MISTAGupName,MISTAGdnName
	#	if nbtag!='0p':
	#		tTree[tTreePkey].Draw(BTAGupName  +' >> '+iPlot+'btagUp'    +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_btagUp+')', 'GOFF')
	#		tTree[tTreePkey].Draw(BTAGdnName  +' >> '+iPlot+'btagDown'  +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_btagDn+')', 'GOFF')
	#		tTree[tTreePkey].Draw(MISTAGupName+' >> '+iPlot+'mistagUp'  +lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_mistagUp+')', 'GOFF')
	#		tTree[tTreePkey].Draw(MISTAGdnName+' >> '+iPlot+'mistagDown'+lumiStr+'fb_'+catStr+'_'+process  , weightStr+'*('+cut_mistagDn+')', 'GOFF')


		if tTree[tTreePkey+'jecUp']:
			print "DOING JEC!!!"
			tTree[tTreePkey+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
                        tTree[tTreePkey+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')

		#	print "I am in JECup!!!"
		#	for weightStr in weightjsfStr_List:
		#		tTree[tTreePkey+weightStr].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if tTree[tTreePkey+'jerUp']:
			tTree[tTreePkey+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[tTreePkey+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		#	
		##for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
#		if doPDF:
#			print 'Processing PDF ...'
#			for i in range(100): 
#				print i+1,
#				tTree[process].Draw(plotTreeName+' >> '+histName.replace(iPlot,iPlot+'pdf'+str(i)), 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
#			print '/ 100 ... PDF done.'
		
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
