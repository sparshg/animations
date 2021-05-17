from manim import *

from manim._config.utils import ManimConfig

ManimConfig.background_color = "#ece6e2"
radius = 2
ground_len = 5
FONT = "product sans"
BLACK = "#343434"
WHITE = "#ece6e2"
SPEED = 25


def time_adj(k):
    return 1 + 1 / k


def speed_adj(k):
    return (k - 1) / (k + 1)


def get_slow_mo(k):  # |k| > 1
    return lambda t: (t / k) * (k + 1 - t)


class Test(MovingCameraScene):
    def construct(self):
        wheel = SVGMobject("assets/wheel.svg").scale(1.25).shift(1.22 * DOWN)
        wheel.speed = SPEED

        ground = VGroup(
            # Dashed lines
            DashedLine(
                start=ground_len * LEFT,
                end=(ground_len + 12) * RIGHT,
                positive_space_ratio=0.4,
                dash_length=0.2,
                color=BLACK,
            ).shift(2.5 * DOWN)
        )
        [i.rotate(PI / 4) for i in ground[0].submobjects]
        ground.add(
            # Add simple line for ground
            Line(ground_len * LEFT, ground_len * RIGHT, color=BLACK).align_to(
                ground, UP, DOWN
            ),
            # Mask for left side
            Rectangle(
                fill_opacity=1,
                color=WHITE,
                height=0.2,
                width=config.frame_x_radius - ground_len,
            )
            .move_to(ground, aligned_edge=UP)
            .to_edge(LEFT, 0),
            # Mask for right side
            Rectangle(
                fill_opacity=1,
                color=WHITE,
                height=0.2,
                width=config.frame_x_radius - ground_len,
            )
            .move_to(ground, aligned_edge=UP)
            .to_edge(RIGHT, 0),
        )
        head = VGroup(
            Text(
                "Translational",
                font=FONT,
                color=BLACK,
            ),
            Text(
                "Motion",
                font=FONT,
                color=BLACK,
            ),
        )
        head1 = VGroup(
            Text(
                "Rotational",
                font=FONT,
                color=BLACK,
            ),
            Text(
                "Motion",
                font=FONT,
                color=BLACK,
            ),
        )
        head2 = VGroup(
            Text(
                "Rolling",
                font=FONT,
                color=BLACK,
            ),
            Text(
                "Motion",
                font=FONT,
                color=BLACK,
            ),
        )
        [i.arrange().scale(1.2).shift(3 * UP) for i in [head, head1, head2]]
        head2[0].shift(0.1 * DOWN)

        self.play(
            AnimationGroup(FadeIn(ground), Write(wheel), run_time=2, lag_ratio=0.5)
        )
        self.wait(0.5)
        self.play(AnimationGroup(Write(head), ShiftWiggle(wheel), lag_ratio=0.5))
        self.play(
            wheel.animate.shift(4 * LEFT),
            ground[0].animate.shift(4 * LEFT),
        )

        # Start slow-mo
        d = 3
        k = 1.01
        self.play(
            wheel.animate.shift(d * RIGHT),
            self.camera.frame.animate.scale(0.8).shift(DOWN),
            rate_func=get_slow_mo(k),
            run_time=d * time_adj(k) / wheel.speed,
        )
        wheel.speed *= speed_adj(k)
        # End slow-mo

        v = VGroup(
            Vector(RIGHT / 2),
            Vector(RIGHT / 2).shift(DR * 0.7),
            Vector(RIGHT / 2).shift(DL * 0.75),
            Vector(RIGHT / 2).shift(UL * 0.75),
            Vector(RIGHT / 2).shift(UR * 0.75),
            Vector(RIGHT / 2).shift(LEFT),
            Vector(RIGHT / 2).shift(RIGHT),
            Vector(RIGHT / 2).shift(DOWN * 1.1),
            Vector(RIGHT / 2).shift(UP * 1.1),
        ).set_color(RED)
        v[0].set_color(BLUE_D)
        v.add_updater(
            lambda v: v.move_to(wheel.get_center()).shift(
                v.get_center() - v[0].get_start()
            )
        )
        Vcom = MathTex("V_{Center\ of\ mass}", color=BLACK).shift(0.4 * UP)
        wheel.add_updater(lambda m, dt: m.shift(RIGHT * m.speed * dt))
        self.play(Create(v))
        self.wait()
        self.play(
            Succession(
                Write(Vcom),
                Wait(),
                Transform(Vcom, MathTex("V_{c}", color=BLACK).move_to(Vcom)),
            ),
        )
        self.wait(3)
        wheel.clear_updaters()

        # Reverse start slow-mo
        d = 4
        k *= -1
        self.play(
            wheel.animate.shift(d * RIGHT),
            FadeOut(v),
            FadeOut(Vcom),
            self.camera.frame.animate.shift(UP).scale(1.25),
            rate_func=get_slow_mo(k),
            run_time=d * time_adj(k) / wheel.speed,
        )
        wheel.speed *= speed_adj(k)
        # Reverse end slow-mo

        self.wait()
        self.play(
            wheel.animate.shift(wheel.get_center()[0] * LEFT),
            ground[0].animate.shift(wheel.get_center()[0] * LEFT),
        )
        self.play(Transform(head, head1))
        self.play(Rotate(wheel, TAU - PI / 4))
        self.wait(0.5)

        wheel.speed = SPEED
        wheel.w = wheel.speed / 1.2

        # Start slow-mo
        d = PI / 1.7
        k = 1.05
        self.play(
            Rotate(wheel, -d),
            self.camera.frame.animate.scale(0.8).shift(DOWN),
            rate_func=get_slow_mo(k),
            run_time=d * time_adj(k) / wheel.w,
        )
        wheel.w *= speed_adj(k)
        # End slow-mo
        wheel.add_updater(lambda m, dt: m.rotate(-m.w * dt))

        v = VGroup(
            Dot(fill_opacity=0),
            *[
                Dot(color=WHITE)
                .shift(RIGHT / (i % 2 + 1) * 1.04)
                .rotate_about_origin(PI / 3 * i)
                for i in range(6)
            ],
            *[
                DashedLine(
                    ORIGIN,
                    RIGHT / (i % 2 + 1) * 1.04,
                    positive_space_ratio=0.3,
                    color=WHITE,
                ).rotate_about_origin(PI / 3 * i)
                for i in range(6)
            ],
            *[
                Vector(RIGHT / (i % 2 + 1), color=RED)
                .shift(RIGHT / (i % 2 + 1) * 1.04)
                .rotate(-PI / 2, about_point=(RIGHT / (i % 2 + 1) * 1.04))
                .rotate_about_origin(PI / 3 * i)
                for i in range(6)
            ],
        ).move_to(wheel.get_center())
        v.shift(v.get_center() - v[0].get_center())
        v.add_updater(
            lambda m, dt: m.rotate(-wheel.w * dt, about_point=wheel.get_center())
        )
        omega = MathTex(r"\omega", font=FONT, color=BLACK).shift(0.4 * UP)
        self.play(Create(v))
        self.play(Write(omega))

        self.wait(5)
        wheel.clear_updaters()

        # Reverse start slow-mo
        d = TAU * 0.75
        k *= -1
        self.play(Uncreate(v), Unwrite(omega), run_time=0.2)
        self.play(
            Rotating(wheel, OUT, -d),
            self.camera.frame.animate.shift(UP).scale(1.25),
            rate_func=get_slow_mo(k),
            run_time=d * time_adj(k) / wheel.w,
        )
        wheel.w *= speed_adj(k)
        # Reverse end slow-mo

        self.wait(0.5)

        h1 = (
            VGroup(
                Text(
                    "Translational + Rotational \n when",
                    color=BLACK,
                    line_spacing=0.8,
                ),
                Text(
                    "V꜀=Rω",
                    color=BLACK,
                ).shift(0.5 * DOWN),
            )
            .scale(0.6)
            .shift(2 * UP)
        )
        self.play(LaggedStart(Transform(head, head2), Write(h1), lag_ratio=0.4))
        self.wait()

        self.play(
            wheel.animate.shift(4 * LEFT),
            ground[0].animate.shift(4 * LEFT),
        )
        self.wait()
        wheel.speed = SPEED
        wheel.w = wheel.speed / 1.2

        # Start slow-mo
        d = 3.8
        k = 1.005
        self.play(
            RotatingAndShifting(wheel, d * RIGHT, -d / 1.2),
            self.camera.frame.animate.scale(0.7).shift(1.5 * DOWN),
            rate_func=get_slow_mo(k),
            run_time=d * time_adj(k) / wheel.speed,
        )
        wheel.speed *= speed_adj(k)
        wheel.w *= speed_adj(k)
        # End slow-mo
        self.remove(h1[0])
        h1[1].scale(1.4).shift(0.3 * UP)

        v = VGroup(
            Vector(RIGHT / 2, color=BLUE_D),
            *[
                Vector(RIGHT / 2, color=BLUE_D)
                .shift(RIGHT * 1.06)
                .rotate_about_origin(-PI / 2 * i + PI / 1.8)
                for i in [0, 1, 2, 2.5]
            ],
            *[
                Vector(RIGHT / 2, color=RED)
                .shift(RIGHT * 1.06)
                .rotate(-PI / 2, about_point=(RIGHT * 1.06))
                .rotate_about_origin(-PI / 2 * i + PI / 1.8)
                for i in [0, 1, 2, 2.5]
            ],
            Dot(color=WHITE).set_z_index(2),
            *[
                Dot(color=WHITE)
                .set_z_index(2)
                .shift(RIGHT * 1.06)
                .rotate_about_origin(-PI / 2 * i + PI / 1.8)
                for i in [0, 1, 2, 2.5]
            ],
        )
        wheel.add_updater(lambda m, dt: m.shift(RIGHT * m.speed * dt).rotate(-m.w * dt))
        v.add_updater(
            lambda v, dt: v.move_to(wheel.get_center())
            .shift(v.get_center() - v[9].get_center())
            .rotate(-wheel.w * dt, about_point=v[9].get_center())
        )

        for i in v[:5]:
            i.add_updater(lambda m: m.set_angle(0))

        self.play(Create(v), run_time=0.5)
        self.wait(3)
        v.clear_updaters()
        wheel.clear_updaters()
        t1 = Text("Point at rest", font=FONT, color=BLACK).scale(0.5).shift(3 * DOWN)
        t2 = (
            MathTex("V_{c}", color=BLACK)
            .scale(0.6)
            .shift(3.05 * DOWN)
            .set_stroke(width=1)
        )
        t3 = (
            MathTex("V_{c}", "-", "R\omega", color=BLACK)
            .scale(0.6)
            .shift(3.05 * DOWN)
            .set_stroke(width=1)
        )
        t4 = (
            MathTex("V_{c}", "-", "R\omega", "=", "0", color=BLACK)
            .scale(0.6)
            .shift(3.05 * DOWN)
            .set_stroke(width=1)
        )
        t5 = (
            MathTex("V_{c}", "=", "R\omega", color=BLACK)
            .scale(0.6)
            .shift(3.05 * DOWN)
            .set_stroke(width=1)
        )

        vv1 = v[-2].copy()
        self.play(LaggedStart(Write(t1), Indicate(vv1), lag_ratio=0.5))
        self.remove(vv1)
        self.play(t1.animate.shift(2 * LEFT), run_time=0.5)
        vv2 = v[3].copy().set_color(YELLOW)
        self.play(LaggedStart(Write(t2), Wiggle(vv2), lag_ratio=0.5))
        self.remove(vv2)
        vv3 = v[7].copy().set_color(YELLOW)
        self.play(LaggedStart(TransformMatchingTex(t2, t3), Wiggle(vv3), lag_ratio=0.5))
        self.remove(vv3)
        self.wait(0.5)
        self.play(TransformMatchingTex(t3, t4))
        self.wait(0.5)
        self.play(FadeOut(t1), Transform(t4, t5))
        self.wait(2)
        vv5 = v[5].copy()
        vv2 = v[2].copy()
        vv6 = v[6].copy()
        fv26 = Vector(DR / 2, color=YELLOW_E)
        fv26.shift(v[-3].get_center() - fv26.get_start())
        vv4 = v[4].copy()
        vv8 = v[8].copy()
        fv48 = Vector(RIGHT * 0.293 / 2.2 + UP * 0.707 / 2.2, color=YELLOW_E)
        fv48.shift(v[-1].get_center() - fv48.get_start())
        self.remove(v[2], v[6], v[4], v[8])
        self.play(
            Uncreate(v[3]),
            Uncreate(v[7]),
            Uncreate(v[1]),
            Uncreate(v[5]),
            Transform(vv2, fv26),
            Transform(vv6, fv26),
            Transform(vv4, fv48),
            Transform(vv8, fv48),
            vv5.animate.scale(
                2, scale_tips=True, about_point=v[5].get_start()
            ).set_color(YELLOW_E),
        )

        self.wait(3)

        # Reverse start slow-mo
        d = TAU * 0.75
        k *= -1
        self.play(
            FadeOut(vv5),
            FadeOut(vv2),
            FadeOut(vv4),
            FadeOut(v[0]),
            FadeOut(vv6),
            FadeOut(vv8),
            FadeOut(t4),
            # run_time=0.4,
            RotatingAndShifting(wheel, d * RIGHT, -d / 1.2),
            self.camera.frame.animate.shift(UP).scale(1.428),
            rate_func=get_slow_mo(k),
            run_time=d * time_adj(k) / wheel.speed,
        )
        self.remove(v)
        wheel.speed *= speed_adj(k)
        wheel.w *= speed_adj(k)
        # Reverse end slow-mo
        self.wait()
        banner = ManimBanner(dark_theme=False).move_to(8 * DOWN).scale(0.6)
        l = (
            Text("<github.com/sparshg>", font=FONT, color="#a6a6a6")
            .next_to(banner, DOWN, 1.5)
            .scale(0.5)
        )
        self.wait()
        self.play(
            LaggedStart(
                self.camera.frame.animate.shift(8 * DOWN),
                banner.create(),
                Write(l),
                lag_ratio=0.2,
            )
        )
        self.play(banner.expand())
        self.wait()
        self.play(Unwrite(banner), Unwrite(l))


class RotatingAndShifting(Rotating):
    def __init__(self, mobject, shift, radians, **kwargs):
        self.shift = shift
        self.radians = radians
        super().__init__(mobject, OUT, radians, **kwargs)

    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate(alpha * self.radians).shift(alpha * self.shift)


class ShiftWiggle(Wiggle):
    def __init__(
        self,
        mobject,
        amp: float = 0.4,
        direction: np.ndarray = RIGHT,
        n_wiggles: int = 6,
        run_time: float = 2,
        **kwargs
    ):
        self.amp = amp
        self.direction = direction
        self.n_wiggles = n_wiggles
        super().__init__(mobject, 1, 0, run_time=run_time, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        submobject.points[:, :] = starting_submobject.points
        submobject.shift(wiggle(alpha, self.n_wiggles) * self.amp * self.direction)
