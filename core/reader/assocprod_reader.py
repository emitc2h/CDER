#**************************************************#
# file   : core/reader/lhprocessor_reader.py       #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A reader to read LHProcessor.*.root files        #
#**************************************************#

#############################################################################
#   Copyright 2012-2013 Michel Trottier-McDonald                            #
#                                                                           #
#   This file is part of CDER.                                              #
#                                                                           #
#   CDER is free software: you can redistribute it and/or modify            #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   CDER is distributed in the hope that it will be useful,                 #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with CDER.  If not, see <http://www.gnu.org/licenses/>.           #
#############################################################################

## ROOT imports
from ROOT import gROOT

## CDER imports
from reader import Reader

## Enable ROOT to read std::vectors
gROOT.ProcessLine('.L core/reader/addVectorToROOT.C+')

####################################################
class Custom_Reader(Reader):

    ## --------------------------------------- ##
    def __init__(self, file_path, tree_name):
        """
        Constructor
        """
        
        Reader.__init__(self, file_path, tree_name)


            
    ## --------------------------------------- ##
    def get_taus(self):
        """
        Taus
        """

        if self.tree.nTaus > 0:
            self.event_taus.append((self.tree.tau1_pt, self.tree.tau1_eta, self.tree.tau1_phi))
        if self.tree.nTaus > 1:
            self.event_taus.append((self.tree.tau2_pt, self.tree.tau2_eta, self.tree.tau2_phi))


        
    ## --------------------------------------- ##
    def get_muons(self):
        """
        Muons
        """

        if self.tree.lep1_flavour == 13:
            self.event_muons.append((self.tree.lep1_pt, self.tree.lep1_eta, self.tree.lep1_phi))
        if self.tree.lep2_flavour == 13:
            self.event_muons.append((self.tree.lep2_pt, self.tree.lep2_eta, self.tree.lep2_phi))
        if self.tree.lep3_flavour == 13:
            self.event_muons.append((self.tree.lep3_pt, self.tree.lep3_eta, self.tree.lep3_phi))
        if self.tree.lep4_flavour == 13:
            self.event_muons.append((self.tree.lep4_pt, self.tree.lep4_eta, self.tree.lep4_phi))


            
    ## --------------------------------------- ##
    def get_electrons(self):
        """
        Electrons
        """
        
        if self.tree.lep1_flavour == 11:
            self.event_electrons.append((self.tree.lep1_pt, self.tree.lep1_eta, self.tree.lep1_phi))
        if self.tree.lep2_flavour == 11:
            self.event_electrons.append((self.tree.lep2_pt, self.tree.lep2_eta, self.tree.lep2_phi))
        if self.tree.lep3_flavour == 11:
            self.event_electrons.append((self.tree.lep3_pt, self.tree.lep3_eta, self.tree.lep3_phi))
        if self.tree.lep4_flavour == 11:
            self.event_electrons.append((self.tree.lep4_pt, self.tree.lep4_eta, self.tree.lep4_phi))


    
    ## --------------------------------------- ##
    def get_met(self):
        """
        MET
        """
        
        self.event_met = (self.tree.MET_pt*1000.0, self.tree.MET_phi)


        
    ## --------------------------------------- ##
    def get_extra_information(self):
        """
        Extra information
        """


            
