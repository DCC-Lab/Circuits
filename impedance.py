from numpy import angle, linspace,pi
import matplotlib.pyplot as plt

class Impedance:
    def impedance(self, frequency):
        return None
    def Z(self, frequency):
        return self.impedance(frequency)
    def phase(self, frequency):
        return angle(self.Z(frequency))
    def amplitude(self, frequency):
        return abs(self.Z(frequency))
    def inParallelWith(self, impedance):
        return Parallel(self, impedance)
    def inSeriesWith(self, impedance):
        return Series(self, impedance)
    def showResponse(self):
        amplitude = []
        phase = []

        frequencies = 10**(linspace(-1,6,100))
        for f in frequencies:
            amplitude.append( abs(self.Z(f)))
            phase.append( angle(self.Z(f)))
        fig,(axis1,axis2) = plt.subplots(1,2, sharex=True,figsize=(10,5))
        axis1.plot(frequencies, amplitude,'k')
        plt.xscale('log')
        axis2.plot(frequencies, phase,'k')
        plt.xscale('log')

        axis1.set_xlabel("Frequency [Hz]")
        axis2.set_xlabel("Frequency [Hz]")
        axis1.set_ylabel("Z [Ω]")
        axis2.set_ylabel("Phase [rad]")
        axis1.grid(True)
        axis2.grid(True)
        plt.show()

class Parallel(Impedance):
    def __init__(self, z1, z2):
        Impedance.__init__(self)
        self.z1 = z1
        self.z2 = z2
    def impedance(self, frequency):
        return 1/(1/self.z1.Z(frequency) + 1/self.z2.Z(frequency))

class Series(Impedance):
    def __init__(self, z1, z2):
        Impedance.__init__(self)
        self.z1 = z1
        self.z2 = z2
    def impedance(self, frequency):
        return self.z1.Z(frequency) + self.z2.Z(frequency)

class Divider:
    def __init__(self, z1, z2):
        self.z1 = z1
        self.z2 = z2
        self.zt = z1.inSeriesWith(z2)

    def voltage(self, frequency):
        return self.z1.Z(frequency)/self.zt.Z(frequency)

    def showResponse(self):
        amplitude = []
        phase = []

        frequencies = 10**(linspace(-1,6,100))
        for f in frequencies:
            v = self.voltage(f)
            amplitude.append(abs(v))
            phase.append(angle(f))
        fig,(axis1,axis2) = plt.subplots(1,2, sharex=True,figsize=(10,5))
        axis1.plot(frequencies, amplitude,'k')
        plt.xscale('log')
        axis2.plot(frequencies, phase,'k')
        plt.xscale('log')

        axis1.set_xlabel("Frequency [Hz]")
        axis2.set_xlabel("Frequency [Hz]")
        axis1.set_ylabel("Response")
        axis2.set_ylabel("Phase [rad]")
        axis1.grid(True)
        axis2.grid(True)
        plt.show()


class Resistor(Impedance):
    def __init__(self, R):
        Impedance.__init__(self)
        self.R = R
    def impedance(self, frequency):
        return self.R

class Capacitor(Impedance):
    def __init__(self, C):
        Impedance.__init__(self)
        self.C = C
    def impedance(self, frequency):
        return 1/(1j*2*pi*frequency*self.C)

class Inductor(Impedance):
    def __init__(self, L):
        Impedance.__init__(self)
        self.L = L       
    def impedance(self, frequency):
        return 1j*2*pi*frequency*self.L

class OpAmp:
    def __init__(self, vp, vn):
        self.vp = vp
        self.vn = vn
    def showResponse(self):
        vps = []
        phaseps = []
        vns = []
        phasens = []

        frequencies = 10**(linspace(-1,6,100))
        for f in frequencies:
            vp = self.vp.voltage(f)
            vps.append(abs(vp))
            phaseps.append(angle(vp))
            vn = self.vn.voltage(f)
            vns.append(abs(vn))
            phasens.append(angle(vn))
        fig,(axis1,axis2) = plt.subplots(1,2, sharex=True,figsize=(10,5))
        axis1.plot(frequencies, vps,'k')
        axis1.plot(frequencies, vns,'k')
        plt.xscale('log')
        axis2.plot(frequencies, phaseps,'k')
        axis2.plot(frequencies, phasens,'k')
        plt.xscale('log')

        axis1.set_xlabel("Frequency [Hz]")
        axis2.set_xlabel("Frequency [Hz]")
        axis1.set_ylabel("Response")
        axis2.set_ylabel("Phase [rad]")
        axis1.grid(True)
        axis2.grid(True)
        plt.show()


if __name__ == "__main__":
    R1 = Resistor(10000)
    R2 = Resistor(5000)

    R = Resistor(10000)
    C = Capacitor(1e-6)
    Z1 = R.inSeriesWith(C)
    Z2 = R.inParallelWith(C)

    Divider(Z1,Z2).showResponse()
    Divider(R1,R2).showResponse()
    opamp = OpAmp(Divider(Z1,Z2),Divider(R1,R2))
    opamp.showResponse()
