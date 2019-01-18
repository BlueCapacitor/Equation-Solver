'''
Created on Nov 16, 2018

@author: Gosha
'''
import unittest
from Main import *


class Test(unittest.TestCase):

    def test_tree_show(self):
        tree1 = tree(10.0)
        self.assertEqual(tree1.show(), "10.0")
        tree2 = tree('a')
        self.assertEqual(tree2.show(), "a")
        tree3 = tree('+', [tree1, tree2])
        self.assertEqual(tree3.show(), "+(10.0, a)")

    def test_number(self):
        for eq in ['0', '1', '1.0', '1.5']:
            self.assertEqual(parse(eq).show(), str(float(eq)))

    def test_implicit_negative_number(self):
        for n in ['-1', '-1.0', '-1.5', '- 1', '- 1.0', '- 1.5']:
            self.assertEqual(parse(n).show(), str(float(n)))
            eq = "1 + " + n
            self.assertEqual(parse(eq).show(), "+(1.0, " + str(float(n)) + ")")

    def test_implicit_decimal(self):
        self.assertEqual(parse(".5").show(), "0.5")
        self.assertEqual(parse(".0").show(), "0.0")

    def test_implicit_multiplication(self):
        self.assertEqual(parse("ab").show(), "*(a, b)")
        self.assertEqual(parse("2a").show(), "*(2.0, a)")
        self.assertNotEqual(parse("12").show(), "*(1.0, 2.0)")

        self.assertEqual(parse("-0").show(), "0.0")

    def test_oops(self):
        self.assertEqual(parse("0 = 1 + 2 - 3 * 4 / 5 ^ 6").show(), "=(0.0, -(+(1.0, 2.0), /(*(3.0, 4.0), ^(5.0, 6.0))))")


if __name__ == "__main__":
    unittest.main()
