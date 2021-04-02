import unittest
import numpy as np
from impedance import *

class TestImpedance(unittest.TestCase):
    def testSimpleImpedance(self):
        self.assertIsNotNone(Impedance())

    def testPrintImpedance(self):
        print("\n",Impedance())
        print("\n",Resistor(R=100))
        print("\n",Capacitor(C=100))
        print("\n",Inductor(L=100))

    def testInitValuesImpedances(self):
        z = Resistor(R=100)
        self.assertIsNotNone(z.impedance())
        self.assertAlmostEqual(z.impedance(), 100)
        self.assertAlmostEqual(z.impedance(frequency=200), 100)

        z = Capacitor(C=100)
        self.assertIsNone(z.impedance())
        self.assertAlmostEqual(z.impedance(frequency=200), 1/2j/np.pi/200/100)

        z = Inductor(L=100)
        self.assertIsNone(z.impedance())
        self.assertAlmostEqual(z.impedance(frequency=200), 2j*np.pi*200*100)

    def testShowResponse(self):
        z = Resistor(R=100)
        z.showImpedanceResponse()
        
        z = Capacitor(C=100)
        z.showImpedanceResponse()

        z = Inductor(L=100)
        z.showImpedanceResponse()

if __name__ == '__main__':
    unittest.main()
