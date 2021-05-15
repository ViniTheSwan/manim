from upload.neural_network import NeuralNetwork
from grant_network import NetworkMobject
from manimlib import *


class myNetworkMobject(NetworkMobject):
    CONFIG = {
        "edge_propogation_color": BLUE,
        "edge_propogation_time": 0.6,
    }


class DotsMoving(Scene):
    def construct(self):
        dots = [Dot() for i in range(5)]
        directions = [np.random.randn(3) for dot in dots]
        self.add(*dots)  # It isn't absolutely necessary
        animations = [ApplyMethod(dot.shift, direction) for dot, direction in zip(dots, directions)]
        self.play(*animations)  # * -> unpacks the list animations



class SynSpike(Scene):
    def construct(self):
        n1 = myNetworkMobject(NeuralNetwork((10,10,10)),)

        self.play(FadeIn(n1))
        dots = [Dot(edge.get_start(), radius = 0.05, fill_opacity = 0.5, color = RED) for edge in n1.edge_groups[0]]
        self.add(*dots)
        animations = [ApplyMethod(dot.move_to,edge.get_end())for dot, edge in zip(dots, n1.edge_groups[0])]
        self.play(*animations)
        self.remove(*dots)
class AsynSpike(Scene):
    def construct(self):
        n1 = myNetworkMobject(NeuralNetwork((10,10,10)),)
        self.play(FadeIn(n1))
        all_edges = []
        for edges in n1.edge_groups:
            all_edges.extend(edges)
        print(all_edges)
        for i in range(10):
            self.wait(np.random.random())
            r = np.random.randint(len(all_edges))
            edge = all_edges[r]
            dot = Dot(edge.get_start(), radius = 0.05, fill_opacity = 0.5, color = RED)
            self.add(dot)
            self.play(ApplyMethod(dot.move_to, edge.get_end()), run_time = 0.3)
            self.remove(dot)
class AsynSpike2(Scene):
    def construct(self):
        def update(mobj,dt):
            print(dt)
            fps = self.camera.frame_rate
            if dt != 0 :
                mobj = mobj.set_x(mobj.get_x() + (mobj.distance[0] / fps / mobj.duration))
                mobj = mobj.set_y(mobj.get_y() + (mobj.distance[1] / fps / mobj.duration))
            return mobj

        n1 = myNetworkMobject(NeuralNetwork((10,10,10)),)
        self.play(FadeIn(n1))
        all_edges= []
        for edges in n1.edge_groups:
            all_edges.extend(edges)
        ovr_duration = 10
        signal_density = 0.8
        start = time.time()*10
        dots = []
        while time.time()-start <= 5:
            starting = time.time()
            if signal_density > np.random.random():
                r = np.random.randint(len(all_edges))
                edge = all_edges[r]
                dot = Dot(edge.get_start(), radius=0.05, fill_opacity=0.5, color=RED)
                dot.duration = (np.random.random()/8+0.2)
                dot.end = time.time() + dot.duration
                dot.distance = edge.get_end()-edge.get_start()

                dot.add_updater(update)
                self.add(dot)
                dots.append(dot)


            # wait random seconds between 0 and 1
            lag = time.time()-starting
            for dot in dots:
                dot.end += lag
                if time.time() > dot.end:
                    dot.clear_updaters()
                    self.remove(dot)

            self.wait(0.1)
class Test(Scene):
    def construct(self):
        edge = Line(start = LEFT, end = RIGHT)
        circle = Circle(radius = 0.05)
        circle.move_to(edge.get_start())

        self.add(edge)
        self.add(circle)
        fps = self.camera.frame_rate
        print(fps)
        circle.distance = edge.get_end()- edge.get_start()
        print(circle.distance)
        circle.duration = 4
        def update(mobj,dt):
            #self.wait(1/fps)
            #time.sleep(1/fps)
            print(dt)
            if(dt!= 0 ):
                mobj = mobj.shift((mobj.distance / fps / mobj.duration ))
            #mobj = mobj.set_y(mobj.get_y() + (mobj.distance[1] / fps / mobj.duration))
            return mobj

        circle.add_updater( update_function = update, )
        self.wait(circle.duration)
        circle.clear_updaters()
        #self.remove(circle)


class EdgeActivation(Scene):
    def construct(self):
        n1 = myNetworkMobject(NeuralNetwork((10, 10, 10)), )
        self.play(FadeIn(n1))
        self.play(*n1.activate_edges(0))
        self.play(*n1.deactivate_edges())
        self.play(*n1.activate_edges(1))
        self.play(*n1.deactivate_edges())
        self.play(ScaleInPlace(n1, 0.5))


class Landscape(ThreeDScene):
    def construct(self):
        pass
class GraphScene(FunctionGraph):
    def construct(self):
        pass
class TestScene(Scene):
    def construct(self):

        line = Line(np.array([0,0]),np.array([1,1]))
        circle = Circle(color = BLUE, radius = 0.4, )
        circle.set_fill(PINK, opacity = 0.2)

        self.add(line)
        self.add(circle)
        self.play(circle.move_to,line.end)

class BitcoinGraph(Scene):
    def construct(self):
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
            include_tip = True,
        )
        f = a.get_graph(self.func)
        self.add(a)
        self.play(Write(f))
        #self.play(FadeIn(a))
        #a.get_graph(self.func)
    def func(self, x):
        return x**2