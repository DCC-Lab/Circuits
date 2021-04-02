import unittest
import numpy as np
from impedance import *

class TestComponent(unittest.TestCase):
    def testSimpleComponent(self):
        self.assertIsNotNone(Component())

    def testSimpleResistor(self):
        self.assertTrue(Resistor(100).label == "Resistor [100 Ω]")

    def testPrintComponent(self):
        print("\n",Component())
        print("\n",Resistor(R=100))
        print("\n",Capacitor(C=1e-6))
        print("\n",Inductor(L=1e-3))

    def testInitValuesComponents(self):
        z = Resistor(R=100)
        self.assertIsNotNone(z.impedance())
        self.assertAlmostEqual(z.impedance(), 100)
        self.assertAlmostEqual(z.impedance(frequency=200), 100)

        z = Capacitor(C=1e-6)
        self.assertIsNone(z.impedance())
        self.assertAlmostEqual(z.impedance(frequency=200), 1/2j/np.pi/200/1e-6)

        z = Inductor(L=1e-3)
        self.assertIsNone(z.impedance())
        self.assertAlmostEqual(z.impedance(frequency=200), 2j*np.pi*200*1e-3)

    # @unittest.skip
    def testShowResponse(self):
        z = Resistor(R=100)
        z.showComponentResponse()

        z = Capacitor(C=1e-6)
        z.showComponentResponse()

        z = Inductor(L=1e-3)
        z.showComponentResponse()

    def testSeriesComponent(self):
        z1 = Resistor(R=100)
        z2 = Resistor(R=200)
        series = Series(z1,z2)
        self.assertAlmostEqual(series.impedance(), 300)
        self.assertAlmostEqual(series.impedance(), z1.impedance()+z2.impedance())
        self.assertAlmostEqual(series.impedance(terminalPlus=2, terminalMinus=0), 200)
        self.assertAlmostEqual(series.impedance(terminalPlus=1, terminalMinus=2), 100)

    def testParallelComponent(self):
        z1 = Resistor(R=100)
        z2 = Resistor(R=200)
        parallel = Parallel(z1,z2)
        self.assertAlmostEqual(parallel.impedance(), 200/3)

    def testSeriesVoltage(self):
        z1 = Resistor(R=100)
        z2 = Resistor(R=200)
        series = Series(z1,z2)
        self.assertAlmostEqual(series.voltageAt(terminal=2), 1*200/(100+200))

    def testParallelVoltage(self):
        z1 = Resistor(R=100)
        z2 = Resistor(R=200)
        parallel = Parallel(z1,z2)
        self.assertAlmostEqual(parallel.voltageAt(terminal=1), 1)

    # @unittest.skip
    def testShowResponse(self):
        z = Resistor(R=100)
        z.showVoltageResponse()

        z = Capacitor(C=1e-6)
        z.showVoltageResponse()

        z = Inductor(L=1e-3)
        z.showVoltageResponse()

        z1 = Resistor(R=100)
        z2 = Resistor(R=200)
        Parallel(z1,z2).showVoltageResponse()
        Series(z1,z2).showVoltageResponse()

    def testShowRCFilter(self):
        r = Resistor(R=100)
        c = Capacitor(C=1e-6)
        lowPass = Series(r,c, label="Low-pass RC filter")
        lowPass.showVoltageResponse(terminal=2)
        highPass = Series(c,r, label="High-pass RC filter")
        highPass.showVoltageResponse(terminal=2)

if __name__ == '__main__':
    unittest.main()
