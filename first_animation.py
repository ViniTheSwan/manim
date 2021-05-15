from manim import *
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3*TAU/8)
        circle.set_fill(PINK, opacity = 0.5)
        circle = Circle(color=RED)

        #self.play(ShowCreation(circle))
        #self.play(Transform(square, circle))
        #self.play(FadeOut(square))




        #LATEX in use
        eq1 = TextMobject(r"$\frac{dJ}{d\theta} = \textbf{W}\vec{x} $")
        eq1.shift(UP)
        #self.play(Write(eq1))

