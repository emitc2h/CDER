//*************************************************//
// file   : addVectorToROOT.C                      //
// author : Dugan O'Neil                           //
// date   : 2009                                   //
// description:                                    //
// Add vectors of floats, ints and ROOT            //
// TLorentzVectors to ROOT dictionary              //
//*************************************************//

//#############################################################################
//#   Copyright 2012-2013 Dugan O'Neil                                        #
//#                                                                           #
//#   This file is part of CDER.                                              #
//#                                                                           #
//#   CDER is free software: you can redistribute it and/or modify            #
//#   it under the terms of the GNU General Public License as published by    #
//#   the Free Software Foundation, either version 3 of the License, or       #
//#   (at your option) any later version.                                     #
//#                                                                           #
//#   CDER is distributed in the hope that it will be useful,                 #
//#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
//#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
//#   GNU General Public License for more details.                            #
//#                                                                           #
//#   You should have received a copy of the GNU General Public License       #
//#   along with CDER.  If not, see <http://www.gnu.org/licenses/>.           #
//#############################################################################

#include <vector>
#include "TLorentzVector.h"
#ifdef __MAKECINT__
#pragma link C++ class vector<vector<float> >+;
#pragma link C++ class vector<vector<int> >+;
#pragma link C++ class vector<TLorentzVector>;
#endif
