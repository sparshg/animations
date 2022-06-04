import random
from manim import *
from manim_physics import *

from manim.utils.rate_functions import (
    ease_in_circ,
    ease_out_quad,
    ease_out_quart,
)

FONT = "product sans"
BLACK = "#343434"
SLATE = "#a2a2a2"
WHITE = "#ece6e2"
W = config.frame_width
H = config.frame_height
config.background_color = WHITE


class Test(SpaceScene, MovingCameraScene):
    def setup(self):
        self.add(self.space)
        ChangeSpeed.add_updater(self.space, lambda space, dt: space.space.step(dt))

    def construct(self):
        config = {"stroke_color": SLATE, "stroke_width": 2, "stroke_opacity": 0.2}
        grid = NumberPlane(
            background_line_style=config,
            axis_config={"stroke_color": WHITE, "stroke_opacity": 0},
            x_range=(-W, W * 20, 1.5),
            y_range=(-H, H * 19, 1.5),
        )

        ground = Line(LEFT * 4, RIGHT * 4).shift(DOWN * 1.53).set_color(BLACK)

        square = (
            Square(1, fill_opacity=1)
            .set_color(BLACK)
            .shift(UP * 3)
            .rotate(PI / 15)
            .shift(LEFT)
        )

        self.make_static_body(ground)
        self.make_rigid_body(square, elasticity=0.2, friction=1)

        self.add(grid, square)
        self.wait(3)

        self.remove(square)
        square = (
            Square(1, fill_opacity=1).set_color(BLACK).shift(DOWN)
        )  # .move_to(square)
        self.add(grid, square)

        self.play(
            Rotating(
                square,
                radians=PI / 4,
                about_point=square.get_corner(DL),
                run_time=0.6,
                rate_func=ease_out_quart,
            ),
        )
        # square.rotate(PI / 4, about_point=square.get_corner(DL))

        def lerp(a, b, t):
            return a * (1 - pow(t, 2)) + b * pow(t, 2)

        def test(x):
            test.t += 0.015
            if test.t > 1:
                test.t = 1
            p = square.body.position
            x.move_to(lerp(x.get_center(), np.array([p.x, p.y, 0]), test.t))

        test.t = 0
        self.camera.frame.add_updater(test)
        self.make_rigid_body(square)
        self.play(self.camera.frame.animate.scale(1), run_time=0.1)
        square.body.apply_impulse_at_local_point((30, 4), (0.06, 0.06))
        self.wait()
        self.camera.frame.clear_updaters()

        v = square.body.velocity

        pos = square.body.position
        self.camera.frame.move_to(square)

        def update_grid(x, dt):
            update_grid.y -= dt * 5
            return x.shift(-np.array((v.x, update_grid.y, 0)) * dt)

        update_grid.y = v.y

        ChangeSpeed.add_updater(grid, update_grid)

        def update_square(x):
            x.body.position = pos
            x.body.velocity = 0, 0

        square.add_updater(update_square)
        self.play(
            self.camera.frame.animate(run_time=0.5).scale(0.35),
            rate_func=ease_in_circ,
        )
        # grid.clear_updaters()
        self.play(
            ChangeSpeed(
                AnimationGroup(
                    Wait(2),
                    self.camera.frame.animate(
                        run_time=0.2, rate_func=ease_out_quad
                    ).scale(1 / 0.35),
                    lag_ratio=1,
                ),
                {0: 0.1, 0.5: 0.5, 0.8: 0.5, 1: 1},
            ),
        )

        wall = Rectangle(color=BLACK, fill_opacity=1, height=2 * H, width=4).move_to(
            self.camera.frame.get_center() + (W / 2 + 2) * RIGHT
        )

        self.play(
            ChangeSpeed(
                wall.animate(rate_func=linear, run_time=4 / v.x).shift(LEFT * 4),
                {0.4: 0.05, 0.7: 0.05, 1: 1},
            ),
        )
        grid.clear_updaters()
        square.remove_updater(update_square)
        square.body.velocity = v.x, 0
        square.body.position = (
            square.body.position.x + v.x / 60,
            square.body.position.y,
        )
        # self.add(wall.shift(LEFT * 4))
        self.wait(0.15)
        # self.play(ChangeSpeed(Wait(0.15), {0.2: 0.05, 0.5: 0.05, 1: 1}))

        particles = VGroup(
            *[
                Poly(
                    [-0.2, -0.12, 0],
                    [0.2, -0.12, 0],
                    [(random.random() - 0.5) * 0.4, 0.12, 0],
                    color=BLACK,
                    fill_opacity=1,
                )
                .scale(random.random() * 1.2)
                .move_to(square)
                .shift(
                    [
                        random.random() * 2,
                        1.5 * (random.random() * 2 - 1),
                        0,
                    ]
                )
                for i in range(40)
            ]
        ).rotate(
            angle_between_vectors(square.get_corner(UR), RIGHT),
            about_point=square.get_center(),
        )
        self.add(particles)
        self.make_rigid_body(particles)
        for i in particles:
            i.body.apply_impulse_at_local_point((0, 0.01), (1, 0))
            i.body.velocity = (
                (random.random() - 1) * 40,
                (random.random() - 0.5) * 20,
            )
        self.play(ChangeSpeed(Wait(), {0: 2, 0.2: 0.05, 0.4: 0.05, 0.5: 1}))

        self.wait(3)
        banner = (
            ManimBanner(False)
            .scale(0.5)
            .move_to(self.camera.frame.get_center() + 4 * LEFT)
            .shift(UP * 0.5)
        )
        l = (
            Text("<github.com/sparshg>", font=FONT, color="#a6a6a6")
            .next_to(banner, DOWN, 1.5)
            .scale(0.5)
        )
        self.play(
            banner.create(), self.camera.frame.animate.shift(LEFT * 4), FadeOut(grid)
        )
        self.play(banner.expand(), Write(l))
        self.wait()
        self.play(Unwrite(banner), Unwrite(l))


class Poly(Polygon):
    def __init__(self, *vertices, **kwargs):
        if len(vertices) == 0:
            vertices = [[-0.2, -0.12, 0], [0.2, -0.12, 0], [0, 0.12, 0]]
        super().__init__(*vertices, **kwargs)
