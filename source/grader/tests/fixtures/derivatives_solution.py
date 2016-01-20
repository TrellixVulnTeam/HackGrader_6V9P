import sys


class Parser:
    def __init__(self, input_f):
        self.input_f = input_f
        self.expressions = self._get_expressions()
        self.powers = {}

    def _get_expressions(self):
        return [exp for exp in self.input_f.split("+")]

    def __get_power_for_expression(self, expr):
        temp = [x for x in expr.split("^")]
        return temp[1]

    def __get_coef_for_expression(self, expr):
        if expr == 'x':
            return '1'

        temp = [x for x in expr.split("x")]

        if temp[0] == '':
            return 1

        return temp[0]

    def add_power(self, power, expr):
        if power == 0:
            self.powers[0] = [expr]

        elif power not in self.powers:
            self.powers[power] = [self.__get_coef_for_expression(expr)]

        else:
            self.powers[power].append(self.__get_coef_for_expression(expr))

    def take_power_for_expression(self):
        for exp in self.expressions:
            if exp.endswith("x"):
                self.add_power(1, exp)

            elif "^" in exp:
                power = self.__get_power_for_expression(exp)
                self.add_power(int(power), exp)

            else:
                self.add_power(0, exp)

        return self.powers


class Derivate:

    def create_function(self, coef, var, power):
        if power == 0:
            return "{}".format(coef)
        elif power == 1:
            if coef == 1:
                return "{}".format(var)
            return "{}{}".format(coef, var)
        else:
            if coef == 1:
                return "{}^{}".format(var, power)
            return "{}{}^{}".format(coef, var, power)

    def create_derivates(self, coef, var, power):
        new_coef = int(coef) * power
        new_power = power - 1

        return self.create_function(new_coef, var, new_power)


class Polynomial:
    def __init__(self, parser, derivate):
        self.powers = parser.take_power_for_expression()
        self.derivate = derivate
        self.derivates = []
        self.polynomials = []

    def create_derivate(self):
        for power in self.powers:
            if power != 0:
                coef = sum([int(x) for x in self.powers[power]])
                derivate = self.derivate.create_derivates(coef, 'x', power)
                polynomial = self.derivate.create_function(coef, 'x', power)

            else:
                polynomial = self.powers[0][0]
                derivate = "0"

            self.polynomials.append(polynomial)
            self.derivates.append(derivate)

        self.derivates.reverse()
        self.polynomials.reverse()

    def build_derivate(self):
        if len(self.derivates) > 1 and "0" in self.derivates:
            self.derivates.remove("0")

        if len(self.derivates) == 1:
            return self.derivates[0]

        return " + ".join(self.derivates)

    def build_polynomial(self):
        if "0" in self.polynomials:
            self.polynomials.remove("0")

        if len(self.polynomials) == 1:
            return self.polynomials[0]

        return " + ".join(self.polynomials)


class CLI:
    def __init__(self, poly):
        self.poly = poly

    def start(self):
        self.poly.create_derivate()
        print("The derivative of f(x) = {} is:".format(
            self.poly.build_polynomial()))

        print("f'(x) = {}".format(self.poly.build_derivate()))


def main():
    function = sys.argv[1]
    p = Parser(function)
    d = Derivate()
    poly = Polynomial(p, d)

    interface = CLI(poly)
    interface.start()

if __name__ == '__main__':
    main()
