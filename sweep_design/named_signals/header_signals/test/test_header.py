import unittest

import numpy as np

from ..defaults import names as dn
from ..relation_header import HeaderRelation
from ....math_signals.defaults.base_structures import MathOperation


class TestHeaderRelation(unittest.TestCase):
    """Test headers."""

    def check_equal(self, r_named: HeaderRelation, name, category):
        self.assertEqual(str(r_named), name)
        self.assertEqual(r_named.category, category)

    def setUp(self) -> None:
        self.name = "test_name"
        self.category = "test_category"
        self.nr = HeaderRelation(self.name, self.category)
        self.dname = "R_1"
        self.dcategory = "relation"
        self.dnr = HeaderRelation()

    def tearDown(self) -> None:
        HeaderRelation._quantity = 1

    def test_init(self):

        self.check_equal(self.nr, self.name, self.category)

    def test_select_data(self):

        x_start = 0
        x_end = 1

        nr = self.nr.select_data(x_start, x_end)
        self.check_equal(
            nr,
            dn.make_default_name_select_data(self.nr, x_start, x_end),
            self.dcategory,
        )

        nr2 = self.nr.select_data(x_start, x_end, self.name, self.category)
        self.check_equal(nr2, self.name, self.category)

    def test_exp(self):
        nr = self.nr.exp()
        self.check_equal(nr, dn.make_default_name_exp(self.nr), self.nr.category)

        nr2 = self.nr.exp(self.name, self.category)
        self.check_equal(nr2, self.name, self.category)

    def test_diff(self):
        nr = self.nr.diff()
        self.check_equal(
            nr,
            dn.make_default_diff_name(self.nr),
            dn.make_diff_category_name(self.nr.category),
        )

        nr2 = self.nr.exp(self.name, self.category)
        self.check_equal(nr2, self.name, self.category)

    def test_integrate(self):
        nr = self.nr.integrate()
        self.check_equal(
            nr,
            dn.make_default_integrate_name(self.nr),
            dn.make_integrate_category_name(self.nr.category),
        )

        nr2 = self.nr.diff(self.name, self.category)
        self.check_equal(nr2, self.name, self.category)

    def test_interpolate_extrapolate(self):
        new_x = np.array([0.0, 1.0])
        nr = self.nr.interpolate_extrapolate(new_x)
        self.check_equal(
            nr, dn.make_default_interpolate_name(self.nr, new_x), self.nr.category
        )

        nr2 = self.nr.interpolate_extrapolate(new_x, self.name, self.category)
        self.check_equal(nr2, self.name, self.category)

    def test_shift(self):
        x_shift = 10.0

        nr = self.nr.shift(x_shift)
        self.check_equal(
            nr, dn.make_default_shift_name(self.nr, x_shift), self.nr.category
        )

        nr2 = self.nr.shift(x_shift, self.name, self.category)
        self.check_equal(nr2, self.name, self.category)

    def test_operation(self):
        list_operation = [
            MathOperation.ADD,
            MathOperation.RADD,
            MathOperation.SUB,
            MathOperation.RSUB,
            MathOperation.MUL,
            MathOperation.RMUL,
            MathOperation.TRUEDIV,
            MathOperation.RTRUEDIV,
            MathOperation.POW,
            MathOperation.RPOW,
        ]
        for k in list_operation:
            for m in [1.0, self.nr]:
                with self.subTest(k=k, m=m):
                    result = getattr(self.nr, k.value)(m)
                    self.check_equal(
                        result,
                        dn.make_default_names_operations(self.nr, m, k),
                        self.nr.category,
                    )

    def test_equalize(self):
        new_x = np.array([0.0, 1.0])
        nr, nr2 = HeaderRelation.equalize(self.nr, self.nr, new_x)

        self.check_equal(
            nr, dn.make_default_interpolate_name(self.nr, new_x), self.nr.category
        )
        self.check_equal(
            nr2, dn.make_default_interpolate_name(self.nr, new_x), self.nr.category
        )

        nr3, nr4 = HeaderRelation.equalize(
            self.nr, self.nr, new_x, self.name, self.name, self.category, self.category
        )
        self.check_equal(nr3, self.name, self.category)
        self.check_equal(nr4, self.name, self.category)

    def test_correlate(self):
        nr = HeaderRelation.correlate(self.nr, self.nr)
        self.check_equal(
            nr, dn.make_default_name_correlation(self.nr, self.nr), self.nr.category
        )
        nr2 = HeaderRelation.correlate(self.nr, self.nr, self.name, self.category)
        self.check_equal(nr2, self.name, self.category)

    def test_correlate(self):
        nr = HeaderRelation.convolve(self.nr, self.nr)
        self.check_equal(
            nr, dn.make_default_name_convolution(self.nr, self.nr), self.nr.category
        )
        nr2 = HeaderRelation.convolve(self.nr, self.nr, self.name, self.category)
        self.check_equal(nr2, self.name, self.category)
