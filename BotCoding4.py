from manimlib.mobject.svg.Code import CodeScene
from manimlib.scene.scene import Scene
from manimlib.mobject.svg.text_mobject import Text
from manimlib import *
import numpy as np

class Coding(CodeScene):
    def construct(self):
        self.write_code( filename = "manim_doc.py", code_str= None)

