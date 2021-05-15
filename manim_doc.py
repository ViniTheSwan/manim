from manimlib import *

#to run a new scene

#command line
#manim first_animation.py SquareToCircle -p -ql
#SquareToCircle is the Scene
#-p means play Video right away
#-ql means quality low

#create new scene every Scene inherits form Scene
class NewScene(Scene):
    def construct(self):
        #get the properties of Mobjects
        print(Dot.CONFIG.keys())
        #get the global config
        from manimlib.config import get_custom_config
        config = get_custom_config()

        ## graphical Objects
        circle = Circle(color =RED, radius = 0.2)
        square =  Square(color= BLUE)
        triangle =  Triangle(color = PINK)
        point = Point(np.array([0,0]))
        dot = Dot(np.array([0,0]), radius = 0.1)
        rectangle = Rectangle(height = 2, width = 3)
        edge = Line(
            start_coord,
            end_coord,
            buff = 1,
            stroke_color = RED,
            stroke_width = 1,)
        a = Axes(
            x_min=-3,
            x_max=3,
            x_axis_width=15,
            x_tick_frequency=1,
            x_leftmost_tick=None,
            x_axis_label=None,

            y_min=-3,
            y_max=3,
            y_axis_height=15,
            y_tick_frequency=1,
            y_bottom_tick=None,
            y_labeled_nums=None,
            y_axis_label=None,

            axes_color=WHITE,
            graph_origin=1 * DOWN + 1 * LEFT,
            exclude_zero_label=True,
            num_graph_anchor_points=25,
            default_graph_colors=[BLUE, GREEN, YELLOW],
            default_derivative_color=GREEN,
            default_input_color=YELLOW,
            default_riemann_start_color=BLUE,
            default_riemann_end_color=GREEN,
            function_color=WHITE,
            area_opacity=0.8,
            num_rects=50,
            include_tip=True,
            axis_config={"include_tip": False},
            x_axis_config={"x_min": -40},
            y_axis_config={}
        )
        n = NumberLine()
        f = FunctionGraph(lambda x:x**2, x_min = 3,x_max = 3,color = BLUE)
        f = ParametricFunction(self.func, t_min = - 3, t_max = 3, color=BLUE)

        # graphical actions

        #Grouping
        VGroup(circle, triangle,square) # groups multiple objects, color shifting rotation is applied to all elements
        Group()    # groups for objects not base on bezier curves

        #Animations/Effects
        Write(eq1)    #writes an equation
        ShowCreation(circle)
        FadeIn(circle)
        FadeOut(circle)
        FadeInFromPoint(circle, point)
        FadeIn(circle, shift=LEFT) #shift in from the right side
        ReplacementTransform()
        ShowTextWordByWord(eq1) #writes the text 1 by 1

        ## Latex equations Objects
        eq1 = TexText(r"$\frac{dJ}{d\theta} = \textbf{W}\vec{x} $")

        ## mobject methods
        circle.set_x()
        circle.get_x()
        circle.add_updater(lambda mobj: mobj.set_x(mobj.get_x()+1))
        # mobject transformation
        circle.set_fill(PINK, opacity=0.5) # sets the circle fill color
        eq1.shift(UP)# shifts the mobject up relative to the current position
        circle.move_to(self,point_or_mobject=point)
        circle.move_to(self,point_or_mobject=square)



        #Scene methods
        self.play(Write(eq1), run_time = 3) #play the given animation, run_time modifies the duration of the animation
        self.play(circle.shift, UP) #play the shifting of the circle as animation
        self.add(eq1)    #add an object to a Scene without animation
        self.remove(eq1)  # removes the object from the screen
        self.wait(1)     #pauses the animtion for the given amount of seconds

        #change camera settings
        self.play(
            # Set the size with the width of a object
            self.camera.frame.set_width, 20,

        )
