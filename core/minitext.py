
def pop_begin(string):
    first_character = string[0]
    string = string[1:len(string)]
    return first_character, string

def pop_end(string):
    last_character = string[-1]
    string = string[0:len(string)-1]
    return last_character, string


class MiniText():

    def __init__(self, max_characters, multiline=False):

        self.max_characters = max_characters
        self.n_characters  = 0
        self.prompt        = '> '
        self.segment_1     = ''
        self.sep_time      = 0.0
        self.sep_visible   = '|'
        self.sep_invisible = ' '
        self.sep           = '|'
        self.segment_2     = ''
        self.kill_ring     = ''

        self.full_output = ''
        self.update_full_output()

        self.text_output = ''
        self.update_text_output()

        
    def update_full_output(self):
        self.full_output = self.prompt + \
          self.segment_1 + \
          self.sep + \
          self.segment_2

          
    def update_text_output(self):
        self.text_output = self.segment_1 + self.segment_2


    def update_all(self):
        self.update_full_output()
        self.update_text_output()
        self.n_characters = len(self.segment_1) + len(self.segment_2)


    def update(self, dt):
        self.sep_time += dt
        if self.sep_time > 0.25:
            self.sep = self.sep_invisible
        if self.sep_time > 0.50:
            self.sep = self.sep_visible
        if self.sep_time > 0.75:
            self.sep = self.sep_invisible
            self.sep_time = 0.0

        self.update_all()


    def set(self, text):
        self.segment_1 = text
        self.segment_2 = ''
        self.update_all()
            
        
    def insert(self, character):
        if self.n_characters <= self.max_characters:
            self.segment_1 += character
            self.update_all()

        
    def backspace(self):
        if len(self.segment_1) > 0:
            self.segment_1 = self.segment_1[0:len(self.segment_1)-1]
            self.update_all()


    def delete(self):
        if len(self.segment_2) > 0:
            self.segment_2 = self.segment_2[1:len(self.segment_2)]
            self.update_all()


    def kill(self):
        if len(self.segment_2) > 0:
            self.kill_ring = self.segment_2
            self.segment_2 = ''
            self.update_all()


    def yank(self):
        if not self.kill_ring == '':
            if self.n_characters + len(self.kill_ring) > self.max_characters:
                n = self.max_characters - (self.n_characters + len(self.kill_ring))
                self.segment_1 += self.kill_ring[0:n]
            else:
                self.segment_1 += self.kill_ring
            self.update_all()
        
        
    def cursor_left(self):
        if not len(self.segment_1) == 0:
            character, new_segment = pop_end(self.segment_1)
            self.segment_2 = character + self.segment_2
            self.segment_1 = new_segment
            self.update_all()

        
    def cursor_right(self):
        if not len(self.segment_2) == 0:
            character, new_segment = pop_begin(self.segment_2)
            self.segment_1 = self.segment_1 + character
            self.segment_2 = new_segment
            self.update_all()


    def goto_end(self):
        self.segment_1 = self.segment_1 + self.segment_2
        self.segment_2 = ''


    def goto_begin(self):
        self.segment_2 = self.segment_1 + self.segment_2
        self.segment_1 = ''


    def reset(self):
        self.segment_1 = ''
        self.segment_2 = ''
