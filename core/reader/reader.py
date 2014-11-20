#**************************************************#
# file   : core/reader/reader.py                   #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Generic class providing common facilities to     #
# load ROOT TTrees from file and pass the events   #
# to CDER                                          #
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
from ROOT import TChain, TFile

## Basic python imports
import random as rand
import copy

## CDER particle types imports
from ..particle.jet import Jet
from ..particle.tau import Tau
from ..particle.electron import Electron
from ..particle.muon import Muon
from ..particle.photon import Photon
from ..particle.met import MET

## Default string for no cuts applied
CUT_NO_SELECTION = 'No selection'


####################################################
class Reader():

    ## --------------------------------------- ##
    def __init__(self, file_path, tree_name, initial_cut_string=CUT_NO_SELECTION):
        """
        Constructor
        """

        ## Load the file
        self.chain = TChain(tree_name)
        self.chain.Add(file_path)

        ## tree to keep all events
        self.full_tree = self.chain

        ## tree to keep inly events surviving cut
        self.cut_tree = self.full_tree

        ## Main tree reference
        self.tree = self.full_tree


        ## Tree navigation
        self.entries = self.tree.GetEntries()
        self.event = -1

        ## Cuts
        self.current_cut = initial_cut_string
        self.history = []

        ## Particles to display
        self.event_particles = []

        ## particle data holders
        self.event_jets      = []
        self.event_taus      = []
        self.event_electrons = []
        self.event_muons     = []
        self.event_photons   = []
        self.event_met       = None

        ## extra information holder
        self.extra_information = {}

        ## Set teminal height for nice output
        self.terminal_adjust_height = 1

        if not (initial_cut_string == CUT_NO_SELECTION):
            print 'Applying cut string from config.ini:', initial_cut_string
            print 'Please wait ...'
            if self.cut(initial_cut_string):
                print 'Successful.'
            else:
                print 'There is something wrong with the provided cut string. Please check.'



    ## --------------------------------------- ##
    def reset(self):
        """
        Erase the content of all containers
        """
        
        ## Empty the event particles
        self.event_particles = []

        ## Empty local particle data holders
        self.event_jets      = []
        self.event_taus      = []
        self.event_electrons = []
        self.event_muons     = []
        self.event_photons   = []
        self.event_met       = None



    ## --------------------------------------- ##
    def next(self):
        """
        Fetch next event into local containers
        """

        ## Increment local event iterator
        if self.event <= (self.entries-1):
            self.event += 1

        ## Make sure next has good behavior after cut
        if self.event > (self.entries-1):
            self.event = (self.entries-1)
            ## No new event is selected, tell Display
            return None

        ## Empty local containers
        self.reset()

        ## Set tree pointer to retrieve desired event data
        self.tree.GetEntry(self.event)

        ## Get new particle kinematics
        self.get_particles()

        ## Convert these kinematics into particle objects
        self.make_particles()

        return self.event_particles



    ## --------------------------------------- ##
    def previous(self):
        """
        Fetch previous event into local containers
        """

        ## Decrement local event iterator
        if self.event >= 0:
            self.event -= 1

        ## Initial iterator value is -1, make sure previous has good behavior
        if self.event < 0:
            self.event = 0
            ## No new event is selected, tell Display
            return None

        ## Empty local containers
        self.reset()

        ## Set tree pointer to retrieve desired event data
        self.tree.GetEntry(self.event)

        ## Get new particle kinematics
        self.get_particles()

        ## Convert these kinematics
        self.make_particles()

        return self.event_particles



    ## --------------------------------------- ##
    def random(self):
        """
        Fetch random event into local containers
        """

        ## Empty local containers
        self.reset()

        ## Set local iterator to random value in allowed range
        self.event = rand.randint(0, (self.entries-1))

        ## Set tree pointer to retrieve desired event data
        self.tree.GetEntry(self.event)

        ## Get new particle kinematics
        self.get_particles()

        ## Convert these kinematics
        self.make_particles()

        return self.event_particles



    ## --------------------------------------- ##
    def cut(self, cut_string):
        """
        Select subset of events to inspect based on a cut
        on an existing variable in the tree
        """

        ## Flag for sucessful cut
        cut_applied = False
        
        ## Do not cut if nothing is entered
        if cut_string != '':

            ## Apply the cut by copying a subset of the full tree
            self.cut_tree = self.full_tree.CopyTree(cut_string)
            self.tree     = self.cut_tree

            ## Do not let CDER crash if the cut is not valid, jusr do nothing
            try:
                self.entries = self.cut_tree.GetEntries()
                self.current_cut = cut_string
                cut_applied = True
            except TypeError:
                self.tree = self.full_tree
                print 'Bad cut expression : "%s". Resetting the full tree' % cut_string
                self.current_cut = CUT_NO_SELECTION
                cut_applied = False

            ## Store the cut string in the cut history
            self.history.reverse()
            self.history.append(cut_string)
            self.history.reverse()

        return cut_applied



    ## --------------------------------------- ##
    def reset_cut(self):
        """
        Remove the currently applied cut
        """
        
        self.tree     = self.full_tree
        self.cut_tree = self.full_tree
        self.entries = self.full_tree.GetEntries()
        self.current_cut = CUT_NO_SELECTION



    ## --------------------------------------- ##
    def get_jets(self):
        """
        A method to obtain jet kinematics to be implemented in the derived reader class
        """
        
        print 'WARNING : get_jets() method not imlemented in current Reader'



    ## --------------------------------------- ##
    def get_taus(self):
        """
        A method to obtain tau kinematics to be implemented in the derived reader class
        """
        
        print 'WARNING : get_taus() method not imlemented in current Reader'



    ## --------------------------------------- ##
    def get_electrons(self):
        """
        A method to obtain electron kinematics to be implemented in the derived reader class
        """
        
        print 'WARNING : get_electrons() method not imlemented in current Reader'



    ## --------------------------------------- ##
    def get_muons(self):
        """
        A method to obtain muon kinematics to be implemented in the derived reader class
        """
        
        print 'WARNING : get_muons() method not imlemented in current Reader'



    ## --------------------------------------- ##
    def get_photons(self):
        """
        A method to obtain photon kinematics to be implemented in the derived reader class
        """
        
        print 'WARNING : get_photons() method not imlemented in current Reader'



    ## --------------------------------------- ##
    def get_met(self):
        """
        A method to obtain MET kinematics to be implemented in the derived reader class
        """
        
        print 'WARNING : get_met() method not imlemented in current Reader'



    ## --------------------------------------- ##
    def get_particles(self):
        """Run all the kinematic getters
        """
        
        self.get_jets()
        self.get_taus()
        self.get_electrons()
        self.get_muons()
        self.get_photons()
        self.get_met()
        self.get_extra_information()



    ## --------------------------------------- ##
    def get_extra_information(self):
        """
        A method to obtain variable (key) / content (value) pairs to be printed as
        extra information. Ignore if not implemented.
        """
        
        pass
        


    ## --------------------------------------- ##
    def make_particles(self):
        """
        Convert the obtained kinematics into particle objects to be displayed
        """

        ## Convert jets
        ## 4 values: Pt, Eta, Phi, btag
        for jet in self.event_jets:
            btag = False
            try:
                btag = jet[3]
            except IndexError:
                pass
            new_jet = Jet(jet[0], jet[1], jet[2], btag)
            self.event_particles += new_jet.particles

        ## Convert taus
        ## 3 values: Pt, Eta, Phi
        for tau in self.event_taus:
            new_tau = Tau(tau[0], tau[1], tau[2])
            self.event_particles += new_tau.particles

        ## Convert electrons
        ## 3 values: Pt, Eta, Phi
        for el in self.event_electrons:
            new_el = Electron(el[0], el[1], el[2])
            self.event_particles += new_el.particles

        ## Convert muons
        ## 3 values: Pt, Eta, Phi
        for mu in self.event_muons:
            new_mu = Muon(mu[0], mu[1], mu[2])
            self.event_particles += new_mu.particles

        ## Convert photons
        ## 3 values: Pt, Eta,Phi
        for ph in self.event_photons:
            new_ph = Photon(ph[0], ph[1], ph[2])
            self.event_particles += new_ph.particles

        ## Convert MET
        ## 2 values: Magnitude, Phi
        try:
            met = MET(self.event_met[0], self.event_met[1])
            self.event_particles += met.particles
        except TypeError:
            pass
            


    ## --------------------------------------- ##
    def print_event(self):
        """
        Print the kinematics and extra information to terminal
        """

        ## Do not do anything if no information is stored locally
        if len(self.event_particles) == 0:
            return
        
        ## Clear terminal
        print chr(27) + "[2J"


        
        ## Print kinematics table ##
        #--------------------------#
        
        ## Print header and legend
        print '===='*14
        print '| Event      | {:<40d}|'.format(self.event)
        
        print '----'*14
        print '| object     | {:<12}| {:<12}| {:<12}|'.format('pt [GeV]', 'eta', 'phi')
        print '----'*14

        ## Record the number of lines taken by the kinematics to always place the
        ## kinematics table at the same height
        n_lines = 0

        ## Print electrons
        for el in self.event_electrons:
            print '| \033[34melectron\033[0m   | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(el[0]/1000.0,
                                                                                      el[1],
                                                                                      el[2])
            n_lines +=1

        ## Print muons
        for mu in self.event_muons:
            print '| \033[35mmuon\033[0m       | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(mu[0]/1000.0,
                                                                                      mu[1],
                                                                                      mu[2])
            n_lines +=1

        ## Print taus
        for tau in self.event_taus:
            print '| \033[33mtau\033[0m        | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(tau[0]/1000.0,
                                                                                      tau[1],
                                                                                      tau[2])
            n_lines +=1

        ## Print photons
        for ph in self.event_photons:
            print '| \033[34mphoton\033[0m     | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(ph[0]/1000.0,
                                                                                      ph[1],
                                                                                      ph[2])
            n_lines +=1

        ## Print jets
        for jet in self.event_jets:
            try:
                ## Change jet label color if btag jet
                if jet[3]:
                    print '| \033[36mjet\033[0m        | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(jet[0]/1000.0,
                                                                                              jet[1],
                                                                                              jet[2])
                else:
                    print '| \033[31mjet\033[0m        | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(jet[0]/1000.0,
                                                                                              jet[1],
                                                                                              jet[2])
                        
            except IndexError:
                print '| \033[31mjet\033[0m        | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(jet[0]/1000.0,
                                                                                          jet[1],
                                                                                          jet[2])
            n_lines +=1

        ## Print MET
        try:
            print '| \033[32mMET\033[0m        | {:<12.2f}| {:<12}| {:<12.2f}|'.format(self.event_met[0]/1000.0,
                                                                                       '----', 
                                                                                       self.event_met[1])
        except IndexError:
            pass

        print '===='*14


        
        ## Print extra information ##
        #---------------------------#

        ## Do not print if there is no extra information
        if len(self.extra_information) > 0:

            ## Find out the longest variable name and adjust the table width accordingly
            max_word_length = 0
            
            for key in self.extra_information.iterkeys():
                key_word_length = len(key)
                if key_word_length > max_word_length:
                    max_word_length = key_word_length

            ## Print table header
            print '\n'*(6-n_lines)
            print '='*(max_word_length+21)
            title = '| {:<%d} |' % (max_word_length+17)
            print title.format('Extra Information')
            print '-'*(max_word_length+21)

            ## Print variable-content pairs
            for key in sorted(self.extra_information.iterkeys()):
                n_lines += 1
                information_string = '| {:<%s}| {:<14%s} |' % (max_word_length+1, self.extra_information[key][1])
                print information_string.format(key, self.extra_information[key][0])

            print '='*(max_word_length+21)

        ## Print Number of events available for display and current cut applied
        print '\n'*(self.terminal_adjust_height)
        print '\033[31mEvents :\033[0m %d   \033[31mselection :\033[0m %s' % (self.entries, self.current_cut)

