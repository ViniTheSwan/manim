"""Mobject representing highlighted source code listings."""
import html
from manimlib.constants import *
from manimlib.container.container import Container
from manimlib.mobject.geometry import Rectangle, Dot, RoundedRectangle
from manimlib.mobject.shape_matchers import SurroundingRectangle
from manimlib.mobject.svg.text_mobject import Paragraph
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.animation.creation import Write, ShowCreation
from manimlib.animation.fading import FadeIn
import os
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from manimlib.scene.scene import Scene

from manimlib.event_handler.event_listner import EventListner
from manimlib.event_handler.event_type import EventType

'''
1) Code is VGroup() with three things
    1.1) Code[0] is Code.background_mobject
        which can be a 
            1.1.1) Rectangle() if background == "rectangle" 
            1.1.2) VGroup() of Rectangle() and Dot() for three buttons if background == "window" 
    1.2) Code[1] is Code.line_numbers Which is a Paragraph() object, this mean you can use 
                Code.line_numbers[0] or Code[1][0] to access first line number 
    1.3) Code[2] is Code.code
        1.3.1) Which is a Paragraph() with color highlighted, this mean you can use 
            Code.code[1] or Code[2][1] 
                line number 1
            Code.code[1][0] or Code.code[1][0] 
                first character of line number 1
            Code.code[1][0:5] or Code.code[1][0:5] 
                first five characters of line number 1
'''


class CodeScene(Scene):
    def write_code(self, filename=None, code_str=None, style = "typewriter", stroke_time = 0.1, line_time = 1, user_control = True):
        code = Code(file_name=filename, code_str=code_str)
        self.play(*code.FadeInWindow())
        self.add(*code.code)
        self.add(*code.line_numbers)
        code.code.set_opacity(0)
        code.line_numbers.set_opacity(0)
        if style == "typewriter":
            for line_nr in range(len(code.code)):
                code.line_numbers[line_nr].set_opacity(1)
                #self.add_sound(f"typewriter{np.random.randint(1,11)}.wav")
                self.wait(stroke_time*np.random.uniform(0.2,0.8))
                for char_nr in range(len(code.code[line_nr])):
                    code.code[line_nr][char_nr].set_opacity(1)
                    if not type(code.code[line_nr][char_nr]) == Dot:
                        self.add_sound(f"typewriter{np.random.randint(1,11)}.wav")
                    else:
                        self.add_sound("space.wav")
                    self.wait(stroke_time*np.random.uniform(0.2,0.8))
                self.add_sound("bell.wav")
                if user_control: input()
                else: self.wait(line_time*0.5*np.random.uniform(0.2,0.8))
                self.add_sound("carriage_return.wav")
                if line_nr > 15:
                    code.center_to_code()
                self.wait(line_time*0.5*np.random.uniform(0.2,0.8))
        if style == "keyboard":
            pass

class Code(VGroup):
    CONFIG = {
        "tab_width": 1,
        "line_spacing": 0.3,     # space between the lines
        "scale_factor": 0.4,
        "run_time": 1,
        #"font": 'Monospac821 BT',
        #"font": 'Arial',
        #"font": "DejaVu Sans Mono",
        "font": "Courier New",
        #"font": 'Courier New',
        "font_size": 48,
        'stroke_width': 0,
        'margin': 0.3,
        'indentation_char': " ",
        "background": "window",  #rectangle or window
        "corner_radius": 0.2,
        'insert_line_no': True,
        'line_no_from': 1,
        "line_no_buff": 0.4,
        'style': 'railscasts',           #white based:railscasts, vim , material, native; black based: tango, xcode ;
                                      #pink-based: paraiso-light; styles not highlithing print() and list(): monokai, fruity, paraiso-dark
                                      #grey-based: arduino, solarized-dark, solarized-light
                                    #beige-based: inkpot, zenburn
        'language': 'python',
        'generate_html_file': False,
        'adapting_x': False,
        'adapting_y': False,
        'center_y': True,
    }

    def __init__(self, file_name=None,code_str = None, **kwargs):
        Container.__init__(self, **kwargs)
        self.file_name = file_name
        self.code_str = code_str
        self.ensure_valid_file()
        self.style = self.style.lower()
        self.gen_html_string()
        strati = self.html_string.find("background:")
        self.background_color = self.html_string[strati + 12:strati + 19]
        self.gen_code_json()

        self.code = self.gen_colored_lines()

        if self.insert_line_no:
            self.line_numbers = self.gen_line_numbers()
            self.line_numbers.next_to(self.code, direction=LEFT, buff=self.line_no_buff)

        if self.background == "rectangle":
            if self.insert_line_no:
                forground = VGroup(self.code, self.line_numbers)
            else:
                forground = self.code
            self.background_mobject = SurroundingRectangle(forground, buff=self.margin,
                                                           color=self.background_color,
                                                           fill_color=self.background_color,
                                                           stroke_width=0,
                                                           fill_opacity=1, )

            self.background_mobject.round_corners(self.corner_radius)
        else:
            if self.insert_line_no:
                forground = VGroup(self.code, self.line_numbers)
            else:
                forground = self.code

            height = forground.get_height() + 0.1 * 3 + 2 * self.margin
            width = forground.get_width() + 0.1 * 3 + 2 * self.margin

            rrect = RoundedRectangle(corner_radius=self.corner_radius, height=height, width=width,
                                     stroke_width=0,
                                     color= GREY_E, fill_opacity=1)
            red_button = Dot(radius=0.1, stroke_width=0, color='#ff5f56')
            red_button.shift(LEFT * 0.1 * 3)
            yellow_button = Dot(radius=0.1, stroke_width=0, color='#ffbd2e')
            green_button = Dot(radius=0.1, stroke_width=0, color='#27c93f')
            green_button.shift(RIGHT * 0.1 * 3)
            buttons = VGroup(red_button, yellow_button, green_button)
            buttons.shift(
                UP * (height / 2 - 0.1 * 2 - 0.05) + LEFT * (width / 2 - 0.1 * 5 - self.corner_radius / 2 - 0.05))

            self.background_mobject = VGroup(rrect,buttons)
            x = (height - forground.get_height()) / 2 - 0.1 * 3
            self.background_mobject.shift(forground.get_center())
            self.background_mobject.shift(UP * x)



        if self.insert_line_no:
            VGroup.__init__(self, self.background_mobject, self.line_numbers, *self.code, **kwargs)
        else:
            VGroup.__init__(self, self.background_mobject, Dot(fill_opacity=0, stroke_opacity=0), *self.code, **kwargs)

        window = RIGHT_SIDE[0] - LEFT_SIDE[0]
        width = self.background_mobject.get_width()
        print(width)
        scale_x = window / width * 0.96

        window = TOP[1] - BOTTOM[1]
        print(window)
        width = self.background_mobject.get_height()
        scale_y = window / width * 0.96


        if self.adapting_x and scale_x < scale_y:
            self.scale(scale_x)
        if self.adapting_y and scale_y <= scale_x:
            self.scale(scale_y)
        self.align_to(LEFT_SIDE + self.margin, LEFT)
        self.align_to(TOP - self.margin+0.42*(self.code.char_height + self.code.line_spacing)*self.scale_factor, UP)

    def FadeInWindow(self):
        return FadeIn(self.background_mobject),
    '''
    def Write(self):
        write_code = [Write(line) for line in self.code.lines[0]]
        write_line_numbers = [Write(number) for number in self.line_numbers.lines[0]]
        write_all = [item for sublist in zip(write_line_numbers, write_code) for item in sublist]
        return write_all
    def ShowCreation(self):
        write_code = [ShowCreation(line, duration= 1) for line in self.code.lines[0]]
        write_line_numbers = [ShowCreation(number) for number in self.line_numbers.lines[0]]
        write_all = [item for sublist in zip(write_line_numbers, write_code) for item in sublist]

        return write_all
    '''
    def center_to_code(self):
        if self.center_y:
            print(self.get_y()-self.code.lines[0][0].get_height()+self.code.line_spacing)
            self.set_y(self.get_y()+(self.code.char_height + self.code.line_spacing)*self.scale_factor)
    def apply_points_function_about_point(self, func, about_point=None, about_edge=None):
        if about_point is None:
            if about_edge is None:
                about_edge = self.get_corner(UP + LEFT)
            about_point = self.get_critical_point(about_edge)
        for mob in self.family_members_with_points():
            mob.points -= about_point
            mob.points = func(mob.points)
            mob.points += about_point
        return self

    def ensure_valid_file(self):
        if not self.file_name is None:
            possible_paths = [
                os.path.join(os.path.join("assets", "codes"), self.file_name),
                self.file_name,
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    self.file_path = path
                    return
            raise IOError("No file matching %s in codes directory" %
                          self.file_name)

    def gen_line_numbers(self):
        line_numbers_array = []
        for line_no in range(0, self.code_json.__len__()):
            number = str(self.line_no_from + line_no)
            line_numbers_array.append(number)
        #color  ="#E6E8E8"
        line_numbers = Paragraph(*[i for i in line_numbers_array], line_spacing=self.line_spacing,
                            alignment="left", font=self.font,stroke_width=self.stroke_width,
                             ).scale(self.scale_factor)
        return line_numbers

    def gen_colored_lines(self):

        lines_text = []
        for line_no in range(0, self.code_json.__len__()):
            line_str = ""
            for word_index in range(self.code_json[line_no].__len__()):
                line_str = line_str + self.code_json[line_no][word_index][0]
            lines_text.append(self.tab_spaces[line_no] * "\t" + line_str)
        #print(lines_text)
        code = Paragraph(*[text for text in lines_text], line_spacing=self.line_spacing, tab_width=self.tab_width,
                    alignment="left", font=self.font, stroke_width=self.stroke_width, unpack_groups = True).scale(self.scale_factor)
        for line_no in range(code.__len__()):
            line = code[line_no]
            line_char_index = self.tab_spaces[line_no]
            for word_index in range(self.code_json[line_no].__len__()):
                line[line_char_index:line_char_index + self.code_json[line_no][word_index][0].__len__()].set_color(
                    self.code_json[line_no][word_index][1])
                line_char_index += self.code_json[line_no][word_index][0].__len__()
        #print(self.code_json)
        return code


    def gen_html_string(self):
        if self.file_name:
            file = open(self.file_path, "r")
            code_str = file.read()
            file.close()
        if self.code_str:
            code_str = self.code_str
        self.html_string = hilite_me(code_str, self.language, {}, self.style, self.insert_line_no,
                                     "border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;")

        if self.generate_html_file:
            os.makedirs(os.path.join("assets", "codes", "generated_html_files"), exist_ok=True)
            file = open(os.path.join("assets", "codes", "generated_html_files", self.file_name + ".html"), "w")
            file.write(self.html_string)
            file.close()

    def gen_code_json(self):
        #print(self.html_string)
        if self.background_color == "#111111" or \
                self.background_color == "#272822" or \
                self.background_color == "#202020" or \
                self.background_color == "#000000":
            self.default_color = "#ffffff"
        else:
            self.default_color = "#000000"

        for i in range(3, -1, -1):
            self.html_string = self.html_string.replace("</" + " " * i, "</")
        for i in range(10, -1, -1):
            self.html_string = self.html_string.replace("</span>" + " " * i, " " * i + "</span>")

        self.html_string = self.html_string.replace("background-color:", "background:")

        if self.insert_line_no:
            start_point = self.html_string.find("</td><td><pre")
            start_point = start_point + 9
        else:
            start_point = self.html_string.find("<pre")
        self.html_string = self.html_string[start_point:]
        # print(self.html_string)
        lines = self.html_string.split("\n")
        lines = lines[0:lines.__len__() - 2]
        start_point = lines[0].find(">")
        lines[0] = lines[0][start_point + 1:]
        # print(lines)
        self.code_json = []
        self.tab_spaces = []
        code_json_line_index = -1
        #print(self.html_string)
        starting_string = ""
        for line_index in range(0, lines.__len__()):
            if lines[line_index].__len__() == 0:
                continue
            #print(lines[line_index])
            self.code_json.append([])
            code_json_line_index = code_json_line_index + 1
            if lines[line_index].startswith(self.indentation_char):
                start_point = lines[line_index].find("<")
                starting_string = lines[line_index][:start_point]
                indentation_char_count = lines[line_index][:start_point].count(self.indentation_char)
                if starting_string.__len__() != indentation_char_count * self.indentation_char.__len__():
                    lines[line_index] = "\t" * indentation_char_count + starting_string[starting_string.rfind(
                        self.indentation_char) + self.indentation_char.__len__():] + \
                                        lines[line_index][start_point:]
                else:
                    lines[line_index] = "\t" * indentation_char_count + lines[line_index][start_point:]

            indentation_char_count = 0
            while lines[line_index][indentation_char_count] == '\t':
                indentation_char_count = indentation_char_count + 1
            self.tab_spaces.append(indentation_char_count)
            # print(lines[line_index])
            lines[line_index] = self.correct_non_span(lines[line_index])
            # print(lines[line_index])
            words = lines[line_index].split("<span")
            for word_index in range(1, words.__len__()):
                color_index = words[word_index].find("color:")
                if color_index == -1:
                    color = self.default_color
                else:
                    starti = words[word_index][color_index:].find("#")
                    color = words[word_index][color_index + starti:color_index + starti + 7]

                start_point = words[word_index].find(">")
                end_point = words[word_index].find("</span>")
                text = words[word_index][start_point + 1:end_point]
                text = html.unescape(text)
                if text != "":
                    #print(text, "'" + color + "'")
                    self.code_json[code_json_line_index].append([text, color])
        #print(self.code_json)

    def correct_non_span(self, line_str):
        words = line_str.split("</span>")
        line_str = ""
        for i in range(0, words.__len__()):
            if i != words.__len__() - 1:
                j = words[i].find("<span")
            else:
                j = words[i].__len__()
            temp = ""
            starti = -1
            for k in range(0, j):
                if words[i][k] == "\t" and starti == -1:
                    continue
                else:
                    if starti == -1: starti = k
                    temp = temp + words[i][k]
            if temp != "":
                if i != words.__len__() - 1:
                    temp = '<span style="color:' + self.default_color + '">' + words[i][starti:j] + "</span>"
                else:
                    temp = '<span style="color:' + self.default_color + '">' + words[i][starti:j]
                temp = temp + words[i][j:]
                words[i] = temp
            if words[i] != "":
                line_str = line_str + words[i] + "</span>"
        return line_str


def hilite_me(code, lexer, options, style, linenos, divstyles):
    lexer = lexer or 'python'
    style = style or 'colorful'
    defstyles = 'overflow:auto;width:auto;'

    formatter = HtmlFormatter(style=style,
                              linenos=False,
                              noclasses=True,
                              cssclass='',
                              cssstyles=defstyles + divstyles,
                              prestyles='margin: 0')
    html = highlight(code, get_lexer_by_name(lexer, **options), formatter)
    #print(html)
    if linenos:
        html = insert_line_numbers(html)
    html = "<!-- HTML generated using hilite.me -->" + html
    return html


def get_default_style():
    return 'border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;'


def insert_line_numbers(html):
    match = re.search('(<pre[^>]*>)(.*)(</pre>)', html, re.DOTALL)
    if not match: return html

    pre_open = match.group(1)
    pre = match.group(2)
    pre_close = match.group(3)

    html = html.replace(pre_close, '</pre></td></tr></table>')
    numbers = range(1, pre.count('\n') + 1)
    format = '%' + str(len(str(numbers[-1]))) + 'i'
    lines = '\n'.join(format % i for i in numbers)
    html = html.replace(pre_open, '<table><tr><td>' + pre_open + lines + '</pre></td><td>' + pre_open)
    return html