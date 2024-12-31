from manim import *

class IntroductionScene(Scene):
    def construct(self):
        title = Text("Introduction to Manim", font_size=48)
        subtitle = Text("Creating Educational Animations", font_size=32)
        author = Text("By: Your Name", font_size=24)

        title.to_edge(UP)
        subtitle.next_to(title, DOWN, buff=0.5)
        author.to_edge(DOWN)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(author, shift=UP), run_time=1)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(author), run_time=1)


class BinarySearchIntro(Scene):
    def construct(self):
        # Main text
        main_text = Text("Welcome to Binary Search", font_size=48).to_edge(UP)
        subtitle = Text("A powerful algorithm for searching sorted arrays", font_size=24).next_to(main_text, DOWN)

        # Animations
        self.play(Write(main_text))
        self.play(FadeIn(subtitle))
        self.wait(3)
        self.play(FadeOut(main_text), FadeOut(subtitle))
        self.wait(1)


class BinarySearchScene(Scene):
    def construct(self):
        title = Text("What is Binary Search?", font_size=48).center()
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        array = [3, 7, 10, 15, 19, 23, 27]
        array_mob = VGroup(*[Text(str(num), font_size=32) for num in array]).arrange(RIGHT, buff=1.0)
        self.play(Write(array_mob))
        self.wait(2)

        self.play(array_mob.animate.set_color(YELLOW))
        low_arrow = Arrow(start=UP, end=DOWN, color=BLUE).next_to(array_mob[0], DOWN)
        high_arrow = Arrow(start=UP, end=DOWN, color=RED).next_to(array_mob[-1], DOWN)
        self.play(Create(low_arrow), Create(high_arrow))
        mid_index = 3
        mid_arrow = Arrow(start=UP, end=DOWN, color=GREEN).next_to(array_mob[mid_index], DOWN)
        self.play(Create(mid_arrow))
        self.play(array_mob[mid_index].animate.set_color(GREEN))
        mid_text = Text(f"Value at mid = {array[mid_index]}", font_size=24).next_to(array_mob, DOWN)
        self.play(Write(mid_text))
        self.wait(1)
        left_half = array_mob[:mid_index]
        self.play(FadeOut(left_half), FadeOut(mid_text))
        self.play(low_arrow.animate.next_to(array_mob[mid_index + 1], DOWN))
        self.wait(2)

        new_array = array_mob[mid_index + 1:]
        self.play(new_array.animate.set_color(YELLOW))
        self.play(high_arrow.animate.next_to(new_array[-1], DOWN))
        mid_index_new = 1
        mid_arrow_new = Arrow(start=UP, end=DOWN, color=GREEN).next_to(new_array[mid_index_new], DOWN)
        self.play(Create(mid_arrow_new))
        self.play(new_array[mid_index_new].animate.set_color(GREEN))
        mid_text_new = Text(f"Value at mid = {array[mid_index + 1 + mid_index_new]}", font_size=24).next_to(new_array, DOWN)
        self.play(Write(mid_text_new))
        self.wait(1)
        right_half = new_array[mid_index_new + 1:]
        self.play(FadeOut(right_half), FadeOut(mid_text_new))
        self.play(high_arrow.animate.next_to(new_array[mid_index_new], DOWN))
        self.wait(2)

        final_value = new_array[mid_index_new]
        self.play(final_value.animate.set_color(YELLOW))
        self.play(low_arrow.animate.next_to(final_value, DOWN), high_arrow.animate.next_to(final_value, DOWN))
        mid_arrow_final = Arrow(start=UP, end=DOWN, color=GREEN).next_to(final_value, DOWN)
        self.play(Create(mid_arrow_final))
        self.play(final_value.animate.set_color(GREEN))
        final_text = Text(f"Value at mid = {array[mid_index + 1 + mid_index_new]}. Target found!", font_size=24).next_to(final_value, DOWN)
        self.play(Write(final_text))
        self.wait(2)


class PythonCodeImplementation(Scene):
    def construct(self):
        # Title Animation
        title = Text("Python Code Implementation", font_size=48).move_to(ORIGIN)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Code Display
        code = '''def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1'''
        code_lines = code.split('\n')
        code_mob = VGroup(*[Text(line, font="Monospace", font_size=24) for line in code_lines]).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)

        self.play(Write(code_mob[0]))
        self.wait(0.5)
        self.play(Write(code_mob[1]))
        self.wait(0.5)
        self.play(Write(code_mob[2]))
        self.wait(0.5)
        self.play(Write(code_mob[3]))
        self.wait(0.5)
        self.play(Write(code_mob[4]))
        self.wait(0.5)
        self.play(Write(code_mob[5]))
        self.wait(0.5)
        self.play(Write(code_mob[6]))
        self.wait(0.5)
        self.play(Write(code_mob[7]))
        self.wait(0.5)
        self.play(Write(code_mob[8]))
        self.wait(0.5)
        self.play(Write(code_mob[9]))
        self.wait(0.5)

        # Highlight Key Sections
        while_loop = code_mob[2]
        if_condition = code_mob[4]
        return_statement = code_mob[5]

        self.play(Indicate(while_loop))
        self.wait(1)
        self.play(Indicate(if_condition))
        self.wait(1)
        self.play(Indicate(return_statement))
        self.wait(1)

        # Fade Out Code
        self.play(FadeOut(code_mob))

        # Time and Space Complexity
        complexity = Text("Time Complexity: O(log n)\nSpace Complexity: O(1)", font_size=32).move_to(ORIGIN)
        self.play(Write(complexity))
        self.wait(2)
        self.play(FadeOut(complexity))


class ComplexityAnalysis(Scene):
    def construct(self):
        title = Text("Complexity Analysis", font_size=72).center()
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        time_complexity = Text("Time Complexity: O(log n)", font_size=48).center().shift(UP * 0.5)
        space_complexity = Text("Space Complexity: O(1)", font_size=48).center().shift(DOWN * 0.5)
        self.play(FadeIn(time_complexity), FadeIn(space_complexity))
        self.wait(12)
        self.play(FadeOut(time_complexity), FadeOut(space_complexity))

        main_text = Text("Binary Search is simple yet elegant.", font_size=48).center()
        subtitle = Text("Use it to save time and resources!", font_size=32).next_to(main_text, DOWN)
        self.play(Write(main_text), FadeIn(subtitle))
        self.wait(7)
        self.play(FadeOut(main_text), FadeOut(subtitle))