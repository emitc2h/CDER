#**************************************************#
# file   : core/interface.py                       #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Handles the elements of the 2D scene             #
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

## Pyglet import
import pyglet

####################################################
class Interface():

    ## --------------------------------------- ##
    def __init__(self, window_width, window_height):
        """
        Constructor
        """

        ## Logo ##
        #--------#

        self.image_logo = pyglet.resource.image('core/images/logo_transparent.png')

        ## Scale logo to something small
        self.max_scale_logo = 0.15

        self.logo = pyglet.sprite.Sprite(self.image_logo,
                                         x=window_width - int(self.image_logo.width * self.max_scale_logo * 1.1),
                                         y=int(self.image_logo.height * self.max_scale_logo * 0.1))


        
        ## Help message ##
        #----------------#
        
        self.image_help = pyglet.resource.image('core/images/help.png')

        ## Anchor help message by the center
        self.image_help.anchor_x = self.image_help.width/2
        self.image_help.anchor_y = self.image_help.height/2

        self.help = pyglet.sprite.Sprite(self.image_help,
                                         x=window_width/2,
                                         y=window_height/2)

        ## Control when and how to update help message opacity
        self.help_fade_in    = False
        self.help_fade_out = False

        

        ## Help pointer ##
        #----------------#
        
        self.image_help_pointer = pyglet.resource.image('core/images/help_pointer.png')
        self.help_pointer = pyglet.sprite.Sprite(self.image_help_pointer,
                                                 x=int(self.image_help_pointer.width * 0.04),
                                                 y=int(self.image_help_pointer.height * 0.4))

        

        ## Cut message ##
        #---------------#
        
        self.image_cut = pyglet.resource.image('core/images/cut_message.png')

        ## Anchor help message by the center
        self.image_cut.anchor_x = self.image_cut.width/2
        self.image_cut.anchor_y = self.image_cut.height/2

        self.cut = pyglet.sprite.Sprite(self.image_cut,
                                         x=window_width/2,
                                         y=window_height*0.16)

        ## Control when and how to update cut message opacity
        self.cut_fade_out = False
        self.cut_fade_in = False


        
        ## Cut reset message ##
        #---------------------#
        
        self.image_cut_reset = pyglet.resource.image('core/images/cut_reset.png')

        ## Anchor cut reset message by the center
        self.image_cut_reset.anchor_x = self.image_cut.width/2
        self.image_cut_reset.anchor_y = self.image_cut.height/2

        self.cut_reset = pyglet.sprite.Sprite(self.image_cut_reset,
                                              x=window_width/2,
                                              y=window_height*0.16)

        ## Control when and how to update cut reset message opacity
        self.cut_reset_fade_out = False

        
        
        ## Text editor field ##
        #---------------------#
        
        self.text_field = pyglet.text.Label('',
                                            font_name='Monaco',
                                            font_size=10,
                                            x=window_width*0.02,
                                            y=window_height*0.1,
                                            color=(73, 145, 255, 255),
                                            align='center')


        
        ## Display everything initially
        self.resize(window_width, window_height)

        
        ## Hide some elements initially
        self.help.opacity = 0
        self.cut.opacity = 0
        self.cut_reset.opacity = 0



    ## --------------------------------------- ##
    def resize(self, window_width, window_height):
        """
        Resize and reposition objects according to window size
        """

        ## Calculate a generic scaling tp apply to objects when the window
        ## gets smaller than (400,300)
        scale = 1.0
        if window_width < 400:
            scale *= float(window_width) / 400
        if window_height < 300:
            scale *= float(window_height) / 300

            
        ## Scale and reposition logo
        self.logo.x = window_width - int(self.image_logo.width * scale * self.max_scale_logo * 1.1)
        self.logo.y = int(self.image_logo.height * scale * self.max_scale_logo * 0.1)
        self.logo.scale = scale * self.max_scale_logo


        ## Scale help message and re-center
        self.help.scale = 0.4 * scale
        self.help.x = window_width/2
        self.help.y = window_height/2


        ## Scale and reposition help pointer
        self.help_pointer.x = int(self.image_help_pointer.width * 0.04 * scale)
        self.help_pointer.y = int(self.image_help_pointer.height * 0.4 * scale)
        self.help_pointer.scale = 0.4 * scale


        ## Scale and reposition cut messages
        self.cut.scale = 0.4 * scale
        self.cut.x = window_width/2
        self.cut.y = window_height*0.16

        self.cut_reset.scale = 0.4 * scale
        self.cut_reset.x = window_width/2
        self.cut_reset.y = window_height*0.16

        
        ## Reposition text field
        self.text_field.x = window_width*0.02
        self.text_field.y = window_height*0.1



    ## --------------------------------------- ##
    def set_text(self, text):
        """
        Set the text field content
        """
        self.text_field.text = text



    ## --------------------------------------- ##
    def update(self, dt):
        """
        Update the scene to manage fade in/out effects
        """

        ## Fade in help message
        if self.help_fade_in:
            self.help.opacity += 20
        if self.help.opacity > 255:
            self.help.opacity = 255
            self.help_fade_in = False

        ## Fade out help message
        if self.help_fade_out:
            self.help.opacity -= 20
        if self.help.opacity < 0:
            self.help.opacity = 0
            self.help_fade_out = False

        ## Fade in help message
        if self.cut_fade_in:
            self.cut.opacity += 20
        if self.cut.opacity > 255:
            self.cut.opacity = 255
            self.cut_fade_in = False

        ## Fade out help message
        if self.cut_fade_out:
            self.cut.opacity -= 20
        if self.cut.opacity < 0:
            self.cut.opacity = 0
            self.cut_fade_out = False

        ## Fade out cut reset message
        if self.cut_reset_fade_out:
            self.cut_reset.opacity -= 10
        if self.cut_reset.opacity < 0:
            self.cut_reset.opacity = 0
            self.cut_reset_fade_out = False



    ## --------------------------------------- ##
    def draw(self):
        """
        Draw all 2D scene objects
        """

        ## Draw logo
        self.logo.draw()

        ## Draw help message (only if fading or displayed)
        if self.help.opacity > 0:
            self.help.draw()
        else:
            ## Draw help pointer (only is help message is not displayed)
            self.help_pointer.draw()

        ## Draw cut message (only if fading or displayed)
        if self.cut.opacity > 0:
            self.cut.draw()

        ## Draw cut reset message (only if fading out)
        if self.cut_reset.opacity > 0:
            self.cut_reset.draw()

        ## Draw text field
        self.text_field.draw()



    ## --------------------------------------- ##
    def toggle_help(self):
        """
        Toggle fading in/out of help message
        """

        ## action = fade in or fade out?
        action = 0
        if self.help.opacity == 0 or self.help_fade_out:
            action = 0
        if self.help.opacity == 255 or self.help_fade_in:
            action = 1

        ## Fade in (if not displayed)
        if action == 0:
            self.help_fade_in  = True
            self.help_fade_out = False

        ## Fade out (if displayed)
        if action == 1:
            self.help_fade_in  = False
            self.help_fade_out = True



    ## --------------------------------------- ##
    def toggle_cut(self):
        """
        Toggle fading in/out of cut message
        """

        ## action = fade in or fade out?
        action = 0
        if self.cut.opacity == 0 or self.cut_fade_out:
            action = 0
        if self.cut.opacity == 255 or self.cut_fade_in:
            action = 1

        ## Fade in (if not displayed)
        if action == 0:
            self.cut_fade_in  = True
            self.cut_fade_out = False

        ## Fade out (if displayed)
        if action == 1:
            self.cut_fade_in  = False
            self.cut_fade_out = True


    ## --------------------------------------- ##
    def reset_cut(self):
        """
        Trigger apparition and immediate fade out of
        cut reset message
        """
        
        self.cut_reset.opacity = 255
        self.cut_reset_fade_out = True
        

