from manim import *
from manim.opengl import *
import numpy as np

BLACK = "#343434"
SLATE = "#a2a2a2"
WHITE = "#ece6e2"
W = config.frame_width
H = config.frame_height
config.background_color = WHITE


ceil_len = 3
w1 = 6
w2 = w1 * 1.1  # w2 > w1
# A1 = 0.2
# A2 = 0.2
p1 = 0
p2 = 0
L = 4
l = 1.5
sep = 2
T = 4 * PI / (w1 + w2)


class Spring(VMobject):
    def __init__(self, start=ORIGIN, length=2, bumps=14):
        self.length = length
        self.empty = 0.4
        self.step = 0.07
        self.bump = 0.18
        super().__init__(color=BLACK)
        vertices = np.array(
            [
                [0, 0, 0],
                [self.empty, 0, 0],
                [self.empty + self.step, self.bump, 0],
                *[
                    [
                        self.empty + self.step + self.step * 2 * i,
                        self.bump * (1 - (i % 2) * 2),
                        0,
                    ]
                    for i in range(1, bumps)
                ],
                [self.empty + self.step * 2 * bumps, 0, 0],
                [self.empty * 2 + self.step * 2 * bumps, 0, 0],
            ]
        )
        vertices = vertices * [self.length /
                               (1 + 0.2 * bumps), 1, 0] + np.array(start)

        self.start_new_path(np.array(start))
        self.add_points_as_corners(
            [*(np.array(vertex) for vertex in vertices)])


class Test(ThreeDScene):
    def construct(self):
        self.renderer.background_color = WHITE
        # Setup
        a = Circle(radius=0.4, fill_opacity=1).shift(LEFT * sep + DOWN)
        b = Circle(radius=0.4, fill_opacity=1).shift(RIGHT * sep + DOWN)
        l1 = Line(a.get_center() + UP * L, a.get_center()).set_color(BLACK)
        l2 = Line(b.get_center() + UP * L, b.get_center()).set_color(BLACK)
        ceil = VGroup(
            DashedLine(
                start=ceil_len * LEFT,
                end=(ceil_len) * RIGHT,
                dashed_ratio=0.4,
                dash_length=0.2,
                color=BLACK,
            ).shift(l1.get_start()[1] * UP)
        )
        [i.rotate(PI / 4, about_point=i.get_start())
         for i in ceil[0].submobjects]
        ceil.add(
            Line(ceil_len * LEFT, ceil_len * RIGHT,
                 color=BLACK).align_to(ceil, DOWN)
        )
        spring = Spring(l1.get_start() + DOWN * l, 2 * sep)
        d1 = Dot(color=BLACK).move_to(spring.get_start())
        d2 = Dot(color=BLACK).move_to(spring.get_end())
        paint1 = Dot(color=BLACK).move_to(a.shift(DOWN))
        paint2 = Dot(color=BLACK).move_to(b.shift(DOWN))

        # Physics
        t = ValueTracker()
        A1 = ValueTracker(0.4)
        A2 = ValueTracker(0)
        l1.add_updater(
            lambda m: m.set_angle(
                A1.get_value() * np.cos(w1 * t.get_value() + p1)
                + A2.get_value() * np.cos(w2 * t.get_value() + p2)
                - PI / 2
            )
        )
        l2.add_updater(
            lambda m: m.set_angle(
                A1.get_value() * np.cos(w1 * t.get_value() + p1)
                - A2.get_value() * np.cos(w2 * t.get_value() + p2)
                - PI / 2
            )
        )
        a.add_updater(lambda m: m.move_to(l1.get_end()))
        b.add_updater(lambda m: m.move_to(l2.get_end()))

        def springupdater(m: Spring):
            # Modified Mobject.put_start_and_end_on
            curr_start, curr_end = m.get_start_and_end()
            curr_vect = curr_end - curr_start
            target_vect = (
                l2.get_start()
                + (l2.get_end() - l2.get_start()) * l / L
                - l1.get_start()
                - (l1.get_end() - l1.get_start()) * l / L
            )
            axis = (
                normalize(np.cross(curr_vect, target_vect))
                if np.linalg.norm(np.cross(curr_vect, target_vect)) != 0
                else OUT
            )
            m.stretch(
                np.linalg.norm(target_vect) / np.linalg.norm(curr_vect),
                0,
                about_point=curr_start,
            )
            m.rotate(
                angle_between_vectors(curr_vect, target_vect),
                about_point=curr_start,
                axis=axis,
            )
            m.move_to(
                l1.get_start() + (l1.get_end() - l1.get_start()) * l / L,
                aligned_edge=LEFT,
            )

        spring.add_updater(springupdater)
        d1.add_updater(lambda m: m.move_to(spring.get_start()))
        d2.add_updater(lambda m: m.move_to(spring.get_end()))

        paint1.add_updater(lambda m: m.set_x(a.get_x()))
        paint2.add_updater(lambda m: m.set_x(b.get_x()))
        trails = VGroup()

        def add_trail():
            self.play(FadeIn(paint1), FadeIn(paint2), run_time=0.4)
            trails.add(
                VGroup(
                    VMobject()
                    .start_new_path(paint1.get_center())
                    .set_stroke(color=[WHITE, BLACK])
                    .set_sheen_direction(UP),
                    VMobject()
                    .start_new_path(paint2.get_center())
                    .set_stroke(color=[WHITE, BLACK])
                    .set_sheen_direction(UP),
                )
            )
            trails[-1][0].add_updater(
                lambda m, dt: m.shift(DOWN * 0.25 * dt).add_points_as_corners(
                    [paint1.get_center()]
                )
            )
            trails[-1][1].add_updater(
                lambda m, dt: m.shift(DOWN * 0.25 * dt).add_points_as_corners(
                    [paint2.get_center()]
                )
            )

        def remove_trail(play=True):
            if play:
                self.play(FadeOut(paint1), FadeOut(paint2), run_time=0.4)
            for i in trails[-1]:
                i.clear_updaters().add_updater(
                    lambda m, dt: m.shift(
                        DOWN * 0.25 * dt
                    )  # .set_opacity(m.get_stroke_opacity() - 0.2*dt)
                )

        config = {"stroke_color": SLATE,
                  "stroke_width": 2, "stroke_opacity": 0.2}
        grid = NumberPlane(
            background_line_style=config,
            axis_config={"stroke_color": WHITE, "stroke_opacity": 0},
            x_range=(-W, W, 1.5),
            y_range=(-H / 2, H, 1.5),
        )

        rect = Rectangle(WHITE, H, W, fill_opacity=1)
        self.add(l1, l2, spring, ceil, d1,
                 d2, a, b, trails, rect, grid)
        self.play(Create(grid))
        self.play(FadeOut(rect))

        def simulate(time):
            self.play(
                t.animate.increment_value(time),
                trails[-1][0].animate.set_stroke(color=[BLACK, WHITE]),
                trails[-1][1].animate.set_stroke(color=[BLACK, WHITE]),
                rate_func=linear,
                run_time=time,
            )

        add_trail()
        simulate(10 * T)
        remove_trail()
        self.play(A1.animate.set_value(0),
                  A2.animate.set_value(0.4), run_time=2)
        add_trail()
        simulate(10 * T)
        remove_trail()
        self.play(A1.animate.set_value(0.2),
                  A2.animate.set_value(0.2), run_time=2)
        add_trail()
        simulate(25 * T)
        remove_trail(False)
        self.play(
            t.animate.increment_value(1),
            rate_func=lambda x: 2*x-x*x,
            run_time=2,
        )

        banner = ManimBanner(dark_theme=False).scale(
            0.8).move_to([0, 5, 5.5]).rotate(PI / 2, axis=RIGHT)
        banner.anim.rotate(PI / 2, axis=RIGHT)
        self.add(banner)

        self.move_camera(
            phi=PI / 2,
            theta=-PI / 2,
            frame_center=[0, 0, 5],
            added_anims=[grid.animate.set_opacity(0)],
        )

        line = Text("<github.com/sparshg>", color="#a6a6a6").next_to(banner,
                                                                     IN, 2).scale(0.6).rotate(PI / 2, axis=RIGHT)

        self.play(
            LaggedStart(
                banner.expand(),
                Write(line),
                lag_ratio=0.2,
            )
        )
        self.wait()
        self.play(Unwrite(banner), Unwrite(line))
