"""Geometric regression checks for native artwork on a photographed shirt plane."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from badge_surface import projection, validate_surface


class ShirtSurfaceTests(unittest.TestCase):
    def test_frontal_surface_keeps_straight_features(self):
        point = projection({'corners':[(100,100),(140,100),(140,140),(100,140)],'curve':0})
        self.assertEqual(point(.25,.75), (110,130))

    def test_foreshortened_center_is_diagonal_intersection(self):
        point = projection({'corners':[(100,100),(160,100),(150,160),(110,160)],'curve':0})
        x,y=point(.5,.5)
        self.assertAlmostEqual(x,130)
        self.assertAlmostEqual(y,136)
        self.assertAlmostEqual(point(0,1)[0],110)
        self.assertAlmostEqual(point(1,1)[0],150)

    def test_curved_print_has_continuous_shared_edges(self):
        point = projection({'corners':[(100,100),(160,112),(150,175),(92,160)],'curve':.7})
        for i in range(1,8):
            a=point(i/8-1e-7,.45);b=point(i/8+1e-7,.45)
            self.assertLess(abs(a[0]-b[0])+abs(a[1]-b[1]),.001)

    def test_mirrored_folded_and_degenerate_surfaces_are_rejected(self):
        for corners in [((140,100),(100,100),(100,140),(140,140)),
                        ((100,100),(140,140),(140,100),(100,140)),
                        ((100,100),(140,100),(140,100),(100,100))]:
            with self.assertRaises(ValueError):
                validate_surface({'corners':corners,'curve':0})


if __name__=='__main__':
    unittest.main()
