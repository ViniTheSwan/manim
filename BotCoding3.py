from manimlib import *

import numpy as np
from decimal import Decimal, getcontext, ROUND_DOWN
WAIT_TIME = 1

def round_down(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor



class StepSizeSell(Scene):
    def construct(self):

        quantity = np.random.uniform(0,1)
        quantity_mobj = TexText( str(quantity) )# quantity of the coin
        stepSize = 0.00100000
        minQty =   0.00100000
        # The following rule comes from the binace rest API github page. We will link the page down in the description
        #eq1 = TexText(r"\textrm{(quantity - minQty)\:{}\:\%\:{ }stepSize == 0}")
        eq1 = TexText(r"$(quantity - minQty) \bmod{} stepSize == 0$")
        #self.play(Write(eq1))
        self.play(ShowCreation(eq1))
        self.wait(WAIT_TIME)
        self.play(FadeOut(eq1))
        ##############################
        print(RoundedRectangle.CONFIG.keys())
        binance_name = TexText(r"binance", color = BLUE).shift(1.9*UP)
        binance = VGroup(
            RoundedRectangle(corner_radius = 0.3, height = 6, width = 8),
            binance_name
                         )
        binance.shift(3*RIGHT)
        quantity_mobj.shift(4*LEFT)
        user_name = TexText(r"user", color = BLUE)
        user_name.shift(4*LEFT).shift(1.9*UP)
        ######################################
        self.play(FadeIn(binance), FadeIn(user_name))
        self.play(FadeIn(quantity_mobj))


        self.play(quantity_mobj.shift,7*RIGHT)
        quantity_rounded = round_down(quantity, 9)
        quantity_rounded_mobj = TexText(str(quantity_rounded)).shift(3*RIGHT)
        quantity_rounded_mobj.shift(0.835*LEFT)

        self.wait(WAIT_TIME)
        self.remove(quantity_mobj)
        self.add(quantity_rounded_mobj)
        self.wait(WAIT_TIME)

        # minus minQTY
        getcontext().prec = 9
        eq2 = TexText(fr"${quantity_rounded}-0.00100000$")
        eq2.shift(3.6*RIGHT)
        self.remove(quantity_rounded_mobj)
        self.add(eq2)
        #self.play(ReplacementTransform(quantity_rounded_mobj, eq2))
        self.wait(WAIT_TIME)


        # show result from minus min QTY
        result = quantity_rounded - minQty
        result_mobj = TexText(str(round_down(result, 9)))
        result_mobj.shift(1.1* RIGHT)
        self.play(ReplacementTransform(eq2, result_mobj))
        self.wait(WAIT_TIME)

        # modulo
        #self.play(Transform(quantity_mobj, quantity_rounded_mobj))
        eq3 = TexText(fr"$ \mod 0.00100000 $")
        eq3.shift(4.2*RIGHT)
        self.play(FadeIn(eq3))
        self.wait(WAIT_TIME)

        # result from modulo
        result_mod = result % stepSize
        result_mod_mobj = TexText(str(round_down(result_mod, 9)))
        result_mod_mobj.shift(3.3 * RIGHT)

        self.play(ReplacementTransform(result_mobj, result_mod_mobj),ReplacementTransform(eq3, result_mod_mobj) )
        self.wait(WAIT_TIME)


        # unequal to zero
        eq4 = TexText(r"$ \neq 0 $", color = RED)
        eq4.shift(2.9*RIGHT)
        eq4.shift(0.7*DOWN)
        self.play(FadeIn(eq4))
        self.wait(WAIT_TIME)

        # return LOT_SIZE ERROR
        self.play(FadeOut(eq4), FadeOut(result_mod_mobj))
        Error = Text(r"LOT_SIZE ERROR", color = RED).scale(0.5).shift(3*RIGHT)
        self.play(FadeIn(Error))
        self.play(Error.shift, 7*LEFT)
        self.play(FadeOut(Error), FadeOut(binance), FadeOut(user_name))


class Solution(Scene):
    def construct(self):
        ######################### OUR SOLUTION #########################
        self.play(ShowCreationThenFadeOut(Text("Our Solution", font="Helvetica")))

        # quantity = stepSize * Decimal(math.floor(Decimal(quantity) / stepSize))
        quantity = np.random.uniform(0, 1)
        quantity_mobj = TexText(str(quantity))  # quantity of the coin
        stepSize = 0.00200000
        minQty = 0.00100000


        binance_name = TexText(r"binance", color=BLUE).shift(1.9 * UP)
        binance = VGroup(
            RoundedRectangle(corner_radius=0.3, height=6, width=8),
            binance_name
        )
        binance.shift(3 * RIGHT)
        quantity_mobj.shift(4 * LEFT)
        user_name = TexText(r"user", color=BLUE)
        user_name.shift(4 * LEFT).shift(1.9 * UP)
        ######################################
        self.play(FadeIn(binance), FadeIn(user_name))
        self.play(FadeIn(quantity_mobj))
        self.wait(WAIT_TIME)
        self.play(
            # Set the size with the width of a object
            self.camera.frame.set_width,17,

        )
        eq5 = TexText(fr"Decimal({quantity})").shift(4.3*LEFT)
        self.play(FadeOut(quantity_mobj))
        self.play(ShowCreation(eq5))
        self.wait(WAIT_TIME)


        getcontext().prec = 9
        getcontext().rounding = ROUND_DOWN
        quantity_decimal = Decimal(str(quantity))
        print(quantity_decimal)
        quantity_decimal_mobj = TexText(str(quantity_decimal)).shift(4*LEFT)
        self.play(ReplacementTransform(eq5,quantity_decimal_mobj))
        self.wait(WAIT_TIME)

        self.play(FadeOut(quantity_decimal_mobj))
        stepSize = Decimal(str(0.00100000))
        eq6 = TexText(fr"{quantity_decimal} / stepSize").shift(4.5*LEFT)
        self.play(ShowCreation(eq6))
        self.wait(WAIT_TIME)

        eq7 = TexText(fr"{quantity_decimal} / {stepSize}").shift(4.5*LEFT)
        self.play(ReplacementTransform(eq6, eq7))
        self.wait(WAIT_TIME)

        step2 = quantity_decimal/stepSize
        step2_mobj = TexText(str(step2)).shift(4.5*LEFT)
        self.play(ReplacementTransform(eq7, step2_mobj))
        self.wait(WAIT_TIME)

        eq8 = TexText(fr"math.floor({step2})").shift(4*LEFT)
        self.play(FadeOut(step2_mobj))
        self.play(ShowCreation(eq8))
        self.wait(WAIT_TIME)

        step3 = math.floor(step2)
        step3_mobj = TexText(str(step3)).shift(4*LEFT)
        #self.play(FadeOut())
        #self.play(ShowCreation(step3_mobj))
        self.play(ReplacementTransform(eq8, step3_mobj))
        self.wait(WAIT_TIME)

        eq9 = TexText(fr"Decimal({step3})").shift(4*LEFT)
        self.play(FadeOut(step3_mobj))
        self.play(Write(eq9))
        self.wait(WAIT_TIME)

        step4 =Decimal(step3)
        step4_mobj = TexText(fr"{step4}").shift(4*LEFT)
        self.play(ReplacementTransform(eq9, step4_mobj))
        self.wait(WAIT_TIME)

        eq10 = TexText(fr"$stepSize \cdot {step4}$").shift(4*LEFT)
        self.play(FadeOut(step4_mobj))
        self.play(Write(eq10))
        self.wait(WAIT_TIME)

        eq102 = TexText(fr"${stepSize} \cdot {step4}$").shift(4*LEFT)
        self.play(Transform(eq10, eq102), )
        self.wait(WAIT_TIME)

        step5 = stepSize * step4
        step5_mobj = TexText(str(step5)).shift(4*LEFT)
        self.play(ReplacementTransform(eq10, step5_mobj))
        self.wait(WAIT_TIME)

        self.play(step5_mobj.shift, 7*RIGHT)
        self.wait(WAIT_TIME)

        eq11 = TexText(fr" - minQty").shift(4.7*RIGHT)
        self.play(Write(eq11))

        eq12 = TexText(fr" - {minQty}").shift(4.45*RIGHT)
        self.play(ReplacementTransform(eq11 , eq12))

        # show result from minus min QTY
        step6 = step5 - Decimal(str(minQty))
        result_mobj = TexText(str(round_down(step6, 9)))
        result_mobj.shift(1.1 * RIGHT)
        self.play(ReplacementTransform(eq12, result_mobj),ReplacementTransform(step5_mobj, result_mobj))
        self.wait(WAIT_TIME)

        # modulo
        # self.play(Transform(quantity_mobj, quantity_rounded_mobj))
        eq13 = TexText(fr"$ \mod 0.00100000 $")
        eq13.shift(3.5 * RIGHT)
        self.play(FadeIn(eq13))
        self.wait(WAIT_TIME)

        # result from modulo
        step7 = step6 % stepSize
        result_mod_mobj = TexText(str(round_down(step7, 9)), color = GREEN)
        result_mod_mobj.shift(3.3 * RIGHT)

        self.play(ReplacementTransform(result_mobj, result_mod_mobj), ReplacementTransform(eq13, result_mod_mobj))
        self.wait(WAIT_TIME)

        self.play(FadeOut(result_mod_mobj))
        text = Text(fr"SUCESSFUL ORDER", color= GREEN).shift(3.3*RIGHT).scale(0.5)
        self.play(ShowCreation(text))
        self.play(text.shift, 7.3*LEFT)
        self.wait(WAIT_TIME)
        self.play(FadeOutToPoint(VGroup(text, user_name, binance), LEFT_SIDE))

class All(Scene):
    def construct(self):
        quantity = np.random.uniform(0, 1)
        quantity_mobj = TexText(str(quantity))  # quantity of the coin
        stepSize = 0.00100000
        minQty = 0.00100000
        # The following rule comes from the binace rest API github page. We will link the page down in the description
        # eq1 = TexText(r"\textrm{(quantity - minQty)\:{}\:\%\:{ }stepSize == 0}")
        eq1 = TexText(r"$(quantity - minQty) \bmod{} stepSize == 0$")
        # self.play(Write(eq1))
        self.play(ShowCreation(eq1))
        self.wait(WAIT_TIME)
        self.play(FadeOut(eq1))
        ##############################
        print(RoundedRectangle.CONFIG.keys())
        binance_name = TexText(r"binance", color=BLUE).shift(1.9 * UP)
        binance = VGroup(
            RoundedRectangle(corner_radius=0.3, height=6, width=8),
            binance_name
        )
        binance.shift(3 * RIGHT)
        quantity_mobj.shift(4 * LEFT)
        user_name = TexText(r"user", color=BLUE)
        user_name.shift(4 * LEFT).shift(1.9 * UP)
        ######################################
        self.play(FadeIn(binance), FadeIn(user_name))
        self.play(FadeIn(quantity_mobj))

        self.play(quantity_mobj.shift, 7 * RIGHT)
        quantity_rounded = round_down(quantity, 9)
        quantity_rounded_mobj = TexText(str(quantity_rounded)).shift(3 * RIGHT)
        quantity_rounded_mobj.shift(0.835 * LEFT)

        self.wait(WAIT_TIME)
        self.remove(quantity_mobj)
        self.add(quantity_rounded_mobj)
        self.wait(WAIT_TIME)

        # minus minQTY
        getcontext().prec = 9
        eq2 = TexText(fr"${quantity_rounded}-0.00100000$")
        eq2.shift(3.6 * RIGHT)
        self.remove(quantity_rounded_mobj)
        self.add(eq2)
        # self.play(ReplacementTransform(quantity_rounded_mobj, eq2))
        self.wait(WAIT_TIME)

        # show result from minus min QTY
        result = quantity_rounded - minQty
        result_mobj = TexText(str(round_down(result, 9)))
        result_mobj.shift(1.1 * RIGHT)
        self.play(ReplacementTransform(eq2, result_mobj))
        self.wait(WAIT_TIME)

        # modulo
        # self.play(Transform(quantity_mobj, quantity_rounded_mobj))
        eq3 = TexText(fr"$ \mod 0.00100000 $")
        eq3.shift(4.2 * RIGHT)
        self.play(FadeIn(eq3))
        self.wait(WAIT_TIME)

        # result from modulo
        result_mod = result % stepSize
        result_mod_mobj = TexText(str(round_down(result_mod, 9)))
        result_mod_mobj.shift(3.3 * RIGHT)

        self.play(ReplacementTransform(result_mobj, result_mod_mobj), ReplacementTransform(eq3, result_mod_mobj))
        self.wait(WAIT_TIME)

        # unequal to zero
        eq4 = TexText(r"$ \neq 0 $", color=RED)
        eq4.shift(2.9 * RIGHT)
        eq4.shift(0.7 * DOWN)
        self.play(FadeIn(eq4))
        self.wait(WAIT_TIME)

        # return LOT_SIZE ERROR
        self.play(FadeOut(eq4), FadeOut(result_mod_mobj))
        Error = Text(r"LOT_SIZE ERROR", color=RED).scale(0.5).shift(3 * RIGHT)
        self.play(FadeIn(Error))
        self.play(Error.shift, 7 * LEFT)
        self.play(FadeOut(Error), FadeOut(binance), FadeOut(user_name))
        #######################################333
        ######################### OUR SOLUTION #########################
        self.play(ShowCreationThenFadeOut(Text("Our Solution", font="Helvetica")))

        # quantity = stepSize * Decimal(math.floor(Decimal(quantity) / stepSize))
        quantity = np.random.uniform(0, 1)
        quantity_mobj = TexText(str(quantity))  # quantity of the coin
        stepSize = 0.00200000
        minQty = 0.00100000

        binance_name = TexText(r"binance", color=BLUE).shift(1.9 * UP)
        binance = VGroup(
            RoundedRectangle(corner_radius=0.3, height=6, width=8),
            binance_name
        )
        binance.shift(3 * RIGHT)
        quantity_mobj.shift(4 * LEFT)
        user_name = TexText(r"user", color=BLUE)
        user_name.shift(4 * LEFT).shift(1.9 * UP)
        ######################################
        self.play(FadeIn(binance), FadeIn(user_name))
        self.play(FadeIn(quantity_mobj))
        self.wait(WAIT_TIME)
        self.play(
            # Set the size with the width of a object
            self.camera.frame.set_width, 17,

        )
        eq5 = TexText(fr"Decimal({quantity})").shift(4.3 * LEFT)
        self.play(FadeOut(quantity_mobj))
        self.play(ShowCreation(eq5))
        self.wait(WAIT_TIME)

        getcontext().prec = 9
        getcontext().rounding = ROUND_DOWN
        quantity_decimal = Decimal(str(quantity))
        print(quantity_decimal)
        quantity_decimal_mobj = TexText(str(quantity_decimal)).shift(4 * LEFT)
        self.play(ReplacementTransform(eq5, quantity_decimal_mobj))
        self.wait(WAIT_TIME)

        self.play(FadeOut(quantity_decimal_mobj))
        stepSize = Decimal(str(0.00100000))
        eq6 = TexText(fr"{quantity_decimal} / stepSize").shift(4.5 * LEFT)
        self.play(ShowCreation(eq6))
        self.wait(WAIT_TIME)

        eq7 = TexText(fr"{quantity_decimal} / {stepSize}").shift(4.5 * LEFT)
        self.play(ReplacementTransform(eq6, eq7))
        self.wait(WAIT_TIME)

        step2 = quantity_decimal / stepSize
        step2_mobj = TexText(str(step2)).shift(4.5 * LEFT)
        self.play(ReplacementTransform(eq7, step2_mobj))
        self.wait(WAIT_TIME)

        eq8 = TexText(fr"math.floor({step2})").shift(4 * LEFT)
        self.play(FadeOut(step2_mobj))
        self.play(ShowCreation(eq8))
        self.wait(WAIT_TIME)

        step3 = math.floor(step2)
        step3_mobj = TexText(str(step3)).shift(4 * LEFT)
        # self.play(FadeOut())
        # self.play(ShowCreation(step3_mobj))
        self.play(ReplacementTransform(eq8, step3_mobj))
        self.wait(WAIT_TIME)

        eq9 = TexText(fr"Decimal({step3})").shift(4 * LEFT)
        self.play(FadeOut(step3_mobj))
        self.play(Write(eq9))
        self.wait(WAIT_TIME)

        step4 = Decimal(step3)
        step4_mobj = TexText(fr"{step4}").shift(4 * LEFT)
        self.play(ReplacementTransform(eq9, step4_mobj))
        self.wait(WAIT_TIME)

        eq10 = TexText(fr"$stepSize \cdot {step4}$").shift(4 * LEFT)
        self.play(FadeOut(step4_mobj))
        self.play(Write(eq10))
        self.wait(WAIT_TIME)

        eq102 = TexText(fr"${stepSize} \cdot {step4}$").shift(4 * LEFT)
        self.play(Transform(eq10, eq102), )
        self.wait(WAIT_TIME)

        step5 = stepSize * step4
        step5_mobj = TexText(str(step5)).shift(4 * LEFT)
        self.play(ReplacementTransform(eq10, step5_mobj))
        self.wait(WAIT_TIME)

        self.play(step5_mobj.shift, 7 * RIGHT)
        self.wait(WAIT_TIME)

        eq11 = TexText(fr" - minQty").shift(4.7 * RIGHT)
        self.play(Write(eq11))

        eq12 = TexText(fr" - {minQty}").shift(4.45 * RIGHT)
        self.play(ReplacementTransform(eq11, eq12))

        # show result from minus min QTY
        step6 = step5 - Decimal(str(minQty))
        result_mobj = TexText(str(round_down(step6, 9)))
        result_mobj.shift(1.1 * RIGHT)
        self.play(ReplacementTransform(eq12, result_mobj), ReplacementTransform(step5_mobj, result_mobj))
        self.wait(WAIT_TIME)

        # modulo
        # self.play(Transform(quantity_mobj, quantity_rounded_mobj))
        eq13 = TexText(fr"$ \mod 0.00100000 $")
        eq13.shift(3.5 * RIGHT)
        self.play(FadeIn(eq13))
        self.wait(WAIT_TIME)

        # result from modulo
        step7 = step6 % stepSize
        result_mod_mobj = TexText(str(round_down(step7, 9)), color=GREEN)
        result_mod_mobj.shift(3.3 * RIGHT)

        self.play(ReplacementTransform(result_mobj, result_mod_mobj), ReplacementTransform(eq13, result_mod_mobj))
        self.wait(WAIT_TIME)

        self.play(FadeOut(result_mod_mobj))
        text = Text(fr"SUCESSFUL ORDER", color=GREEN).shift(3.3 * RIGHT).scale(0.5)
        self.play(ShowCreation(text))
        self.play(text.shift, 7.3 * LEFT)
        self.wait(WAIT_TIME)
        self.play(FadeOutToPoint(VGroup(text, user_name, binance), LEFT_SIDE))

class StepSizeBuy(Scene):
    def construct(self):
        pass

