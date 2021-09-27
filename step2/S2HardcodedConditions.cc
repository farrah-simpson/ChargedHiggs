#define S2HardcodedConditions_cxx
// -*- C++ -*-
//
// Helper class, provides jet tagging eff, scale factors, etc.
// 
// Inspired from BtagS2HardcodedConditions in LJMET
// 
// by
//
// Sinan Sagir, November 2019
//

#include <cmath>
#include "S2HardcodedConditions.h"
#include <unordered_map>

using namespace std;


S2HardcodedConditions::S2HardcodedConditions() {

   if(!(tfile_HTNJ_SF=TFile::Open("HT_njets_SF_sys.root"))){
    std::cout<<"WARNING! SF file doesn't exist! Exiting" << std::endl;
    exit(1);
   }
   if(!(tfile_X53HTNJ_SF=TFile::Open("X53_HT_njets_SF_sys.root"))){
    std::cout<<"WARNING! X5/3 SF file doesn't exist! Exiting" << std::endl;
    exit(1);
   }
   
  std::string SYSs[19] = {"", "_HFup", "_HFdn", "_LFup", "_LFdn", "_jesup", "_jesdn", "_hfstats1up", "_hfstats1dn", "_hfstats2up", "_hfstats2dn", "_cferr1up", "_cferr1dn", "_cferr2up", "_cferr2dn", "_lfstats1up", "_lfstats1dn", "_lfstats2up", "_lfstats2dn"};
  for(size_t isys = 0; isys<19; isys++){
      hscale_ttjj[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttjj"+SYSs[isys]).c_str())->Clone();
      hscale_ttbb[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttbb"+SYSs[isys]).c_str())->Clone();  
      hscale_ttcc[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttcc"+SYSs[isys]).c_str())->Clone();
      hscale_tt2b[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_tt2b"+SYSs[isys]).c_str())->Clone();
      hscale_tt1b[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_tt1b"+SYSs[isys]).c_str())->Clone();
      hscale_STs[SYSs[isys]]     = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STs"+SYSs[isys]).c_str())->Clone();
      hscale_STtw[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STtw"+SYSs[isys]).c_str())->Clone();
      hscale_STt[SYSs[isys]]     = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STt"+SYSs[isys]).c_str())->Clone();
      hscale_WJets[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_WJets"+SYSs[isys]).c_str())->Clone();
      hscale_CHM200[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM200"+SYSs[isys]).c_str())->Clone(); 
      hscale_CHM220[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM220"+SYSs[isys]).c_str())->Clone();
      hscale_CHM250[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM250"+SYSs[isys]).c_str())->Clone();
      hscale_CHM300[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM300"+SYSs[isys]).c_str())->Clone();
      hscale_CHM350[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM350"+SYSs[isys]).c_str())->Clone();
      hscale_CHM400[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM400"+SYSs[isys]).c_str())->Clone();
      hscale_CHM500[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM500"+SYSs[isys]).c_str())->Clone();
      hscale_CHM600[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM600"+SYSs[isys]).c_str())->Clone();
      hscale_CHM700[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM700"+SYSs[isys]).c_str())->Clone();
      hscale_CHM800[SYSs[isys]]   = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM800"+SYSs[isys]).c_str())->Clone();
      hscale_CHM1000[SYSs[isys]]  = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM1000"+SYSs[isys]).c_str())->Clone(); 
      hscale_CHM1250[SYSs[isys]]  = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM1250"+SYSs[isys]).c_str())->Clone();
      hscale_CHM1500[SYSs[isys]]  = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM1500"+SYSs[isys]).c_str())->Clone();
      hscale_CHM1750[SYSs[isys]]  = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM1750"+SYSs[isys]).c_str())->Clone();
      hscale_CHM2000[SYSs[isys]]  = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM2000"+SYSs[isys]).c_str())->Clone();
      hscale_CHM2500[SYSs[isys]]  = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM2500"+SYSs[isys]).c_str())->Clone();
      hscale_CHM3000[SYSs[isys]]  = (TH2F*)tfile_HTNJ_SF->Get(("hscale_CHM3000"+SYSs[isys]).c_str())->Clone();
      hscale_XXM600MH200[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM600MH200"+SYSs[isys]).c_str())->Clone();   
      hscale_XXM600MH400[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM600MH400"+SYSs[isys]).c_str())->Clone();  
      hscale_XXM700MH400[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM700MH400"+SYSs[isys]).c_str())->Clone();  
      hscale_XXM800MH200[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM800MH200"+SYSs[isys]).c_str())->Clone();  
      hscale_XXM800MH400[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM800MH400"+SYSs[isys]).c_str())->Clone();  
      hscale_XXM800MH600[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM800MH600"+SYSs[isys]).c_str())->Clone();  
      hscale_XXM900MH200[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM900MH200"+SYSs[isys]).c_str())->Clone();  
      hscale_XXM900MH400[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM900MH400"+SYSs[isys]).c_str())->Clone();  
      hscale_XXM1000MH200[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1000MH200" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1000MH400[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1000MH400" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1000MH800[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1000MH800" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1100MH200[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1100MH200" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1100MH400[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1100MH400" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1100MH600[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1100MH600" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1100MH800[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1100MH800" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1200MH200[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1200MH200" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1200MH400[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1200MH400" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1200MH600[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1200MH600" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1200MH800[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1200MH800" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1200MH1000[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1200MH1000"+SYSs[isys]).c_str())->Clone();
      hscale_XXM1500MH200[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1500MH200" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1500MH400[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1500MH400" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1500MH600[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1500MH600" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1500MH800[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1500MH800" +SYSs[isys]).c_str())->Clone();
      hscale_XXM1500MH1000[SYSs[isys]]= (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_XXM1500MH1000"+SYSs[isys]).c_str())->Clone();
      hscale_TTToHad0[SYSs[isys]]   = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToHad0" +SYSs[isys]).c_str())->Clone(); 
      hscale_TTToHad700[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToHad700" +SYSs[isys]).c_str())->Clone();
      hscale_TTToHad1000[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToHad1000"+SYSs[isys]).c_str())->Clone();
      hscale_TTToSemiLep0[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToSemiLep0"+SYSs[isys]).c_str())->Clone();
      hscale_TTToSemiLep700[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToSemiLep700"+SYSs[isys]).c_str())->Clone();
      hscale_TTToSemiLep1000[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToSemiLep1000"+SYSs[isys]).c_str())->Clone();
      hscale_TTToLNu0[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToLNu0"+SYSs[isys]).c_str())->Clone();
      hscale_TTToLNu700[SYSs[isys]] = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToLNu700"+SYSs[isys]).c_str())->Clone();
      hscale_TTToLNu1000[SYSs[isys]]  = (TH2F*)tfile_X53HTNJ_SF->Get(("hscale_TTToLNu1000"+SYSs[isys]).c_str())->Clone();
  }
}

S2HardcodedConditions::~S2HardcodedConditions() {
}

float S2HardcodedConditions::GetCSVRenormSF(int year, int isE, int njet, std::string sampleType) {

  if (sampleType == "")
    return 1.0;

  std::unordered_map<string, std::vector<float>> wgt2017_E = { // { type, { nj4, nj5, nj6p}}
      {"tttt", {0.9226035838, 0.9340754278, 0.9178683544}},
      {"ttjj", {0.9952321401, 0.9678148547, 0.916412004}},//{1.0150106608, 1.0158690852, 0.9984062267}}, 
      {"ttcc", {0.9952321401, 0.9678148547, 0.916412004}}, 
      {"ttbb", {0.9586652314, 0.9435930048, 0.8944224401}}, 
      {"tt1b", {0.9952321401, 0.9678148547, 0.916412004}},
      {"tt2b", {0.9952321401, 0.9678148547, 0.916412004}}, 
      {"T",    {0.9933786006, 0.9646801108, 0.9143510121}},    
      {"TTV",  {0.9933786006, 0.9646801108, 0.9143510121}},   
      {"TTXY", {0.9649570916, 0.9760667136, 0.9668860438}},
      {"WJets", {0.8826404583, 0.8583431706, 0.8123368769}},
      {"ZJets", {0.8826404583, 0.8583431706, 0.8123368769}},   
      {"VV",   {0.8826404583, 0.8583431706, 0.8123368769}}, 
      {"qcd",  {0.9844800159, 0.8744057182, 0.7953136397}}  
  }; 
           
  std::unordered_map<string, std::vector<float>> wgt2017_M = {
      {"tttt", {0.9433598986, 0.9272944126, 0.9110504508}},
      {"ttjj", {0.9962244676, 0.9667166631, 0.9186391487}},
      {"ttcc", {0.9962244676, 0.9667166631, 0.9186391487}},    
      {"ttbb", {0.9595725455, 0.9438734429, 0.9030468218}},   
      {"tt1b", {0.9962244676, 0.9667166631, 0.9186391487}},   
      {"tt2b", {0.9962244676, 0.9667166631, 0.9186391487}},
      {"T",    {0.9942103098, 0.9613614481, 0.9144844627}},   
      {"TTV",  {0.9942103098, 0.9613614481, 0.9144844627}}, 
      {"TTXY", {0.9755792626, 0.9659806557, 0.9643891245}},
      {"WJets", {0.9044615563, 0.9076278828, 0.7916357948}},
      {"ZJets", {0.9044615563, 0.9076278828, 0.7916357948}},
      {"VV",   {0.9044615563, 0.9076278828, 0.7916357948}}, 
      {"qcd",  {0.940833989, 0.9788744589, 0.9195875563}} 
  };                       

  std::unordered_map<string, std::vector<float>> wgt2018_E = { // { type, { nj4, nj5, nj6p}}
      {"tttt", {0.9279750194, 0.9479727174, 0.9191942033}},
      {"ttjj", {0.9923480750, 1.0057580471, 1.0011944434}},
      {"ttcc", {1.0050957838, 1.0047475902, 0.9982370828}},    
      {"ttbb", {0.9666382033, 0.9559780476, 0.9556587079}},   
      {"tt1b", {0.9692647427, 0.9778219595, 0.9722511777}},   
      {"tt2b", {0.9956445718, 0.9975362672, 0.9905346602}},
      {"T",    {0.9779770577, 0.9856033892, 0.9726416567}},   
      {"TTV",  {0.9597092704, 0.9660527988, 0.9585140872}}, 
      {"TTXY", {0.9502030288, 0.9594360242, 0.9608876848}},
      {"WJets", {0.8720559924, 0.8777058190, 0.8538766506}},
      {"ZJets", {0.8274565677, 0.8184282280, 0.7902021407}},
      {"VV",   {0.9808907637, 0.8806614835, 0.9322116757}}, 
      {"qcd",  {0.9317167909, 0.9550869373, 0.7593072727}} 
  };  

  std::unordered_map<string, std::vector<float>> wgt2018_M = {
      {"tttt", {0.9598061229, 0.9385816479, 0.9242174919}},
      {"ttjj", {0.9943568547, 1.0037506677, 0.9982871601}},
      {"ttcc", {0.9967671200, 0.9995292499, 0.9998498201}},
      {"ttbb", {0.9569457644, 0.9636918215, 0.9661412214}},
      {"tt1b", {0.9715690171, 0.9751878298, 0.9663625408}},
      {"tt2b", {0.9873304461, 0.9937619408, 0.9917692476}},
      {"T",    {0.9813194258, 0.9931216192, 0.9812484650}},
      {"TTV",  {0.9556623113, 0.9660025586, 0.9641271023}},
      {"TTXY", {0.9472739920, 0.9562394387, 0.9650080939}},
      {"WJets", {0.8705578922, 0.8711052889, 0.8521469129}},
      {"ZJets", {0.8628752440, 0.8546751993, 0.8152587307}},
      {"VV",   {0.8593916158, 0.8730070208, 0.9085752620}},
      {"qcd",  {0.8931172211, 1.0248316102, 0.9197058065}}
  };

  if (wgt2017_E.find(sampleType) ==  wgt2017_E.end()) {
    cout << " GetCSVRenormSF() ---- CHECK sample process type! \n";
    return 1.0;
  }

  if (year == 2017) {

      if (isE == 1) {
        if (njet == 4) {
          return wgt2017_E.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2017_E.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2017_E.at(sampleType)[2];
        }
      }

      else {
        if (njet == 4) {
          return wgt2017_M.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2017_M.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2017_M.at(sampleType)[2];
        }
      }

  }
 
  else if (year == 2018) {

      if (isE == 1) {
        if (njet == 4) {
          return wgt2018_E.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2018_E.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2018_E.at(sampleType)[2];
        }
      }

      else {
        if (njet == 4) {
          return wgt2018_M.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2018_M.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2018_M.at(sampleType)[2];
        }
      }

  }

  return 1.0;

}


float S2HardcodedConditions::GetDeepJetRenorm2DSF( int nljet, int nhjet, std::string sampleType){
  float SF2D_ttjj[6][6] = {{1, 1, 1, 1, 0.939582, 0.87618}, 
                           {1, 1, 1, 0.957002, 0.911638, 0.853485},
                           {1, 1, 0.970434, 0.930546, 0.880593, 0.817999}, 
                           {1, 0.980974, 0.946804, 0.901799, 0.85094, 0.787596}, 
                           {0.989648, 0.959091, 0.917188, 0.869627, 0.819352, 0.779309}, 
                           {0.959994, 0.923669, 0.877175, 0.829647, 0.774213, 0.717095} };

  float SF2D_ttcc[6][6] = {{1, 1, 1, 1, 0.947006, 0.899996}, 
                           {1, 1, 1, 0.963102, 0.925523, 0.874434}, 
                           {1, 1, 0.973196, 0.942934, 0.902485, 0.847356}, 
                           {1, 0.979474, 0.955494, 0.917262, 0.876092, 0.814976}, 
                           {0.986342, 0.962593, 0.930391, 0.89329, 0.855384, 0.793742}, 
                           {0.963446, 0.935476, 0.896962, 0.865743, 0.811242, 0.765619} };

  float SF2D_ttbb[6][6] = {{1, 1, 1, 1, 0.883657, 0.86526}, 
                           {1, 1, 1, 0.923449, 0.915582, 0.838738}, 
                           {1, 1, 0.944189, 0.913233, 0.882771, 0.82867}, 
                           {1, 0.950256, 0.934801, 0.903299, 0.853419, 0.78937}, 
                           {0.960666, 0.944967, 0.923153, 0.880531, 0.860571, 0.782334}, 
                           {0.950986, 0.919905, 0.899561, 0.85355, 0.796195, 0.729436} };
  
  float SF2D_tt2b[6][6] = {{1, 1, 1, 1, 0.972927, 0.932397}, 
                           {1, 1, 1, 0.982712, 0.950536, 0.889349}, 
                           {1, 1, 0.985515, 0.955019, 0.911353, 0.873673}, 
                           {1, 0.989653, 0.9663, 0.936965, 0.892814, 0.84642}, 
                           {0.990539, 0.976992, 0.952355, 0.907868, 0.866692, 0.751665}, 
                           {0.971274, 0.943949, 0.921651, 0.881791, 0.818787, 0.698969} };                     

  float SF2D_tt1b[6][6] = {{1, 1, 1, 1, 0.905169, 0.843257}, 
                           {1, 1, 1, 0.921809, 0.887205, 0.834184}, 
                           {1, 1, 0.944171, 0.903698, 0.863122, 0.800354}, 
                           {1, 0.951601, 0.918797, 0.880442, 0.833286, 0.791393}, 
                           {0.962963, 0.936108, 0.905277, 0.849786, 0.771681, 0.749785}, 
                           {0.944158, 0.909177, 0.873107, 0.821848, 0.863772, 0.778701} };

  float SF2D_STs[5][5] = {{1, 1, 1, 1, 0.921978}, 
                          {1, 1, 1, 0.935643, 0.888106}, 
                          {1, 1, 0.945074, 0.905939, 0.851582}, 
                          {1, 0.959726, 0.919582, 0.876164, 0.816775}, 
                          {0.957571, 0.92423, 0.868378, 0.823301, 0.869474}};
  
  float SF2D_STt[5][5] = {{1, 1, 1, 1, 0.918978}, 
                          {1, 1, 1, 0.940876, 0.898442},
                          {1, 1, 0.949505, 0.909802, 0.850183}, 
                          {1, 0.963022, 0.919389, 0.911295, 0.825214}, 
                          {0.959507, 0.927983, 0.881238, 0.837229, 0.771958}};

  float SF2D_STtw[5][5] = {{1, 1, 1, 1, 0.927632},
                           {1, 1, 1, 0.945819, 0.910207}, 
                           {1, 1, 0.960579, 0.928633, 0.883024}, 
                           {1, 0.972874, 0.941449, 0.902612, 0.84035}, 
                           {0.973624, 0.942087, 0.898423, 0.870541, 0.797636}};
 
  float SF2D_WJets[5][5] = {{1.0, 1, 1, 1, 0.871522}, 
                           {1.0, 1, 1, 0.88504, 0.839207}, 
                           {1.0, 1, 0.923679, 0.858831, 0.810507}, 
                           {1.0, 0.937237, 0.883516, 0.838446, 0.744405}, 
                           {0.931397, 0.897598, 0.856966, 0.791663, 0.567177}};                       
                 
 
  int tmp_nljet = nljet; 
  int tmp_nhjet = nhjet;

  if (sampleType=="ttjj"){
      if(tmp_nljet>5)tmp_nljet=5; 
      if(tmp_nhjet>5)tmp_nhjet=5;
      return SF2D_ttjj[tmp_nljet][tmp_nhjet];
  } 

  if (sampleType=="ttcc"){
      if(tmp_nljet>5)tmp_nljet=5; 
      if(tmp_nhjet>5)tmp_nhjet=5;
      return SF2D_ttcc[tmp_nljet][tmp_nhjet];
  } 

  if (sampleType=="ttbb"){
      if(tmp_nljet>5)tmp_nljet=5; 
      if(tmp_nhjet>5)tmp_nhjet=5;
      return SF2D_ttbb[tmp_nljet][tmp_nhjet];
  } 

  if (sampleType=="tt2b"){
      if(tmp_nljet>5)tmp_nljet=5; 
      if(tmp_nhjet>5)tmp_nhjet=5;
      return SF2D_tt2b[tmp_nljet][tmp_nhjet];
  }

 
  if (sampleType=="tt1b"){
      if(tmp_nljet>5)tmp_nljet=5; 
      if(tmp_nhjet>5)tmp_nhjet=5;
      return SF2D_tt1b[tmp_nljet][tmp_nhjet];
  }


  if (sampleType=="STs"){
      if(tmp_nljet>4)tmp_nljet=4; 
      if(tmp_nhjet>4)tmp_nhjet=4;
      return SF2D_STs[tmp_nljet][tmp_nhjet];
  } 
 
  if (sampleType=="STt"){
      if(tmp_nljet>4)tmp_nljet=4; 
      if(tmp_nhjet>4)tmp_nhjet=4;
      return SF2D_STt[tmp_nljet][tmp_nhjet];
  } 
 
  if (sampleType=="STtw"){
      if(tmp_nljet>4)tmp_nljet=4; 
      if(tmp_nhjet>4)tmp_nhjet=4;
      return SF2D_STtw[tmp_nljet][tmp_nhjet];
  } 
 
  if (sampleType=="WJets"){
      if(tmp_nljet>4)tmp_nljet=4; 
      if(tmp_nhjet>4)tmp_nhjet=4;
      return SF2D_WJets[tmp_nljet][tmp_nhjet];
  } 
 
  return 1.0;
}

float S2HardcodedConditions::GetDeepJetRenorm2DSF_Pt120(int nljet, int nhjet, std::string sampleType){

  float SF2D_ttjj[10][10] = {{1, 1, 1, 1, 0.914295, 0.855981, 0.788017, 0.719348, 0.665896, 0.907472}, 
                             {1, 1, 1, 0.9403, 0.885752, 0.823275, 0.773261, 0.75194, 0.669665, 0.324531}, 
                             {1, 1, 0.961458, 0.912879, 0.854467, 0.802386, 0.723465, 0.690917, 0.822551, 0.432192}, 
                             {1, 0.976138, 0.936126, 0.885704, 0.829272, 0.766006, 0.722983, 0.63443, 0.54405, 1}, 
                             {0.989936, 0.954608, 0.906498, 0.851856, 0.794818, 0.748226, 0.674176, 0.547874, 1, 1}, 
                             {0.967827, 0.92704, 0.874908, 0.827158, 0.769093, 0.707994, 0.626231, 0.529454, 1, 1},
                             {0.941347, 0.896042, 0.843599, 0.802453, 0.748986, 0.749381, 0.752726, 1.35229, 1, 1}, 
                             {0.90902, 0.857969, 0.80447, 0.773602, 0.654969, 0.905507, 1, 1, 1, 1 }, 
                             {0.885848, 0.847048, 0.790042, 0.830957, 0.55508, 0.592558, 1, 1, 1, 1},
                             {0.827688, 0.764788, 0.795124, 0.60106, 0.646121, 1, 1, 1, 1, 1} };

  float SF2D_ttcc[10][10] = {{1, 1, 1, 1, 0.928127, 0.891045, 0.856188, 0.733205, 0.869601, 0.612165}, 
                            {1, 1, 1, 0.952332, 0.908984, 0.871931, 0.777177, 0.754578, 0.633129, 0.819004}, 
                            {1, 1, 0.966178, 0.928641, 0.881489, 0.84136, 0.758343, 0.695484, 0.878269, 1.26438}, 
                            {1, 0.976783, 0.948491, 0.905144, 0.858513, 0.810507, 0.819052, 0.696787, 0.971112, 1}, 
                            {0.986489, 0.959897, 0.923639, 0.878537, 0.825937, 0.748845, 0.781251, 0.936208, 0.4883367, 1}, 
                            {0.970845, 0.937304, 0.896996, 0.859312, 0.797301, 0.739737, 0.719665, 0.684347, 0.413988, 1},
                            {0.951343, 0.914511, 0.873698, 0.815063, 0.81806, 0.70407, 1.01267, 1, 1, 1},
                            {0.917324, 0.885403, 0.860349, 0.806729, 0.885525, 0.685579, 0.32545, 1, 1, 1}, 
                            {0.909687, 0.883426, 0.875301, 0.745303, 0.612943, 1, 1, 1, 1, 1},
                            {0.806097, 0.849363, 0.788071, 0.920666, 1, 1, 1, 1, 1, 1}};
                     

  float SF2D_ttbb[10][10] = {{1, 1, 1, 1, 0.856203, 0.873373, 0.811911, 0.926359, 1.004, 0.924767}, 
                            {1, 1, 1, 0.907266, 0.89026, 0.808529, 0.720003, 0.987361, 0.810721, 0.679076}, 
                            {1, 1, 0.936133, 0.903429, 0.862615, 0.78773, 0.815682, 0.551273, 0.63486, 1}, 
                            {1, 0.946299, 0.923635, 0.891545, 0.859651, 0.792323, 0.85323, 0.716669, 1, 1}, 
                            {0.959651, 0.943695, 0.912355, 0.854609, 0.834287, 0.725201, 0.83797, 0.570797, 1, 1}, 
                            {0.953029, 0.925551, 0.884962, 0.845637, 0.778829, 0.755029, 0.604198, 0.55298, 1, 1}, 
                            {0.940742, 0.913598, 0.859903, 0.817423, 0.90749, 0.51203, 0.467551, 0.461039, 1, 1}, 
                            {0.942408, 0.86938, 0.855046, 0.872003, 0.751884, 1.04017, 1, 1, 1, 1}, 
                            {0.875403, 0.875115, 0.905757, 0.766241, 0.271844, 1, 0.540511, 1, 1, 1}, 
                            {0.885946, 0.898831, 1.08786,1, 1, 1, 1, 1, 1, 1}};

  float SF2D_tt2b[7][7] = {{1, 1, 1, 1, 0.946031, 0.913853, 0.867836},  
                           {1, 1, 1, 0.968685, 0.93936, 0.909541}, 
                           {1, 1, 0.989819, 0.945613, 0.886371, 0.88004, 0.784169}, 
                           {1, 0.987975, 0.962365, 0.920999, 0.852547, 0.815548, 0.823108}, 
                           {0.990038, 0.97252, 0.942915, 0.904403, 0.860505, 0.760451, 0.79842}, 
                           {0.983708, 0.958194, 0.923826, 0.870752, 0.782531, 0.806766, 1.03114}, 
                           {0.953541, 0.912945, 0.907673, 0.791473, 0.759712, 0.622213, 0.690191}};                            

  float SF2D_tt1b[8][8] = {{1, 1, 1, 1, 0.883097, 0.831594, 0.821232, 0.600375}, 
                           {1, 1, 1, 0.908849, 0.866361, 0.843538, 0.719274, 0.574077}, 
                           {1, 1, 0.93369, 0.889267, 0.834048, 0.784524, 0.7199, 0.44332}, 
                           {1, 0.94757, 0.908181, 0.858303, 0.81201, 0.743649, 0.64097, 0.496488}, 
                           {0.962023, 0.929667, 0.896831, 0.849338, 0.758371, 0.758463, 0.625446, 1}, 
                           {0.948803, 0.910331, 0.858764, 0.800337, 0.803771, 0.879735, 0.519613, 1}, 
                           {0.927876, 0.8781, 0.858934, 0.837851, 0.861523, 0.947668, 0.779793, 1},
                           {0.899624, 0.843067, 0.79791, 0.779124, 0.706572, 0.760541, 1, 1}};

  float SF2D_STs[7][7]  = {{1, 1, 1, 1, 0.912418, 0.89435, 0.639492}, 
                           {1, 1, 1, 0.922148, 0.875621, 0.86018, 0.701887}, 
                           {1, 1, 0.94073, 0.894511, 0.852659, 0.731806, 0.81812}, 
                           {1, 0.956359, 0.913565, 0.872706, 0.825797, 0.691711, 0.660154},
                           {0.963887, 0.932558, 0.856557, 0.855656, 0.779453, 1, 1}, 
                           {0.933624, 0.900804, 0.84148, 0.814654, 1, 1, 1}, 
                           {0.896176, 0.838428, 0.94812, 0.8125, 1, 1, 1}}; 


  float SF2D_STtw[8][8] = {{1, 1, 1, 1, 0.912288, 0.870246, 0.783873, 0.731581}, 
                           {1, 1, 1, 0.931507, 0.898732, 0.837464, 0.75079, 0.692539}, 
                           {1, 1, 0.951122, 0.916269, 0.876518, 0.835217, 0.699502, 0.919192}, 
                           {1, 0.969922, 0.934022, 0.887486, 0.83351, 0.818188, 0.809874, 0.738924}, 
                           {0.980168, 0.947751, 0.909781, 0.868633, 0.811947, 0.617954, 0.951286, 1}, 
                           {0.95594, 0.922441, 0.855008, 0.856541, 0.673179, 0.899378, 0.54269, 1},
                           {0.926699, 0.86961, 0.819907, 0.822786, 0.612559, 1, 1, 1}, 
                           {0.917143, 0.885669, 0.764635, 0.78248, 0.904628, 1, 1, 1}};

  float SF2D_STt[8][8] = {{1, 1, 1, 1, 0.907872, 0.831195, 0.799672, 0.848275}, 
                          {1, 1, 1, 0.927118, 0.894337, 0.841062, 0.843695, 0.955127}, 
                          {1, 1, 0.94369, 0.894509, 0.852602, 0.834275, 0.704528, 0.336713}, 
                          {1, 0.958952, 0.911696, 0.894477, 0.789989, 0.882388, 0.60879, 1}, 
                          {0.966774, 0.937393, 0.89499, 0.82697, 0.77672, 0.906953, 1, 1}, 
                          {0.942072, 0.893548, 0.846435, 0.73836, 0.72483, 0.483801, 1, 1}, 
                          {0.929418, 0.858061, 0.816877, 0.851006, 0.640777, 0.52112, 1, 1}, 
                          {0.91376, 0.831527, 0.708463, 0.92597, 1, 1, 1, 1}};

  float SF2D_WJets[7][7] = {{1, 1, 1, 1, 0.837692, 0.707765, 0.892933},
                            {1, 1, 1, 0.857594, 0.834278, 0.758637, 0.905977}, 
                            {1, 1, 0.904951, 0.837138, 0.808672, 0.648008, 1}, 
                            {1, 0.942342, 0.873444, 0.805434, 0.768349, 1, 1}, 
                            {0.941999, 0.899821, 0.823658, 0.689084, 0.711992, 1, 1}, 
                            {0.907745, 0.865801, 0.885909, 0.877998, 1, 1, 1}, 
                            {0.87163, 1.3357, 0.671809, 1.31435, 1, 1, 1}};

 
  int tmp_nljet = nljet; 
  int tmp_nhjet = nhjet;

  if (sampleType=="ttjj"){
      if(tmp_nljet>9)tmp_nljet=9; 
      if(tmp_nhjet>9)tmp_nhjet=9;
      return SF2D_ttjj[tmp_nljet][tmp_nhjet];
  } 

  if (sampleType=="ttcc"){
      if(tmp_nljet>9)tmp_nljet=9; 
      if(tmp_nhjet>9)tmp_nhjet=9;
      return SF2D_ttcc[tmp_nljet][tmp_nhjet];
  } 

  if (sampleType=="ttbb"){
      if(tmp_nljet>9)tmp_nljet=9; 
      if(tmp_nhjet>9)tmp_nhjet=9;
      return SF2D_ttbb[tmp_nljet][tmp_nhjet];
  } 

  if (sampleType=="tt2b"){
      if(tmp_nljet>6)tmp_nljet=6; 
      if(tmp_nhjet>6)tmp_nhjet=6;
      return SF2D_tt2b[tmp_nljet][tmp_nhjet];
  }

 
  if (sampleType=="tt1b"){
      if(tmp_nljet>7)tmp_nljet=7; 
      if(tmp_nhjet>7)tmp_nhjet=7;
      return SF2D_tt1b[tmp_nljet][tmp_nhjet];
  }


  if (sampleType=="STs"){
      if(tmp_nljet>6)tmp_nljet=6; 
      if(tmp_nhjet>6)tmp_nhjet=6;
      return SF2D_STs[tmp_nljet][tmp_nhjet];
  } 
 
  if (sampleType=="STt"){
      if(tmp_nljet>7)tmp_nljet=7; 
      if(tmp_nhjet>7)tmp_nhjet=7;
      return SF2D_STt[tmp_nljet][tmp_nhjet];
  } 
 
  if (sampleType=="STtw"){
      if(tmp_nljet>7)tmp_nljet=7; 
      if(tmp_nhjet>7)tmp_nhjet=7;
      return SF2D_STtw[tmp_nljet][tmp_nhjet];
  } 
 
  if (sampleType=="WJets"){
      if(tmp_nljet>6)tmp_nljet=6; 
      if(tmp_nhjet>6)tmp_nhjet=6;
      return SF2D_WJets[tmp_nljet][tmp_nhjet];
  } 

 return 1.0; 
}


float S2HardcodedConditions::GetDeepJetRenorm2DSF_HTnj(float HT, int njets, std::string sampleType, std::string sysType){

  if(hscale_ttjj.find(sysType)==hscale_ttjj.end()) return 1.0;
  if(sampleType=="") return 1.0;
  int tmp_njets = njets;
  if(tmp_njets>6) tmp_njets=6;
  if (sampleType == "ttjj"){
      return hscale_ttjj[sysType]->GetBinContent(hscale_ttjj[sysType]->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "ttcc"){
      return hscale_ttcc[sysType]->GetBinContent(hscale_ttcc[sysType]->FindBin(tmp_njets, HT));  
  }


  if (sampleType == "ttbb"){
      return hscale_ttbb[sysType]->GetBinContent(hscale_ttbb[sysType]->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "tt2b"){
      return hscale_tt2b[sysType]->GetBinContent(hscale_tt2b[sysType]->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "tt1b"){
      return hscale_tt1b[sysType]->GetBinContent(hscale_tt1b[sysType]->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "STs"){
      return hscale_STs[sysType]->GetBinContent(hscale_STs[sysType]->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "STt"){
      return hscale_STt[sysType]->GetBinContent(hscale_STt[sysType]->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "STtw"){
      return hscale_STtw[sysType]->GetBinContent(hscale_STtw[sysType]->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "WJets"){
      return hscale_WJets[sysType]->GetBinContent(hscale_WJets[sysType]->FindBin(tmp_njets, HT));  
  }
  
  if (sampleType == "CHM200"){
      return hscale_CHM200[sysType]->GetBinContent(hscale_CHM200[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM220"){
      return hscale_CHM220[sysType]->GetBinContent(hscale_CHM220[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM250"){
      return hscale_CHM250[sysType]->GetBinContent(hscale_CHM250[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM300"){
      return hscale_CHM300[sysType]->GetBinContent(hscale_CHM300[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM350"){
      return hscale_CHM350[sysType]->GetBinContent(hscale_CHM350[sysType]->FindBin(tmp_njets, HT));
  }  


  if (sampleType == "CHM400"){
      return hscale_CHM400[sysType]->GetBinContent(hscale_CHM400[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM500"){
      return hscale_CHM500[sysType]->GetBinContent(hscale_CHM500[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM600"){
      return hscale_CHM600[sysType]->GetBinContent(hscale_CHM600[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM700"){
      return hscale_CHM700[sysType]->GetBinContent(hscale_CHM700[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM800"){
      return hscale_CHM800[sysType]->GetBinContent(hscale_CHM800[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM1000"){
      return hscale_CHM1000[sysType]->GetBinContent(hscale_CHM1000[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM1250"){
      return hscale_CHM1250[sysType]->GetBinContent(hscale_CHM1250[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM1500"){
      return hscale_CHM1500[sysType]->GetBinContent(hscale_CHM1500[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM1750"){
      return hscale_CHM1750[sysType]->GetBinContent(hscale_CHM1750[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM2000"){
      return hscale_CHM2000[sysType]->GetBinContent(hscale_CHM2000[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM2500"){
      return hscale_CHM2500[sysType]->GetBinContent(hscale_CHM2500[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "CHM3000"){
      return hscale_CHM3000[sysType]->GetBinContent(hscale_CHM3000[sysType]->FindBin(tmp_njets, HT));
  }  

  if (sampleType == "XXM600MH200"){
		return hscale_XXM600MH200[sysType]->GetBinContent(hscale_XXM600MH200[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM600MH400"){
		return hscale_XXM600MH400[sysType]->GetBinContent(hscale_XXM600MH400[sysType]->FindBin(tmp_njets, HT));
  }


  if (sampleType == "XXM700MH400"){
		return hscale_XXM700MH400[sysType]->GetBinContent(hscale_XXM700MH400[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM800MH200"){
		return hscale_XXM800MH200[sysType]->GetBinContent(hscale_XXM800MH200[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM800MH400"){
		return hscale_XXM800MH400[sysType]->GetBinContent(hscale_XXM800MH400[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM800MH600"){
		return hscale_XXM800MH600[sysType]->GetBinContent(hscale_XXM800MH600[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM900MH200"){
		return hscale_XXM900MH200[sysType]->GetBinContent(hscale_XXM900MH200[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM900MH400"){
		return hscale_XXM900MH400[sysType]->GetBinContent(hscale_XXM900MH400[sysType]->FindBin(tmp_njets, HT));
  }


  if (sampleType == "XXM1000MH200"){
		return hscale_XXM1000MH200[sysType]->GetBinContent(hscale_XXM1000MH200[sysType]->FindBin(tmp_njets, HT));
  }
 
  if (sampleType == "XXM1000MH400"){
		return hscale_XXM1000MH400[sysType]->GetBinContent(hscale_XXM1000MH400[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1000MH800"){
		return hscale_XXM1000MH800[sysType]->GetBinContent(hscale_XXM1000MH800[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1100MH200"){
		return hscale_XXM1100MH200[sysType]->GetBinContent(hscale_XXM1100MH200[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1100MH400"){
		return hscale_XXM1100MH400[sysType]->GetBinContent(hscale_XXM1100MH400[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1100MH600"){
		return hscale_XXM1100MH600[sysType]->GetBinContent(hscale_XXM1100MH600[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1100MH800"){
		return hscale_XXM1100MH800[sysType]->GetBinContent(hscale_XXM1100MH800[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1200MH200"){
		return hscale_XXM1200MH200[sysType]->GetBinContent(hscale_XXM1200MH200[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1200MH400"){
		return hscale_XXM1200MH400[sysType]->GetBinContent(hscale_XXM1200MH400[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1200MH600"){
		return hscale_XXM1200MH600[sysType]->GetBinContent(hscale_XXM1200MH600[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1200MH800"){
		return hscale_XXM1200MH800[sysType]->GetBinContent(hscale_XXM1200MH800[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1200MH1000"){
		return hscale_XXM1200MH1000[sysType]->GetBinContent(hscale_XXM1200MH1000[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1500MH200"){
		return hscale_XXM1500MH200[sysType]->GetBinContent(hscale_XXM1500MH200[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1500MH400"){
		return hscale_XXM1500MH400[sysType]->GetBinContent(hscale_XXM1500MH400[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1500MH600"){
		return hscale_XXM1500MH600[sysType]->GetBinContent(hscale_XXM1500MH600[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1500MH800"){
		return hscale_XXM1500MH800[sysType]->GetBinContent(hscale_XXM1500MH800[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "XXM1500MH1000"){
		return hscale_XXM1500MH1000[sysType]->GetBinContent(hscale_XXM1500MH1000[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "TTToHad0"){
		return hscale_TTToHad0[sysType]->GetBinContent(hscale_TTToHad0[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "TTToHad700"){
		return hscale_TTToHad700[sysType]->GetBinContent(hscale_TTToHad700[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "TTToHad1000"){
		return hscale_TTToHad1000[sysType]->GetBinContent(hscale_TTToHad1000[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "TTToSemiLep0"){
		return hscale_TTToSemiLep0[sysType]->GetBinContent(hscale_TTToSemiLep0[sysType]->FindBin(tmp_njets, HT));
  }

  if (sampleType == "TTToSemiLep700"){
		return hscale_TTToSemiLep700[sysType]->GetBinContent(hscale_TTToSemiLep700[sysType]->FindBin(tmp_njets, HT));
  }


  if (sampleType == "TTToSemiLep1000"){
		return hscale_TTToSemiLep1000[sysType]->GetBinContent(hscale_TTToSemiLep1000[sysType]->FindBin(tmp_njets, HT));
  }


  if (sampleType == "TTToLNu0"){;
		return hscale_TTToLNu0[sysType]->GetBinContent(hscale_TTToLNu0[sysType]->FindBin(tmp_njets, HT));
  }


  if (sampleType == "TTToLNu700"){;
		return hscale_TTToLNu700[sysType]->GetBinContent(hscale_TTToLNu700[sysType]->FindBin(tmp_njets, HT));
  }


  if (sampleType == "TTToLNu1000"){
		return hscale_TTToLNu1000[sysType]->GetBinContent(hscale_TTToLNu1000[sysType]->FindBin(tmp_njets, HT));
  }


  return 1.0;
}
