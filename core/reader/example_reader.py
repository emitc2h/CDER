#**************************************************#
# file   : core/reader/example_reader.py           #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A reader to read example.root                    #
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

        ## Execute the base class constructor
        Reader.__init__(self, file_path, tree_name)


        
    ## --------------------------------------- ##
    def get_jets(self):
        """
        Get the jet kinematics. Each entry in self.event_jets must be 
        at least a 3-tuple containing jet pt (MeV), jet eta, and jet phi in that
        order. If b-tagging information is relevant and available, pass a 
        4-tuple, the last element being a boolean representing if the jet is
        b-tagged or not.
        """
        
        for i in range(len(self.tree.jet_pt)):
            self.event_jets.append((self.tree.jet_pt[i],
                                    self.tree.jet_eta[i],
                                    self.tree.jet_phi[i],
                                    self.tree.jet_btag[i]))



            
    ## --------------------------------------- ##
    def get_taus(self):
        """
        Get the tau kinematics. Each entry in self.event_taus must be 
        a 3-tuple containing tau pt (MeV), tau eta, and tau phi in that
        order.
        """
        
        for i in range(len(self.tree.tau_pt)):
            self.event_taus.append((self.tree.tau_pt[i],
                                    self.tree.tau_eta[i],
                                    self.tree.tau_phi[i]))



            
    ## --------------------------------------- ##
    def get_muons(self):
        """
        Get the muon kinematics. Each entry in self.event_muons must be 
        a 3-tuple containing muon pt (MeV), muon eta, and muon phi in that
        order.
        """
        
        for i in range(len(self.tree.mu_pt)):
            self.event_muons.append((self.tree.mu_pt[i],
                                     self.tree.mu_eta[i],
                                     self.tree.mu_phi[i]))



            
    ## --------------------------------------- ##
    def get_electrons(self):
        """
        Get the electron kinematics. Each entry in self.event_muons must be 
        a 3-tuple containing electron pt (MeV), electron eta, and electron phi in that
        order.
        """
        
        for i in range(len(self.tree.el_pt)):
            self.event_electrons.append((self.tree.el_pt[i],
                                         self.tree.el_eta[i],
                                         self.tree.el_phi[i]))



            
    ## --------------------------------------- ##
    def get_photons(self):
        """
        Get the photon kinematics. Each entry in self.event_muons must be 
        a 3-tuple containing photon pt (MeV), photon eta, and photon phi in that
        order.
        """
        
        for i in range(len(self.tree.ph_pt)):
            self.event_photons.append((self.tree.ph_pt[i],
                                       self.tree.ph_eta[i],
                                       self.tree.ph_phi[i]))



            
    ## --------------------------------------- ##
    def get_met(self):
        """
        Get the MET kinematics. self.event_met must be a 2-tuple
        containing MET magnitude (MeV) and MET phi in that order.
        """
        
        for i in range(len(self.tree.MET)):
            self.event_met = (self.tree.MET[i], self.tree.MET_phi[0])



            
    ## --------------------------------------- ##
    def get_extra_information(self):
        """
        Get the extra information. self.extra_information is a
        dictionary where keys are variable names that you can customize and
        values are 2-tuples containing the variable value, and the variable type
        as you would give it for string formatting.
        """
        
        nFlebles = 0
        for i in range(len(self.tree.Flebles)):
            nFlebles += self.tree.Flebles[i]

        self.extra_information['flebles'] = (nFlebles, 'd')

            


            
