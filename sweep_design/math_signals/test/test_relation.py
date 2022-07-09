import unittest

import numpy as np
from scipy.integrate import cumulative_trapezoid
from numpy.testing import assert_array_equal

from ..math_relation import Relation
from ..defaults.base_structures import BaseXY


def pre_integr(x, y):
    return BaseXY(x=x[1:], y=np.ones(x[1:].size))


class PreTestRelation:

    # @staticmethod
    # def pre_test_input(test_case: unittest.TestCase, relation_class: Relation):

    #     input_data = [([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]),
    #         (np.array([1, 2, 3, 4, 5]), np.array([10, 20, 30, 40, 50])),
    #         (np.array([1, 2, 3, 4, 5]), [10, 20, 30, 40, 50]),
    #         ([1, 2, 3, 4, 5], np.array([10, 20, 30, 40, 50]))
    #                   ]
    #     for k in input_data:
    #         with test_case.subTest(k=k):
    #             r = relation_class(*k)  # type: Relation
    #             result_x, result_y = r.get_data()
    #             assert_array_equal(result_x, np.array(k[0]))
    #             assert_array_equal(result_y, np.array(k[1]))

    #     input_data_2 = [[[1, 2, 3, 4, 5], [10, 20, 30, 40, 50]],
    #                     ([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]),
    #                     {'x': [1, 2, 3, 4, 5], 'y':[10, 20, 30, 40, 50]}]

    #     for k in input_data_2:
    #         with test_case.subTest(k=k):
    #             r = relation_class(k)  # type: Relation
    #             result_x, result_y = r.get_data()
    #             if isinstance(k, dict):
    #                 k = list(k.values())
    #             assert_array_equal(result_x, np.array(k[0]))
    #             assert_array_equal(result_y, np.array(k[1]))

    @staticmethod
    def pre_test_input(test_case: unittest.TestCase, relation_class: Relation):

        input_data = [
            ([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]),
            (np.array([1, 2, 3, 4, 5]), np.array([10, 20, 30, 40, 50])),
            (np.array([1, 2, 3, 4, 5]), [10, 20, 30, 40, 50]),
            ([1, 2, 3, 4, 5], np.array([10, 20, 30, 40, 50])),
        ]
        for k in input_data:
            with test_case.subTest(k=k):
                r = relation_class(*k)  # type: Relation
                result_x, result_y = r.get_data()
                assert_array_equal(result_x, np.array(k[0]))
                assert_array_equal(result_y, np.array(k[1]))

    @staticmethod
    def pre_test_math(test_case: unittest.TestCase, relation_class: Relation):

        x = np.array([1, 2, 3, 4, 5], dtype="float")
        y1 = np.array([10, 20, 30, 40, 50], dtype="float")

        y2 = np.array([2, 4, 6, 8, 10], dtype="float")

        r1 = relation_class(x, y1)  # type: Relation
        r2 = relation_class(x, y2)  # type: Relation
        operation = ["__add__", "__sub__", "__mul__", "__truediv__", "__pow__"]

        for m in operation:
            for k in [(r2, y2), (2, 2)]:
                with test_case.subTest(k=k, m=m):
                    math_check(r1, k[0], x, y1, k[1], m)

    @staticmethod
    def pre_test_integrate_diff(test_case: unittest.TestCase, relation_class: Relation):

        x = np.array([1, 2, 3, 4, 5, 6])
        y = np.array([10, 20, 30, 40, 50, 60])

        r = relation_class(x, y)  # type: Relation
        dr = r.diff()
        dx, dy = dr.get_data()
        assert_array_equal(dx, x[:-1] + (r.dx) / 2)
        assert_array_equal(dy, np.diff(y))

        d2r = r.diff().diff()
        d2x, d2y = d2r.get_data()
        assert_array_equal(d2x, x[:-2] + r.dx)
        assert_array_equal(d2y, np.diff(np.diff(y)))

        ir = r.integrate()
        ix, iy = ir.get_data()
        assert_array_equal(ix, x[1:])
        assert_array_equal(iy, cumulative_trapezoid(y))

        i2r = r.integrate().integrate()
        i2x, i2y = i2r.get_data()
        assert_array_equal(x[2:], i2x)
        assert_array_equal(i2y, cumulative_trapezoid(cumulative_trapezoid(y)))

        same_r = r.integrate().integrate().diff().diff()
        same_x, same_y = same_r.get_data()
        assert_array_equal(same_x, x[3:-1])
        assert_array_equal(same_y, y[3:-1])

        same_r2 = r.integrate().diff().integrate().diff()
        same_x2, same_y2 = same_r2.get_data()
        assert_array_equal(same_x2, x[3:-1])
        assert_array_equal(same_y2, y[3:-1])

    @staticmethod
    def pre_test_interpolate_extrapolate(
        test_case: unittest.TestCase, relation_class: Relation
    ):
        x = [1, 2, 3, 4, 5]
        y = [10, 20, 30, 40, 50]
        r = relation_class(x, y)  # type: Relation
        new_x = [1.1, 2.1, 3.1, 4.1, 5.1]
        new_r = r.interpolate_extrapolate(new_x)
        new_x2, new_y = new_r.get_data()
        assert_array_equal(new_x, new_x2)
        assert_array_equal(new_y, np.array([11.0, 21.0, 31.0, 41.0, 0.0]))

    @staticmethod
    def pre_test_convolve_correlate(
        test_case: unittest.TestCase, r1, r2, relation_class: Relation
    ):

        rconv = relation_class.convolve(r1, r2)
        test_case.assertIsInstance(rconv, relation_class)

        rcorr = relation_class.correlate(r1, r2)
        test_case.assertIsInstance(rcorr, relation_class)

    # @staticmethod
    # def pre_test_names(test_case: unittest.TestCase, relation_class: Relation, default_name: str):
    #     r = relation_class([0, 1, 2], [0, 1, 2])  # type: Relation
    #     test_case.assertEqual(r.get_name(), '{0}{1}'.format(default_name, r._quantity-1))
    #     name = 'test'
    #     r2 = relation_class([0, 1, 2], [1, 2, 3], name)  # type: Relation
    #     test_case.assertEqual(r2.get_name(), name)


class TestRelation(unittest.TestCase):
    pre_cases = PreTestRelation

    def test_input(self):
        self.pre_cases.pre_test_input(self, Relation)

    def test_math(self):
        self.pre_cases.pre_test_math(self, Relation)

    def test_integrate_diff(self):
        self.pre_cases.pre_test_integrate_diff(self, Relation)

    def test_interpolate_extrapolate(self):
        self.pre_cases.pre_test_interpolate_extrapolate(self, Relation)

    def test_conv_corr(self):
        r1 = Relation([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        r2 = Relation([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        self.pre_cases.pre_test_convolve_correlate(self, r1, r2, Relation)


def math_check(r1, ry, x, y1, y, operation):
    r = r1.__getattribute__(operation)(ry)  # type: Relation
    if operation != "__pow__":
        y = y1.__getattribute__(operation)(y)
    else:
        if isinstance(y1, np.ndarray):
            y = np.abs(y1).__getattribute__(operation)(y) * np.sign(y1)
        else:
            y = y1.__getattribute__(operation)(y)
    result_x, result_y = r.get_data()
    assert_array_equal(result_x, x)
    assert_array_equal(result_y, y)
