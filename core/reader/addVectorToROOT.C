//*****************************************//
// file   : addVectorToROOT.C              //
// author : Dugan O'Neil                   //
// date   : 2009                           //
// description:                            //
// Add vectors of floats, ints and ROOT    //
// TLorentzVectors to ROOT dictionary      //
//*****************************************//

#include <vector>
#include "TLorentzVector.h"
#ifdef __MAKECINT__
#pragma link C++ class vector<vector<float> >+;
#pragma link C++ class vector<vector<int> >+;
#pragma link C++ class vector<TLorentzVector>;
#endif
