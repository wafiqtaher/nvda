#tests/unit/test_locationHelper.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

"""Unit tests for the locationHelper module.
"""

import unittest
from locationHelper import *
from ctypes.wintypes import RECT, POINT

class TestRectOperators(unittest.TestCase):

	def test_intersection(self):
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4).intersection(RectLTRB(left=3,top=3,right=5,bottom=5)), RectLTRB(left=3,top=3,right=4,bottom=4))
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4).intersection(RectLTRB(left=5,top=5,right=7,bottom=7)), RectLTRB(left=0,top=0,right=0,bottom=0))

	def test_superset(self):
		self.assertTrue(RectLTRB(left=2,top=2,right=6,bottom=6).isSuperset(RectLTRB(left=2,top=2,right=4,bottom=4)))
		self.assertTrue(RectLTRB(left=2,top=2,right=6,bottom=6).isSuperset(RectLTRB(left=2,top=2,right=6,bottom=6)))

	def test_subset(self):
		self.assertTrue(RectLTRB(left=2,top=2,right=4,bottom=4).isSubset(RectLTRB(left=2,top=2,right=6,bottom=6)))
		self.assertTrue(RectLTRB(left=2,top=2,right=6,bottom=6).isSubset(RectLTRB(left=2,top=2,right=6,bottom=6)))
		self.assertFalse(RectLTRB(left=2,top=2,right=6,bottom=6).isSubset(RectLTRB(left=2,top=2,right=4,bottom=4)))

	def test_in(self):
		self.assertIn(RectLTRB(left=2,top=2,right=4,bottom=4), RectLTRB(left=2,top=2,right=6,bottom=6))
		self.assertNotIn(RectLTRB(left=2,top=2,right=4,bottom=4), RectLTRB(left=2,top=2,right=4,bottom=4))
		self.assertIn(Point(x=2,y=2), RectLTRB(left=2,top=2,right=6,bottom=6))
		self.assertIn(Point(x=4,y=4), RectLTRB(left=2,top=2,right=6,bottom=6))
		self.assertNotIn(Point(x=2,y=6), RectLTRB(left=2,top=2,right=6,bottom=6))
		self.assertNotIn(Point(x=6,y=6), RectLTRB(left=2,top=2,right=6,bottom=6))

	def test_equal(self):
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4), RectLTRB(left=2,top=2,right=4,bottom=4))
		self.assertNotEqual(RectLTRB(left=2,top=2,right=4,bottom=4), RectLTRB(left=2,top=2,right=6,bottom=6))
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4), RectLTWH(left=2,top=2,width=2,height=2))
		self.assertNotEqual(RectLTRB(left=2,top=2,right=4,bottom=4), RectLTWH(left=2,top=2,width=4,height=4))

class TestRectUtilities(unittest.TestCase):

	def test_points(self):
		rect = RectLTRB(left=-5,top=-5,right=5,bottom=5)
		self.assertEqual(rect.center, Point(x=0,y=0))
		self.assertEqual(rect.topLeft, Point(x=-5,y=-5))
		self.assertEqual(rect.topRight, Point(x=5,y=-5))
		self.assertEqual(rect.bottomLeft, Point(x=-5,y=5))
		self.assertEqual(rect.bottomRight, Point(x=5,y=5))

class TestToRectLTRB(unittest.TestCase):

	def test_collection(self):
		rect=RectLTRB(left=10,top=15,right=500,bottom=1000)
		self.assertEqual(toRectLTRB(
			rect.topLeft, 
			rect.bottomRight, 
			rect.center, 
			Point(15,15),
			Point(20,20),
			Point(50,50),
			Point(400,400),
			POINT(15,15),
			POINT(20,20),
			POINT(50,50),
			POINT(400,400),
			RectLTRB(left=450,top=450,right=490,bottom=990),
			RECT(450,450,490,990)
		), rect)

	def test_integers(self):
		self.assertEqual(RectLTRB(left=10,top=10,right=20,bottom=20), toRectLTRB(10,10,20,20))

class TestToRectLTWH(unittest.TestCase):

	def test_collection(self):
		location=RectLTWH(left=10,top=15,width=500,height=1000)
		self.assertEqual(toRectLTWH(
			location.topLeft, 
			location.bottomRight, 
			location.center, 
			Point(15,15),
			Point(20,20),
			Point(50,50),
			Point(400,400),
			POINT(15,15),
			POINT(20,20),
			POINT(50,50),
			POINT(400,400),
			RectLTRB(left=450,top=450,right=505,bottom=1010),
			RECT(450,450,490,990)
		), location)

	def test_integers(self):
		self.assertEqual(RectLTWH(left=10,top=10,width=20,height=20),toRectLTWH(10,10,20,20))

class TestPointOperators(unittest.TestCase):

	def test_add(self):
		self.assertEqual(Point(x=2,y=4)+Point(x=2,y=4),Point(x=4,y=8))

	def test_sum(self):
		point=Point(x=2,y=4)
		self.assertEqual(sum((point, point, point)), Point(x=6,y=12))

	def test_sub(self):
		self.assertEqual(Point(x=2,y=4)-Point(x=4,y=8),Point(x=-2,y=-4))

	def test_greaterThan(self):
		self.assertTrue(Point(x=3,y=4).yWiseGreaterThan(Point(x=4,y=3)))
		self.assertFalse(Point(x=3,y=4).xWiseGreaterThan(Point(x=4,y=3)))
		self.assertTrue(Point(x=4,y=3).xWiseGreaterThan(Point(x=3,y=4)))
		self.assertFalse(Point(x=4,y=3).yWiseGreaterThan(Point(x=3,y=4)))
		self.assertTrue(Point(x=3,y=4).yWiseGreaterOrEq(Point(x=4,y=3)))
		self.assertFalse(Point(x=3,y=4).xWiseGreaterOrEq(Point(x=4,y=3)))
		self.assertTrue(Point(x=4,y=3).xWiseGreaterOrEq(Point(x=3,y=4)))
		self.assertFalse(Point(x=4,y=3).yWiseGreaterOrEq(Point(x=3,y=4)))

	def test_lessThan(self):
		self.assertTrue(Point(x=4,y=3).yWiseLessThan(Point(x=3,y=4)))
		self.assertFalse(Point(x=4,y=3).xWiseLessThan(Point(x=3,y=4)))
		self.assertTrue(Point(x=3,y=4).xWiseLessThan(Point(x=4,y=3)))
		self.assertFalse(Point(x=3,y=4).yWiseLessThan(Point(x=4,y=3)))
		self.assertTrue(Point(x=4,y=3).yWiseLessOrEq(Point(x=3,y=4)))
		self.assertFalse(Point(x=4,y=3).xWiseLessOrEq(Point(x=3,y=4)))
		self.assertTrue(Point(x=3,y=4).xWiseLessOrEq(Point(x=4,y=3)))
		self.assertFalse(Point(x=3,y=4).yWiseLessOrEq(Point(x=4,y=3)))

	def test_equal(self):
		self.assertEqual(Point(x=4,y=3), Point(x=4,y=3))
		self.assertEqual(POINT(x=4,y=3), Point(x=4,y=3))
		self.assertNotEqual(Point(x=3,y=4), Point(x=4,y=3))
		self.assertNotEqual(POINT(x=3,y=4), Point(x=4,y=3))
