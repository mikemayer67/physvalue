import unittest

from pval.quantity import Quantity as Q
from pval.exceptions import InvalidUnitDefinition
from pval.exceptions import IncompatibleUnits

class QuantityTests(unittest.TestCase):
    def test_init(self):
        q = Q(1,m=1)
        self.assertEqual(q.value,1)
        self.assertEqual(q.unit,(1,0,0,0,0,0,0))

        q = Q(3.5,m=1,sec=-1)
        self.assertEqual(q.value,3.5)
        self.assertEqual(q.unit,(1,0,-1,0,0,0,0))

        q = Q(12.1467)
        self.assertEqual(type(q),float)
        self.assertEqual(q,12.1467)

    def test_init_with_unit(self):
        x1 = Q(1,unit=(1,0,0,0,0,0,0))
        self.assertEqual(x1.value,1)
        self.assertEqual(x1.unit,(1,0,0,0,0,0,0))

        x2 = Q(2,unit=x1)
        self.assertEqual(x2.value,2)
        self.assertEqual(x2.unit,(1,0,0,0,0,0,0))

        x3 = Q(3.5,unit=x1.unit)
        self.assertEqual(x3.value,3.5)
        self.assertEqual(x3.unit,(1,0,0,0,0,0,0))

        x4 = Q(3.5,unit=x2)
        self.assertEqual(x4.value,7)
        self.assertEqual(x4.unit,(1,0,0,0,0,0,0))

        q = Q(1.2,unit=[1,2,3,4,5,6,7])
        self.assertEqual(q.value,1.2)
        self.assertEqual(q.unit,(1,2,3,4,5,6,7))

        with self.assertRaises(InvalidUnitDefinition) as cm:
            q = Q(1.2,unit='km')

        with self.assertRaises(InvalidUnitDefinition) as cm:
            q = Q(1.2,unit=(1,2,3))


    def test_compatible(self):
        x_m = Q(1.2,m=1)
        x_ft = Q(3.5,m=1)
        x_kg = Q(3.5,kg=1)
        self.assertTrue( x_m.compatible(x_ft) )
        self.assertFalse( x_m.compatible(x_kg) )

    def test_abs(self):
        q = Q(1,kg=1)
        r = abs(q)
        self.assertEqual(q.value,1)
        self.assertEqual(r.value,1)
        self.assertEqual(q.unit,(0,1,0,0,0,0,0))

        q = Q(-1.2,kg=1)
        r = abs(q)
        self.assertEqual(q.value,-1.2)
        self.assertEqual(r.value,1.2)
        self.assertEqual(q.unit,(0,1,0,0,0,0,0))

    def test_add(self):
        a = Q(1.2,m=1,sec=-1)
        b = Q(10,m=1,sec=-1)
        c = a + b
        self.assertEqual(c.value,11.2)
        self.assertEqual(c.unit,(1,0,-1,0,0,0,0))

        b = Q(10,m=1,sec=-2)
        with self.assertRaises(IncompatibleUnits) as cm:
            c = a + b

        with self.assertRaises(IncompatibleUnits) as cm:
            c = a + 3

        with self.assertRaises(IncompatibleUnits) as cm:
            c = 2.5 + a

    def test_neg(self):
        q = Q(1.2,m=1,sec=-1)
        n = -q
        p = -n
        self.assertEqual(q.value,1.2)
        self.assertEqual(n.value,-1.2)
        self.assertEqual(p.value,1.2)
        self.assertEqual(q.unit,(1,0,-1,0,0,0,0))
        self.assertEqual(n.unit,(1,0,-1,0,0,0,0))
        self.assertEqual(p.unit,(1,0,-1,0,0,0,0))

    def test_sub(self):
        a = Q(1.2,m=2,sec=-1)
        b = Q(10,m=2,sec=-1)
        c = b-a
        self.assertEqual(c.value,8.8)
        self.assertEqual(c.unit,(2,0,-1,0,0,0,0))
        c = a-b
        self.assertEqual(c.value,-8.8)
        self.assertEqual(c.unit,(2,0,-1,0,0,0,0))

        b = Q(10,m=1,sec=-2)
        with self.assertRaises(IncompatibleUnits) as cm:
            c = a - b

        with self.assertRaises(IncompatibleUnits) as cm:
            c = b - a

        with self.assertRaises(IncompatibleUnits) as cm:
            c = a - 3

        with self.assertRaises(IncompatibleUnits) as cm:
            c = 3 - a

    def test_mul(self):
        v = Q(1.2,m=1,sec=-1)
        t = Q(3,sec=1,K=5)

        d = v * t
        self.assertAlmostEqual(d.value,3.6)
        self.assertEqual(d.unit,(1,0,0,0,5,0,0))

        d = t * v
        self.assertAlmostEqual(d.value,3.6)
        self.assertEqual(d.unit,(1,0,0,0,5,0,0))

        vv = 2.1 * v
        self.assertAlmostEqual(vv.value,2.52)
        self.assertEqual(vv.unit,(1,0,-1,0,0,0,0))

        vv = v * -3
        self.assertAlmostEqual(vv.value,-3.6)
        self.assertEqual(vv.unit,(1,0,-1,0,0,0,0))

    def test_truediv(self):
        d = Q(1.2,m=1)
        t = Q(3,sec=1,K=5)

        v = d/t
        self.assertAlmostEqual(v.value,0.4)
        self.assertEqual(v.unit,(1,0,-1,0,-5,0,0))

        q = t/d
        self.assertAlmostEqual(q.value,2.5)
        self.assertEqual(q.unit,(-1,0,1,0,5,0,0))

        q = t / 2 
        self.assertAlmostEqual(q.value,1.5)
        self.assertEqual(q.unit,(0,0,1,0,5,0,0))

        q = -3.3 / t
        self.assertAlmostEqual(q.value,-1.1)
        self.assertEqual(q.unit,(0,0,-1,0,-5,0,0))

    def test_floordiv(self):
        d = Q(1.2,m=1)
        t = Q(3,sec=1,K=5)

        v = d//t
        self.assertAlmostEqual(v.value,0.0)
        self.assertEqual(v.unit,(1,0,-1,0,-5,0,0))

        q = t//d
        self.assertAlmostEqual(q.value,2)
        self.assertEqual(q.unit,(-1,0,1,0,5,0,0))

        q = t // 2 
        self.assertAlmostEqual(q.value,1)
        self.assertEqual(q.unit,(0,0,1,0,5,0,0))

        q = -3.3 // t
        self.assertAlmostEqual(q.value,-2)
        self.assertEqual(q.unit,(0,0,-1,0,-5,0,0))




