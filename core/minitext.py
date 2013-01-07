#**************************************************#
# file   : core/minitext.py                        #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A on-line text editor with basic shell-like      #
# calabilities                                     #
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


## --------------------------------------- ##
def pop_begin(string):
    """
    take out the first character of a string, return it plus
    the rest of the string
    """
    first_character = string[0]
    string = string[1:len(string)]
    return first_character, string


## --------------------------------------- ##
def pop_end(string):
    """
    take out the last character of a string, return it plus
    the rest of the string
    """
    last_character = string[-1]
    string = string[0:len(string)-1]
    return last_character, string


####################################################
class MiniText():

    ## --------------------------------------- ##
    def __init__(self, max_characters):

        ## Set a maximum number of characters
        self.max_characters = max_characters

        ## Current number of characters
        self.n_characters  = 0

        ## Prompt
        self.prompt        = '> '

        ## Edited text segment
        self.segment_1     = ''

        ## Cursor and parameters
        self.cursor_time      = 0.0
        self.cursor_visible   = '|'
        self.cursor_invisible = ' '
        self.cursor           = '|'

        ## Non-edited text segment (except for calls to delete)
        self.segment_2     = ''
        self.kill_ring     = ''

        ## Displayed output with prompt and cursor
        self.full_output = ''
        self.update_full_output()

        ## Intended output without prompt or cursor
        self.text_output = ''
        self.update_text_output()



    ## --------------------------------------- ##
    def update_full_output(self):
        """
        Update the displayed output with prompt and cursor
        """
        self.full_output = self.prompt + \
          self.segment_1 + \
          self.cursor + \
          self.segment_2



    ## --------------------------------------- ##
    def update_text_output(self):
        """
        Update the intended output without prompt and cursor
        """
        self.text_output = self.segment_1 + self.segment_2



    ## --------------------------------------- ##
    def update_all(self):
        """
        Update all outputs and new number of characters
        """
        self.update_full_output()
        self.update_text_output()
        self.n_characters = len(self.segment_1) + len(self.segment_2)



    ## --------------------------------------- ##
    def update(self, dt):
        """
        Time sensitive update for flashing cursor, update outputs too
        """
        self.cursor_time += dt
        if self.cursor_time > 0.25:
            self.cursor = self.cursor_invisible
        if self.cursor_time > 0.50:
            self.cursor = self.cursor_visible
        if self.cursor_time > 0.75:
            self.cursor = self.cursor_invisible
            self.cursor_time = 0.0

        self.update_all()



    ## --------------------------------------- ##
    def set(self, text):
        """
        Replace the text currently in the editor, place cursor
        afterwards
        """
        self.segment_1 = text
        self.segment_2 = ''
        self.update_all()
            


    ## --------------------------------------- ##
    def insert(self, character):
        """
        Insert a new character at the end of the edited segment
        """
        if self.n_characters <= self.max_characters:
            self.segment_1 += character
            self.update_all()



    ## --------------------------------------- ##
    def backspace(self):
        """
        Erase last character of edited segment
        """
        if len(self.segment_1) > 0:
            self.segment_1 = self.segment_1[0:len(self.segment_1)-1]
            self.update_all()



    ## --------------------------------------- ##
    def delete(self):
        """
        Erase first character of non-edited segment
        """
        if len(self.segment_2) > 0:
            self.segment_2 = self.segment_2[1:len(self.segment_2)]
            self.update_all()



    ## --------------------------------------- ##
    def kill(self):
        """
        Put the non-edited segment into the kill ring
        """
        if len(self.segment_2) > 0:
            self.kill_ring = self.segment_2
            self.segment_2 = ''
            self.update_all()



    ## --------------------------------------- ##
    def yank(self):
        """
        Put back the kill ring content where the cursor is
        """
        if not self.kill_ring == '':
            if self.n_characters + len(self.kill_ring) > self.max_characters:
                n = self.max_characters - (self.n_characters + len(self.kill_ring))
                self.segment_1 += self.kill_ring[0:n]
            else:
                self.segment_1 += self.kill_ring
            self.update_all()
        


    ## --------------------------------------- ##
    def cursor_left(self):
        """
        Move cursor to the left
        (transfer last character of edited segment to the beginning
        of the non-edited segment)
        """
        if not len(self.segment_1) == 0:
            character, new_segment = pop_end(self.segment_1)
            self.segment_2 = character + self.segment_2
            self.segment_1 = new_segment
            self.update_all()



    ## --------------------------------------- ##
    def cursor_right(self):
        """
        Move cursor to the right
        (transfer first character of non-edited segment to the end
        of the edited segment)
        """
        if not len(self.segment_2) == 0:
            character, new_segment = pop_begin(self.segment_2)
            self.segment_1 = self.segment_1 + character
            self.segment_2 = new_segment
            self.update_all()



    ## --------------------------------------- ##
    def goto_end(self):
        """
        Move cursor to the end
        (all characters in edited segment)
        """
        self.segment_1 = self.segment_1 + self.segment_2
        self.segment_2 = ''



    ## --------------------------------------- ##
    def goto_begin(self):
        """
        Move cursor to the beginning
        (all characters in non-edited segment)
        """
        self.segment_2 = self.segment_1 + self.segment_2
        self.segment_1 = ''



    ## --------------------------------------- ##
    def reset(self):
        """
        Erase text editor content
        """
        self.segment_1 = ''
        self.segment_2 = ''
