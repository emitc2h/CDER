#**************************************************#
# file   : core/reader/vhcn_reader.py              #
# author : Michel Trottier-McDonald                #
# date   : November 2014                           #
# description:                                     #
# A reader to read the common ntuple for the HSG4: #
# VH->Vtautau analysis                             #
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
from reader import Reader, CUT_NO_SELECTION

## Enable ROOT to read std::vectors
gROOT.ProcessLine('.L core/reader/addVectorToROOT.C+')

####################################################
class Custom_Reader(Reader):

    ## --------------------------------------- ##
    def __init__(self, file_path, tree_name, initial_cut_string=CUT_NO_SELECTION):
        """
        Constructor
        """
        
        Reader.__init__(self, file_path, tree_name, initial_cut_string)



    ## --------------------------------------- ##
    def get_jets(self):
        """
        Jets
        """


    ## --------------------------------------- ##
    def get_photons(self):
        """
        Photons
        """


            
    ## --------------------------------------- ##
    def get_taus(self):
        """
        Taus
        """

        if self.tree.evtsel_nMediumTaus > 0:
            self.event_taus.append((self.tree.evtsel_tau1_et, self.tree.evtsel_tau1_eta, self.tree.evtsel_tau1_phi))
        if self.tree.evtsel_nMediumTaus > 1:
            self.event_taus.append((self.tree.evtsel_tau2_et, self.tree.evtsel_tau2_eta, self.tree.evtsel_tau2_phi))


        
    ## --------------------------------------- ##
    def get_muons(self):
        """
        Muons
        """

        if self.tree.evtsel_vlep1_flavour == 13:
            self.event_muons.append((self.tree.evtsel_vlep1_pt, self.tree.evtsel_vlep1_eta, self.tree.evtsel_vlep1_phi))
        if self.tree.evtsel_vlep2_flavour == 13:
            self.event_muons.append((self.tree.evtsel_vlep2_pt, self.tree.evtsel_vlep2_eta, self.tree.evtsel_vlep2_phi))
        if self.tree.evtsel_hlep1_flavour == 13:
            self.event_muons.append((self.tree.evtsel_hlep1_pt, self.tree.evtsel_hlep1_eta, self.tree.evtsel_hlep1_phi))
        if self.tree.evtsel_hlep2_flavour == 13:
            self.event_muons.append((self.tree.evtsel_hlep2_pt, self.tree.evtsel_hlep2_eta, self.tree.evtsel_hlep2_phi))


            
    ## --------------------------------------- ##
    def get_electrons(self):
        """
        Electrons
        """
        
        if self.tree.evtsel_vlep1_flavour == 11:
            self.event_electrons.append((self.tree.evtsel_vlep1_pt, self.tree.evtsel_vlep1_eta, self.tree.evtsel_vlep1_phi))
        if self.tree.evtsel_vlep2_flavour == 11:
            self.event_electrons.append((self.tree.evtsel_vlep2_pt, self.tree.evtsel_vlep2_eta, self.tree.evtsel_vlep2_phi))
        if self.tree.evtsel_hlep1_flavour == 11:
            self.event_electrons.append((self.tree.evtsel_hlep1_pt, self.tree.evtsel_hlep1_eta, self.tree.evtsel_hlep1_phi))
        if self.tree.evtsel_hlep2_flavour == 11:
            self.event_electrons.append((self.tree.evtsel_hlep2_pt, self.tree.evtsel_hlep2_eta, self.tree.evtsel_hlep2_phi))


    
    ## --------------------------------------- ##
    def get_met(self):
        """
        MET
        """
        
        self.event_met = (self.tree.evtsel_MET, self.tree.evtsel_MET_phi)


        
    ## --------------------------------------- ##
    def get_extra_information(self):
        """
        Extra information
        """



            
