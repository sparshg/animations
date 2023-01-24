# This animation is for my asteroids training simulation
# https://github.com/sparshg/asteroids-genetic

from manim import *
import networkx as nx

from manim.mobject.graph import _determine_graph_layout
from manim.opengl import *


brain = [
    [
        -0.009693078,
        0.09939107,
        -0.9073774,
        -0.57600784,
        -0.28215104,
        -1.1938038,
        0.7848887,
        -0.36527398,
        -0.09820301,
        0.35657594,
        0.79946166,
        -0.49511307,
        0.6358272,
        -0.22616765,
        -0.047070365,
        -0.2757149,
        -0.40778914,
        -0.63695973,
        0.57385933,
        -0.8935812,
        -0.09729913,
        0.22516525,
        0.7222565,
        -0.0970098,
        0.68187845,
        0.2298346,
        0.85350573,
        -0.6128707,
        -0.3337645,
        0.036359284,
    ],
    [
        1.282332,
        0.47750735,
        -0.6479809,
        -0.82879424,
        -0.31277427,
        0.33294052,
        0.76130587,
        -0.059874874,
        0.09245835,
        0.010224363,
        0.15314236,
        -0.54873085,
        -0.53317577,
        0.92193705,
        -0.257631,
        -0.0625739,
        0.67577976,
        -0.246336,
        -0.015977442,
        -1.3203895,
        -0.12709938,
        -1.6439004,
        -0.7283819,
        -0.6083856,
        -0.19187418,
        0.33709872,
        -0.17897944,
        -0.47784263,
        -0.06966477,
        -0.56339085,
        -0.56758046,
        0.89432144,
        -0.2775634,
        0.59100586,
        0.43255445,
        -0.036131572,
    ],
    [
        -0.32144403,
        0.14525081,
        -0.7295116,
        -0.11274259,
        1.1643897,
        -0.45038012,
        -0.09214835,
        0.413071,
        -0.68017447,
        1.1750991,
        -1.153951,
        -0.48123106,
        -0.8972865,
        0.3888719,
        0.2741283,
        -0.7187085,
        0.4451282,
        -1.533827,
        -0.016380731,
        1.1047536,
        1.0084127,
        1.501503,
        0.85071784,
        0.52249545,
    ],
]


class CursorText(VGroup):
    def update(m, dt, text, text_obj):
        length = len(text.submobjects)
        target = m.get_center()
        for i in range(length):
            if text.submobjects[length - i - 1].get_fill_opacity() == 1:
                initial = m.get_center()
                target = (
                    m.align_to(text.submobjects[length - i - 1], RIGHT)
                    .shift(
                        RIGHT * (-0.2 if text_obj.erase else 0.25 if i != 0 else 0.1)
                    )
                    .get_center()
                )
                m.move_to(initial)
                break
            elif i == length - 1:
                initial = m.get_center()
                target = m.align_to(text.submobjects[0], LEFT).get_center()
                m.move_to(initial)
        if np.linalg.norm(target - m.get_center()) < 0.1:
            if text_obj.cursor_rising:
                m.set_opacity(m.stroke_opacity + (1.1 - m.stroke_opacity) * 4 * dt)
                if m.stroke_opacity >= 1:
                    text_obj.cursor_rising = False
            else:
                m.set_opacity(m.stroke_opacity + (-0.1 - m.stroke_opacity) * 4 * dt)
                if m.stroke_opacity <= 0:
                    text_obj.cursor_rising = True
        else:
            text_obj.show_cursor()
        m.shift((target - m.get_center()) * 18 * dt)

    def __init__(self, scene, text, font_size=24, sc=1, *args, **kwargs):
        self.text = (
            Text(
                text,
                font_size=font_size,
                font="monocraft",
                color="#DDDDDD",
                *args,
                **kwargs,
            )
            .set_opacity(0)
            .scale(sc)
        )
        self.erase = False
        self.sc = sc
        self.scene = scene
        self.cursor_rising = False
        self.reveal_speed = 30
        self.unreveal_speed = 50
        self.reveal_time = len(text) / self.reveal_speed
        self.unreveal_time = len(text) / self.unreveal_speed
        self.cursor = Line(UP * 0.25, DOWN * 0.25, color="#DDDDDD", stroke_width=6)
        super().__init__(self.text, self.cursor)

    def drop_cursor(self):
        self.cursor.clear_updaters().add_updater(
            lambda m, dt: CursorText.update(m, dt, self.text, self), index=0
        )
        self.scene.play(Create(self.cursor), run_time=0.4)
        self.show_cursor()
        return self

    def show_cursor(self):
        self.cursor.set_opacity(1)
        self.cursor_rising = False

    def reveal(self, wait=1, added_anims=[]):
        self.erase = False
        self.scene.play(
            AddTextLetterByLetter(self.text, run_time=self.reveal_time), *added_anims
        )
        if wait > 0:
            self.scene.wait(wait)
        return self

    def unreveal(self, added_anims=[], hide_cursor=False):
        self.erase = True
        self.scene.play(
            RemoveTextLetterByLetter(self.text),
            run_time=self.unreveal_time,
            *added_anims,
        )
        if hide_cursor:
            self.cursor.clear_updaters()
            self.scene.play(FadeOut(self.cursor), run_time=0.4)
        return self

    def rev_unrev(self, wait_rev, added_anims=[], hide_cursor=False):
        self.reveal(wait_rev, added_anims)
        self.unreveal(hide_cursor=hide_cursor)
        return self

    def switch_text(self, text, font_size=24, wait=0.4, *args, **kwargs):
        self.text = (
            Text(
                text,
                font_size=font_size,
                font=self.text.font,
                color="#DDDDDD",
                *args,
                **kwargs,
            )
            .set_opacity(0)
            .scale(self.sc)
            .move_to(self.text)
        )
        self.reveal_time = len(text) / self.reveal_speed
        self.unreveal_time = len(text) / self.unreveal_speed
        self.scene.wait(wait)
        return self


class NeuralNetwork(Graph):
    def __init__(
        self,
        *layers,
        sx=1,
        sy=1,
        edge_stroke=1.5,
        radius=0.3,
        stroke_width=2,
        randomize=False,
        **kwargs
    ):
        self.sx = sx
        self.sy = sy
        self.layers = layers
        self.edge_stroke = edge_stroke
        self.randomize = randomize
        self.v, self.p, self.e, self.partitions = self.get_positioning(*layers)

        vertex_config = {
            "radius": radius,
            "fill_color": BLACK,
            "stroke_width": stroke_width,
        }

        super().__init__(
            self.v,
            self.e,
            layout={v: p for v, p in zip(self.v, self.p)},
            vertex_config=vertex_config,
            edge_config=self.edge_config,
            **kwargs,
        )
        self.flip(RIGHT)

    def get_positioning(self, *layers):
        edges = []
        partitions = []
        self.edge_config = {}
        c = 0

        for i in layers:
            partitions.append(list(range(c + 1, c + i + 1)))
            c += i
        for i, v in enumerate(layers[:-1]):
            last = sum(layers[: i + 1])
            l = 0
            for j in range(v):
                for k in range(layers[i + 1]):
                    edges.append((j + last - layers[i] + 1, k + last + 1))
                    r = (
                        random.random() * 2 - 1
                        if self.randomize
                        else np.clip(brain[i][l], -1, 1)
                    )
                    l += 1
                    ec = {
                        "stroke_width": self.edge_stroke,
                        "stroke_color": PURE_RED if r < 0 else WHITE,
                        "stroke_opacity": abs(r),
                    }
                    self.edge_config[(j + last - layers[i] + 1, k + last + 1)] = ec

        vertices = np.arange(1, sum(layers) + 1)

        nx_graph = nx.Graph()
        nx_graph.add_nodes_from(vertices)
        nx_graph.add_edges_from(edges)
        positions = np.dot(
            np.array(
                list(
                    _determine_graph_layout(
                        nx_graph,
                        layout="partite",
                        partitions=partitions,
                        layout_scale=3,
                        root_vertex=None,
                    ).values()
                )
            ),
            np.array([[self.sx, 0, 0], [0, self.sy, 0], [0, 0, 1]]),
        )
        return vertices, positions, edges, partitions


class OpenGLScene(ThreeDScene):
    def construct(self):
        img = OpenGLImageMobject(
            "out.png", height=self.camera.height, width=self.camera.width
        )
        self.add(img)
        self.move_camera(
            phi=PI * 0.6,
            theta=-PI * 0.3,
            zoom=0.8,
            frame_center=OUT * 7 + UP + LEFT * 2,
        )


n = NeuralNetwork(
    5,
    6,
    6,
    4,
    sx=1.29,
    sy=0.435,
    radius=0.088,
    stroke_width=1.5,
).shift(1.86 * DOWN + 4.01 * RIGHT)


class AlphaScene(Scene):
    def construct(self):
        img = ImageMobject("out.png").scale_to_fit_height(self.camera.frame_height)
        self.play(Write(n))
        for _ in range(4):
            self.play(
                LaggedStart(
                    *(
                        ShowPassingFlash(i.copy().set_stroke(width=3), time_width=0.8)
                        for i in list(n.edges.values())
                    ),
                    lag_ratio=0.022,
                )
            )
        self.play(n.animate.scale(1.5).move_to(ORIGIN), run_time=1)


class NeuralScene(MovingCameraScene):
    def construct(self):
        ship = (
            VGroup(
                Polygram([[0, 2, 0], [-1, -1, 0], [1, -1, 0]], color=WHITE),
                Line([-1, -1, 0], [-1.2667, -1.8, 0]),
                Line([1, -1, 0], [1.2667, -1.8, 0]),
            )
            .scale(0.2)
            .set_stroke(WHITE, 1.7)
            .shift(RIGHT * 10)
            .rotate(-PI / 1.7)
        )
        bullet = (
            Dot(radius=0.03)
            .set_opacity(0.7)
            .move_to(ship[0].get_center_of_mass() + RIGHT)
            .rotate(-PI / 1.7, about_point=ship.get_center_of_mass())
            .shift(4 * RIGHT)
        )
        asteroid = (
            RegularPolygon(7, color=WHITE, stroke_width=1, radius=0.8)
            .rotate(PI * 0.2)
            .move_to(ship)
            .shift(RIGHT * 1.5 + DOWN * 2)
        )
        asteroid2 = (
            RegularPolygon(5, color=WHITE, stroke_width=1, radius=0.5)
            .rotate(PI * 0.3)
            .move_to(ship)
            .shift(RIGHT * 4 + UP * 1.5)
        )
        asteroid3 = (
            RegularPolygon(3, color=WHITE, stroke_width=1, radius=0.4)
            .rotate(PI * 0.4)
            .move_to(ship)
            .shift(RIGHT + UP * 2)
        )

        self.add(n.scale(1.5).move_to(ORIGIN))
        in_arrows = VGroup(
            *(
                Arrow(ORIGIN, RIGHT * 0.9)
                .set_opacity(0.7)
                .move_to(x.get_center() + LEFT * 0.5)
                for x in list(n.vertices.values())[:5]
            )
        )
        out_arrows = VGroup(
            *(
                Arrow(ORIGIN, RIGHT * 0.9)
                .set_opacity(0.7)
                .move_to(x.get_center() + RIGHT * 0.5)
                for x in list(n.vertices.values())[17:]
            )
        )
        title = Text(
            "Neural Networks", font="monocraft", font_size=36, color="#DDDDDD"
        ).shift(UP * 3.2)
        text = (
            CursorText(self, "This is called a neural network")
            .move_to(self.camera.frame_center)
            .shift(DOWN * 3.5)
        )

        self.play(AddTextLetterByLetter(title), rate_func=rush_from)
        self.wait()
        text.drop_cursor()
        text.rev_unrev(3)
        text.switch_text("It's just a complex mathematical function")
        text.rev_unrev(3)
        text.switch_text("It takes some game information as inputs...")
        text.rev_unrev(3.5, [FadeIn(in_arrows, shift=RIGHT, lag_ratio=0.1)])
        text.switch_text("...and outputs tell what actions to take")
        text.rev_unrev(4, [FadeIn(out_arrows, shift=RIGHT, lag_ratio=0.1)], True)

        world = VGroup(ship, asteroid, asteroid2, asteroid3, bullet)
        self.play(
            self.camera.frame.animate.shift(2.5 * RIGHT + DOWN).scale(1.2),
            world.animate.shift(LEFT * 4),
            FadeOut(title, shift=UP),
        )

        direc = ship[0].get_center_of_mass() - asteroid.get_center()
        distance = DashedLine(
            ship[0].get_center_of_mass(),
            asteroid.get_center() + direc / np.linalg.norm(direc) * 0.8,
        ).set_stroke(RED, 2)
        heading = DashedLine(
            ship[0].get_center_of_mass(),
            ship[0].get_center_of_mass()
            + (ship[0].get_vertices()[0] - ship[0].get_center_of_mass()) * 5,
        ).set_stroke(GREEN, 2)

        theta = Angle(heading, distance, radius=0.5, other_angle=True)
        theta.points = np.concatenate(
            [
                theta.points,
                [ship[0].get_center_of_mass()],
                theta.points[0].reshape(1, 3),
            ]
        )
        theta.set_points_as_corners(theta.points).set_fill(BLUE).set_stroke(
            BLUE, width=0
        ).set_opacity(0.5)

        right = (
            DashedLine(ORIGIN, RIGHT * 2)
            .set_stroke(BLUE, 2)
            .shift(ship[0].get_center_of_mass())
        )
        phi = Angle(heading, right, radius=0.5, other_angle=False)
        phi.points = np.concatenate(
            [
                phi.points,
                [ship[0].get_center_of_mass()],
                phi.points[0].reshape(1, 3),
            ]
        )
        phi.set_points_as_corners(phi.points).set_fill(YELLOW).set_stroke(
            YELLOW, width=0
        ).set_opacity(0.5)

        text = (
            CursorText(self, "This network takes 5 inputs", sc=1.2)
            .move_to(self.camera.frame_center)
            .shift(DOWN * 4)
        )
        text.drop_cursor()
        text.rev_unrev(2.5)

        label = (
            MathTex(r"\ell")
            .move_to(distance)
            .shift(UP * 0.15 + RIGHT * 0.15)
            .set_color(RED)
            .scale(0.7)
        )
        text.switch_text("The distance to the nearest asteroid...")
        text.reveal(1.5, [Write(distance)])
        self.play(
            Write(label),
            Transform(
                in_arrows[0],
                MathTex(r"\ell").set_opacity(0.7).move_to(in_arrows[0]).scale(0.9),
            ),
        )
        self.wait(3.5)
        text.unreveal([Unwrite(label)])

        text.switch_text("...the angle to this asteroid")
        text.reveal(1.5, [LaggedStart(Write(heading), Write(theta), lag_ratio=0.5)])
        label = (
            MathTex(r"\theta")
            .move_to(theta)
            .shift(DOWN * 0.2 + RIGHT * 0.35)
            .set_color(BLUE)
            .scale(0.7)
        )
        self.play(
            Write(label),
            Transform(
                in_arrows[1],
                MathTex(r"\theta").set_opacity(0.7).move_to(in_arrows[1]).scale(0.9),
            ),
        )
        self.wait(3.5)
        text.unreveal(
            (
                Unwrite(distance),
                Unwrite(theta),
                Unwrite(label),
            ),
        )
        text.switch_text("...angle of the ship itself")
        text.reveal(1.5, [LaggedStart(Write(right), Write(phi), lag_ratio=0.5)])

        label = (
            MathTex(r"\phi")
            .move_to(theta)
            .shift(RIGHT * 0.6)
            .set_color(YELLOW)
            .scale(0.6)
        )
        self.play(
            Write(label),
            Transform(
                in_arrows[4],
                MathTex(r"\phi").set_opacity(0.7).move_to(in_arrows[4]).scale(0.9),
            ),
        )
        self.wait(3.5)
        text.unreveal(
            (
                Unwrite(heading),
                Unwrite(right),
                Unwrite(phi),
                Unwrite(label),
            ),
        )
        v1 = Arrow(
            ship[0].get_center_of_mass(),
            ship[0].get_center_of_mass()
            + (heading.get_end() - heading.get_start()) * 0.5,
            buff=0,
            max_stroke_width_to_length_ratio=2,
            max_tip_length_to_length_ratio=0.2,
            color="#FF2222",
        )
        v2 = Arrow(
            asteroid.get_center(),
            asteroid.get_center() + UP,
            buff=0,
            max_stroke_width_to_length_ratio=2,
            max_tip_length_to_length_ratio=0.2,
            color="#FF2222",
        )
        label1 = (
            MathTex(r"\overrightarrow{v_1}")
            .move_to(v1)
            .shift(UP * 0.3)
            .set_color("#FF2222")
            .scale(0.6)
        )
        label2 = (
            MathTex(r"\overrightarrow{v_2}")
            .move_to(v2)
            .shift(RIGHT * 0.3)
            .set_color("#FF2222")
            .scale(0.6)
        )

        text.switch_text("...and the relative velocity of the asteroid")
        text.reveal(1.5, [Write(v1), Write(v2)])
        self.play(
            Write(label1),
            Write(label2),
            Transform(
                in_arrows[2],
                MathTex(r"(\overrightarrow{v_2} - \overrightarrow{v_1})_x")
                .set_opacity(0.7)
                .move_to(in_arrows[2])
                .shift(LEFT * 0.5)
                .scale(0.6),
            ),
            Transform(
                in_arrows[3],
                MathTex(r"(\overrightarrow{v_2} - \overrightarrow{v_1})_y")
                .set_opacity(0.7)
                .move_to(in_arrows[3])
                .shift(LEFT * 0.5)
                .scale(0.6),
            ),
        )
        self.wait(3.5)

        text.unreveal(
            (
                Unwrite(v1),
                Unwrite(v2),
                Unwrite(label1),
                Unwrite(label2),
            ),
            hide_cursor=True,
        )

        self.play(
            self.camera.frame.animate.shift(2.5 * LEFT + UP).scale(1 / 1.2),
            world.animate.shift(RIGHT * 4),
            Transform(
                out_arrows[0],
                Text("RIGHT", font="monocraft", font_size=14)
                .set_opacity(0.7)
                .move_to(out_arrows[0])
                .align_to(out_arrows[0], LEFT),
            ),
            Transform(
                out_arrows[1],
                Text("LEFT", font="monocraft", font_size=14)
                .set_opacity(0.7)
                .move_to(out_arrows[1])
                .align_to(out_arrows[1], LEFT),
            ),
            Transform(
                out_arrows[2],
                Text("SHOOT", font="monocraft", font_size=14)
                .set_opacity(0.7)
                .move_to(out_arrows[2])
                .align_to(out_arrows[2], LEFT),
            ),
            Transform(
                out_arrows[3],
                Text("THROTTLE", font="monocraft", font_size=14)
                .set_opacity(0.7)
                .move_to(out_arrows[3])
                .align_to(out_arrows[3], LEFT),
            ),
        )

        weight_anim = LaggedStart(
            *(
                ShowPassingFlash(i.copy().set_stroke(width=4), time_width=0.5)
                for i in list(n.edges.values())
            ),
            lag_ratio=0.02,
        )
        text = (
            CursorText(self, "The connections between the nodes are called weights")
            .move_to(self.camera.frame_center)
            .shift(DOWN * 3.5)
        )
        text.drop_cursor()
        text.rev_unrev(3, [weight_anim])
        text.switch_text("These define the behaviour of our spaceship")
        text.rev_unrev(3, [weight_anim])
        text.switch_text("But how do we find the correct weights?")
        text.rev_unrev(3.5, hide_cursor=True)
        title = Text(
            "Genetic Algorithm", font="monocraft", font_size=36, color="#DDDDDD"
        ).shift(UP * 3.2)
        self.play(
            AddTextLetterByLetter(title, rate_func=rush_from),
            LaggedStart(
                Unwrite(in_arrows, reverse=False),
                Unwrite(out_arrows, reverse=False),
                lag_ratio=0.1,
            ),
        )
        self.wait()


class GeneticScene(Scene):
    def construct(self):
        title = Text(
            "Genetic Algorithm", font="monocraft", font_size=36, color="#DDDDDD"
        ).shift(UP * 3.2)

        n = (
            NeuralNetwork(
                5,
                6,
                6,
                4,
                sx=1.29,
                sy=0.435,
                radius=0.088,
                stroke_width=1.5,
            )
            .scale(1.5)
            .move_to(ORIGIN)
        )

        self.add(title, n)

        nn_grid = (
            VGroup(
                *(
                    NeuralNetwork(
                        5,
                        6,
                        6,
                        4,
                        sx=1.29,
                        sy=0.435,
                        radius=0.088,
                        randomize=False if i == 4 else True,
                    )
                    for i in range(9)
                )
            )
            .arrange_in_grid(3, 3)
            .scale(0.4)
            .set_stroke(width=0.8)
            .move_to(ORIGIN)
        )
        group = VGroup(*(n.copy().set_opacity(0.25) for _ in range(9)))
        text = (
            CursorText(self, "Instead of training a single ship...")
            .move_to(self.camera.frame_center)
            .shift(DOWN * 3.5)
        )
        text.drop_cursor()
        text.rev_unrev(3)
        text.switch_text("...we start with a population of many")
        self.remove(n)
        self.add(group)
        text.rev_unrev(3, [ReplacementTransform(group, nn_grid)])

        text.switch_text("After they all are dead, we rate them...").rev_unrev(3.5)
        copy0 = nn_grid[0].copy().set_z_index(2)
        copy4 = nn_grid[4].copy().set_z_index(2)
        for i in copy0.vertices.values():
            i.set_z_index(3)
        for i in copy4.vertices.values():
            i.set_z_index(3)
        sr = SurroundingRectangle(nn_grid, color=BLACK).set_opacity(0.5).set_z_index(1)
        text.switch_text("...then select two 'fitter' brains").rev_unrev(
            3.5,
            [FadeIn(sr), FadeIn(copy0), FadeIn(copy4)],
        )
        nn_grid2 = (
            VGroup(
                *(
                    NeuralNetwork(
                        5,
                        6,
                        6,
                        4,
                        sx=1.29,
                        sy=0.435,
                        radius=0.088,
                        randomize=False if i == 4 else True,
                    )
                    for i in range(9)
                )
            )
            .arrange_in_grid(3, 3)
            .scale(0.4)
            .set_stroke(width=0.8)
            .move_to(ORIGIN)
            .shift(RIGHT * 3.5)
        )
        text.switch_text("and merge their weights to create a better brain!")
        text.reveal(
            0,
            [
                nn_grid.animate.shift(LEFT * 3.5),
                sr.animate.shift(LEFT * 3.5),
                Transform(copy0, nn_grid2[0].copy(), rate_func=rush_from),
                Transform(
                    copy4, nn_grid2[0].copy().set_opacity(0), rate_func=rush_from
                ),
            ],
        )
        self.remove(copy4)
        nn_grid2[0].set_opacity(0)
        self.wait(4)
        text.unreveal()

        text.switch_text("Fill the next generation with new brains like this")
        text.reveal(
            3,
            [
                LaggedStart(*(FadeIn(x, shift=LEFT) for x in nn_grid2), lag_ratio=0.1),
            ],
        )
        nn_grid2[0].become(copy0)
        self.remove(copy0)
        text.unreveal()
        text.switch_text("...and repeat to see the population evolve!")
        text.reveal()
        for _ in range(4):
            self.play(
                nn_grid2.animate.shift(LEFT * 7),
                FadeOut(
                    nn_grid,
                    shift=LEFT * 7,
                ),
                FadeOut(
                    sr,
                    shift=LEFT * 7,
                ),
                run_time=0.8,
            )
            self.play(
                FadeIn(sr),
                LaggedStart(
                    *(FadeIn(x, shift=LEFT) for x in nn_grid.move_to(RIGHT * 3.5)),
                    lag_ratio=0.1,
                ),
                run_time=0.8,
            )
            nn_grid, nn_grid2 = nn_grid2, nn_grid
        text.unreveal()
        text.switch_text("Let's plug this back and see it in action!")
        text.reveal(
            0,
            [
                nn_grid2.animate.shift(LEFT * 3.5).scale(4 / 3),
                FadeOut(
                    nn_grid,
                    shift=LEFT * 3.5,
                ),
                FadeOut(
                    sr,
                    shift=LEFT * 3.5,
                ),
            ],
        )

        copy1 = nn_grid2[4].copy()
        nn_grid2[4].set_opacity(0)

        self.play(
            Transform(copy1, n),
            FadeOut(nn_grid2),
        )
        self.wait(3)
        text.unreveal([Unwrite(title, run_time=1.5)], True)


class ScriptScene(Scene):
    def construct(self):
        text = CursorText(self, "Hey There!").drop_cursor().rev_unrev(3)

        text.switch_text(
            "This is my interactive simulation to train your own AI to play asteroids!",
            18,
        ).rev_unrev(4, hide_cursor=True)
        self.wait()

        text = (
            CursorText(self, "The AI is pretty dumb right now...")
            .drop_cursor()
            .rev_unrev(4)
        )

        text.switch_text("It doesn't know what to do...").rev_unrev(2.5)
        text.switch_text("But how is it making these decisions?").rev_unrev(
            5, hide_cursor=True
        )
        self.wait(3)

        text = (
            CursorText(self, "This can be considered as the 'brain' of our AI")
            .drop_cursor()
            .rev_unrev(3)
        )
        text.switch_text("Let's pause & see how it works!").rev_unrev(
            3, hide_cursor=True
        )

        text = (
            CursorText(self, "Here we have a population of 100 ships")
            .drop_cursor()
            .rev_unrev(3)
        )
        text.switch_text("You can drag it to vary the population size").rev_unrev(
            3, hide_cursor=True
        )

        text = (
            CursorText(self, "Click on a ship to track it").drop_cursor().rev_unrev(5)
        )
        text.switch_text("Let's track the best one alive...").rev_unrev(4)
        text.switch_text("This is what the ship is currently looking at").rev_unrev(
            5, hide_cursor=True
        )

        text = (
            CursorText(self, "You can also change the number of layers...")
            .drop_cursor()
            .rev_unrev(9)
        )
        text.switch_text("...and other parameters of the neural network").rev_unrev(3)
        text.switch_text("Let's speedup the simulation").rev_unrev(3, hide_cursor=True)

        text = (
            CursorText(self, "Seems like it found a good strategy to survive")
            .drop_cursor()
            .rev_unrev(6)
        )
        text.switch_text("Asteroids are coded to aim towards the player").rev_unrev(3)
        text.switch_text("Remaining stationary seems to be the best").rev_unrev(3)
        text.switch_text(
            "You can save this model as a file and load it later",
        ).rev_unrev(3, hide_cursor=True)

        text = (
            CursorText(self, "...or track another ship and save that model")
            .drop_cursor()
            .rev_unrev(5)
        )
        text.switch_text("But let's train it further").rev_unrev(3, hide_cursor=True)

        text = (
            CursorText(self, "Changing the inputs or the asteroid behaviour...")
            .drop_cursor()
            .rev_unrev(3)
        )

        for _text in (
            "...can change the strategy the AI uses",
            "It also depends on the fitness function that rates the network",
            "You can modify the code and try out different things",
            "This is written in Rust without any ML libraries",
        ):
            text.switch_text(_text).rev_unrev(3)
        text.switch_text(
            "Source code and download link are in description..."
        ).rev_unrev(3, hide_cursor=True)

        text = (
            CursorText(self, "Thanks for watching!")
            .drop_cursor()
            .rev_unrev(5, hide_cursor=True)
        )

        footer = Text(
            "github.com/sparshg", font="SF Mono Powerline", font_size=32
        ).set_color("#333333")
        footer_sub = (
            Text("made with Manim", font="SF Mono Powerline", font_size=18)
            .set_color("#333333")
            .to_edge(DOWN, buff=0.1)
        )
        self.add(footer, footer_sub)
        self.wait(2)
        self.play(Unwrite(footer), Unwrite(footer_sub))
        self.wait()
