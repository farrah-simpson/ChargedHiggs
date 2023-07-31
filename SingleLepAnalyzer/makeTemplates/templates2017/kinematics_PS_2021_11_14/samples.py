#!/usr/bin/python

samples = {
'DataE':'SingleElectron',
'DataM':'SingleMuon',

#'DYMG200':'DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8',
'DYMG': 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',
#'DYMG400':'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYMG600':'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYMG800':'DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYMG1200':'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYMG2500':'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8',

'DY1MG': 'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
'DY2MG': 'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
'DY3MG': 'DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
'DY4MG': 'DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',

'QCDht200':'QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8',
'QCDht300':'QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8',
'QCDht500':'QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8',
'QCDht700':'QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8',
'QCDht1000':'QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8',
'QCDht1500':'QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8',
'QCDht2000':'QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8',

#TOP
'Tt':'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',#'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8', 
'Tbt': 'ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8',#'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8', 
'Ts': 'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8',#'ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia',
#'Tbs':'ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia',
'TtW':'ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8',
'TbtW': 'ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8',

#'TTTo2L2Nu'
'TTJets2L2nu0':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_Mtt0to700',
'TTJets2L2nu700':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000',
'TTJets2L2nu1000':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf',
'TTJetsHad0':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700',
'TTJetsHad700':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000',
'TTJetsHad1000':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf',
#'TTJetsSemiLepNjet9bin1':'TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700',
#'TTJetsSemiLepNjet9bin2':'TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000',
#'TTJetsSemiLepNjet9bin3':'TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf',
'TTJetsSemiLep01':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_1',
'TTJetsSemiLep02':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_2',
'TTJetsSemiLep03':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_3',
'TTJetsSemiLep04':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_4',
'TTJetsSemiLep05':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_5',
'TTJetsSemiLep06':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_6',
'TTJetsSemiLep07':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_7',
'TTJetsSemiLep08':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_8',
'TTJetsSemiLep09':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_9',
'TTJetsSemiLep010':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_10',
'TTJetsSemiLep7001':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_1',
'TTJetsSemiLep7002':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_2',
'TTJetsSemiLep7003':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_3',
'TTJetsSemiLep7004':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_4',
'TTJetsSemiLep7005':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_5',
'TTJetsSemiLep7006':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_6',
'TTJetsSemiLep7007':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_7',
'TTJetsSemiLep7008':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_8',
'TTJetsSemiLep7009':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_9',
'TTJetsSemiLep70010':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_10',
'TTJetsSemiLep10001':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_1',
'TTJetsSemiLep10002':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_2',
'TTJetsSemiLep10003':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_3',
'TTJetsSemiLep10004':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_4',
'TTJetsSemiLep10005':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_5',
'TTJetsSemiLep10006':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_6',
'TTJetsSemiLep10007':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_7',
'TTJetsSemiLep10008':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_8',
'TTJetsSemiLep10009':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_9',
'TTJetsSemiLep100010':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_10',
'TTJets700mtt':'TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8',
'TTJets1000mtt':'TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8',
'TTToHadronic':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8',
'TTTo2L2Nu': 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',
'TTToSemiLeptonic': 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',
'TTWl':'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
#'TTWq':'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
'TTZl':'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',

#'TTTT':'TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',

'WJetsMG':'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG200':'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG400':'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG600':'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG800':'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG1200':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
#'WJetsMG1200_1':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_1',
#'WJetsMG1200_2':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_2',
#'WJetsMG1200_3':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_3',
#'WJetsMG1200_4':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_4',
#'WJetsMG1200_5':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_5',
#
#'WJetsMG2500_1':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_1',
#'WJetsMG2500_2':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_2',
#'WJetsMG2500_3':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_3',
#'WJetsMG2500_4':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_4',
#'WJetsMG2500_5':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_5',
#'WJetsMG2500_6':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_6',

'WW':'WW_TuneCP5_13TeV-pythia8',
'WZ':'WZ_TuneCP5_13TeV-pythia8',
'ZZ':'ZZ_TuneCP5_13TeV-pythia8',

#'TTHB':'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8',
#'TTHnoB':'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',

# 'TTJets':'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
# 'TTJetsMG':'TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'TTJetsPH':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',
# 'TTJetsPHQ2U':'TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8',
# 'TTJetsPHQ2D':'TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8',
# 'TTJetsPH0to700inc':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Mtt0to700',
# 'TTJetsPH700mtt':'TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8',
# 'TTJetsPH1000mtt':'TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8',
# 'TTZq':'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
# 'TTG':'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',
# 'tZq':'tZq_ll_4f_13TeV-amcatnlo-pythia8',
# 
#'Hptb180':'ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8',
'Hptb200':'ChargedHiggs_HplusTB_HplusToTB_M-200_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb220':'ChargedHiggs_HplusTB_HplusToTB_M-220_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb250':'ChargedHiggs_HplusTB_HplusToTB_M-250_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb300':'ChargedHiggs_HplusTB_HplusToTB_M-300_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb350':'ChargedHiggs_HplusTB_HplusToTB_M-350_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb400':'ChargedHiggs_HplusTB_HplusToTB_M-400_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb450':'ChargedHiggs_HplusTB_HplusToTB_M-450_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb500':'ChargedHiggs_HplusTB_HplusToTB_M-500_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb650':'ChargedHiggs_HplusTB_HplusToTB_M-650_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb750':'ChargedHiggs_HplusTB_HplusToTB_M-750_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb800':'ChargedHiggs_HplusTB_HplusToTB_M-800_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb1000':'ChargedHiggs_HplusTB_HplusToTB_M-1000_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb1250':'ChargedHiggs_HplusTB_HplusToTB_M-1250_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb1500':'ChargedHiggs_HplusTB_HplusToTB_M-1500_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb1750':'ChargedHiggs_HplusTB_HplusToTB_M-1750_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb2000':'ChargedHiggs_HplusTB_HplusToTB_M-2000_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb2500':'ChargedHiggs_HplusTB_HplusToTB_M-2500_TuneCP5_13TeV_amcatnlo_pythia8',
'Hptb3000':'ChargedHiggs_HplusTB_HplusToTB_M-3000_TuneCP5_13TeV_amcatnlo_pythia8',


'X53LHM900':'X53X53_M-900_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1000':'X53X53_M-1000_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1100':'X53X53_M-1100_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1200':'X53X53_M-1200_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1300':'X53X53_M-1300_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1400':'X53X53_M-1400_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1500':'X53X53_M-1500_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1600':'X53X53_M-1600_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1700':'X53X53_M-1700_LH_TuneCP5_13TeV-madgraph-pythia8',

'X53RHM900':'X53X53_M-900_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1000':'X53X53_M-1000_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1100':'X53X53_M-1100_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1200':'X53X53_M-1200_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1300':'X53X53_M-1300_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1400':'X53X53_M-1400_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1500':'X53X53_M-1500_RH_TuneCP2_13TeV-madgraph-pythia8', #2018- CP5 
'X53RHM1600':'X53X53_M-1600_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1700':'X53X53_M-1700_RH_TuneCP5_13TeV-madgraph-pythia8',


'X53M600MH200':'tH_tH_x53x53_narrow_MX600_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M600MH400':'tH_tH_x53x53_narrow_MX600_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M700MH200':'tH_tH_x53x53_narrow_MX700_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M700MH400':'tH_tH_x53x53_narrow_MX700_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M800MH200':'tH_tH_x53x53_narrow_MX800_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M800MH400':'tH_tH_x53x53_narrow_MX800_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M800MH600':'tH_tH_x53x53_narrow_MX800_MH600_TuneCP5_13TeV-madgraph-pythia8',
'X53M900MH200':'tH_tH_x53x53_narrow_MX900_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M900MH400':'tH_tH_x53x53_narrow_MX900_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M900MH600':'tH_tH_x53x53_narrow_MX900_MH600_TuneCP5_13TeV-madgraph-pythia8',
'X53M1000MH200':'tH_tH_x53x53_narrow_MX1000_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M1000MH400':'tH_tH_x53x53_narrow_MX1000_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M1000MH600':'tH_tH_x53x53_narrow_MX1000_MH600_TuneCP5_13TeV-madgraph-pythia8',
'X53M1000MH800':'tH_tH_x53x53_narrow_MX1000_MH800_TuneCP5_13TeV-madgraph-pythia8',
'X53M1100MH200':'tH_tH_x53x53_narrow_MX1100_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M1100MH400':'tH_tH_x53x53_narrow_MX1100_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M1100MH600':'tH_tH_x53x53_narrow_MX1100_MH600_TuneCP5_13TeV-madgraph-pythia8',
'X53M1100MH800':'tH_tH_x53x53_narrow_MX1100_MH800_TuneCP5_13TeV-madgraph-pythia8',
'X53M1200MH200':'tH_tH_x53x53_narrow_MX1200_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M1200MH400':'tH_tH_x53x53_narrow_MX1200_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M1200MH600':'tH_tH_x53x53_narrow_MX1200_MH600_TuneCP5_13TeV-madgraph-pythia8',
'X53M1200MH800':'tH_tH_x53x53_narrow_MX1200_MH800_TuneCP5_13TeV-madgraph-pythia8',
'X53M1200MH1000':'tH_tH_x53x53_narrow_MX1200_MH1000_TuneCP5_13TeV-madgraph-pythia8',
'X53M1500MH200':'tH_tH_x53x53_narrow_MX1500_MH200_TuneCP5_13TeV-madgraph-pythia8',
'X53M1500MH400':'tH_tH_x53x53_narrow_MX1500_MH400_TuneCP5_13TeV-madgraph-pythia8',
'X53M1500MH600':'tH_tH_x53x53_narrow_MX1500_MH600_TuneCP5_13TeV-madgraph-pythia8',
'X53M1500MH800':'tH_tH_x53x53_narrow_MX1500_MH800_TuneCP5_13TeV-madgraph-pythia8',
'X53M1500MH1000':'tH_tH_x53x53_narrow_MX1500_MH1000_TuneCP5_13TeV-madgraph-pythia8',

# 
# 'VHnonbb':'VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8',
# 'WHbb':'WH_HToBB_WToLNu_M125_13TeV_amcatnloFXFX_madspin_pythia8',
# 'WWW':'WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
# 'WWZ':'WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
# 'WZZ':'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
# 'ZZZ':'ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
# 'WWllnn':'WWTo2L2Nu_13TeV-powheg',
# 'WWlnqq':'WWToLNuQQ_13TeV-powheg',
# 'WZlnqq':'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8',
# 'WZlnnn':'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8',
# 'WZllqq':'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
# 'WZllln':'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8',
# 'ZZllnn':'ZZTo2L2Nu_13TeV_powheg_pythia8',
# 'ZZllqq':'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
# 'ZZllll':'ZZTo4L_13TeV_powheg_pythia8',
}

