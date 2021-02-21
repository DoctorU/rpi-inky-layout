import unittest
from rpi_inky_layout import Layout, Rotation


class TestIssue37(unittest.TestCase):

    def testIssue37(self):
        i_res = (250, 122)
        layout = Layout(i_res, packingMode='v', rotation=Rotation.LEFT)
        _ratesLayer = layout.addLayer()
        _time = layout.addLayer()
        _attrs = _ratesLayer.addLayer(packingBias=1)
        _rates = _ratesLayer.addLayer(packingBias=3)

        self.assertEqual((30, 124), _attrs.size)
        self.assertEqual((90, 124), _rates.size)
        self.assertEqual((122, 124), _time.size)
        self.assertEqual(0, _ratesLayer._showSparePixels())


if __name__ == '__main__':
    unittest.main()
