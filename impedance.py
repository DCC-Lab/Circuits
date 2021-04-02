from numpy import angle, linspace,pi
import matplotlib.pyplot as plt


class Impedance:
    def __init__(self):
        self.terminals = (1,0)

    def __repr__(self):
        string  = "\n"
        string += "               ┏━━━┓ \n"
        string += " terminal 1 ━━━┃ Z ┃━━━ terminal 0\n"
        string += "               ┗━━━┛ "
        return string

    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        return None

    def voltageAt(self, terminal=1, vs=1.0, frequency=None):
        """ Returns the voltage with respect to ground at the terminal.
        Vs is always connected to terminal 1, gnd to terminal 0.

        It is a simple application of Kirchoff's law: V = Z * I.
        If the vs source is at terminal 1, and gnd at terminal 0,
        then the current is I = Vs/Ztot. The drop across the component
        is simply Z*I.

        This function here appears fairly trivial, but it is useful to
        subclasses, such as Series, where terminal can be such that we measure
        the voltage across Z2 (for an RC filter for instance). """

        z_component = self.impedance(frequency, terminalPlus=terminal, terminalMinus=0)
        z_total = self.impedance(frequency)
        return z_component*(vs/z_total)

    def connectInParallelWith(self, impedance):
        return Parallel(z1=self, z2=impedance)
    def connectInSeriesWith(self, impedance):
        return Series(z1=self, z2=impedance)

    def showImpedanceResponse(self):
        amplitude = []
        phase = []

        frequencies = 10**(linspace(-1,6,100))
        for frequency in frequencies:
            z = self.impedance(frequency=frequency)
            amplitude.append(abs(z))
            phase.append(angle(z))
        fig,(axis1,axis2) = plt.subplots(1,2, sharex=True,figsize=(10,5))
        axis1.plot(frequencies, amplitude,'k')
        plt.xscale('log')
        axis2.plot(frequencies, phase,'k')
        plt.xscale('log')

        axis1.set_xlabel("Frequency [Hz]")
        axis2.set_xlabel("Frequency [Hz]")
        axis1.set_ylabel(r"Impedance [$\Omega$]")
        axis2.set_ylabel("Phase [rad]")
        axis1.grid(True)
        axis2.grid(True)
        plt.show()

class Resistor(Impedance):
    def __init__(self, R):
        Impedance.__init__(self)
        self.R = R
    def __repr__(self):
        string  = "\n"
        string += "               ┏━━━┓ \n"
        string += " terminal 1 ━━━┃ R ┃━━━ terminal 0\n"
        string += "               ┗━━━┛ "
        return string
    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        return self.R

class Capacitor(Impedance):
    def __init__(self, C):
        Impedance.__init__(self)
        self.C = C
    def __repr__(self):
        string  = "\n"
        string += "               ┃   ┃ \n"
        string += " terminal 1 ━━━┃ C ┃━━━ terminal 0\n"
        string += "               ┃   ┃ \n"
        return string
    def impedance(self, frequency=None):
        if frequency is None:
            return None
        return 1/(1j*2*pi*frequency*self.C)

class Inductor(Impedance):
    def __init__(self, L):
        Impedance.__init__(self)
        self.L = L       
    def __repr__(self):
        string  = "\n"
        string += "               ︗︗︗\n"
        string += " terminal 1 ━━━  L   ━━━ terminal 0\n"
        string += "               ︘︘︘"
        return string
    def impedance(self, frequency=None):
        if frequency is None:
            return None
        return 1j*2*pi*frequency*self.L


class Parallel(Impedance):
    def __init__(self, z1, z2):
        Impedance.__init__(self)
        self.z1 = z1
        self.z2 = z2
    def __repr__(self):
        string  = "                ┏━━━━┓\n"
        string += "            ┏━━━┫ Z1 ┣━━━┓\n"
        string += "terminal 1 ━┫   ┗━━━━┛   ┣━ terminal 0\n"
        string += "            ┃   ┏━━━━┓   ┃\n"
        string += "            ┗━━━┫ Z2 ┣━━━┛\n"
        string += "                ┗━━━━┛ "
    def impedance(self, frequency=None):
        return 1/(1/self.z1.Z(frequency) + 1/self.z2.Z(frequency))

class Series(Impedance):
    def __init__(self, z1, z2):
        Impedance.__init__(self)
        self.z1 = z1
        self.z2 = z2

    def __repr__(self):
        string  = "               ┏━━━━┓              ┏━━━━┓\n"
        string += " terminal 1 ━━━┃ Z1 ┃━ terminal 2 ━┃ Z2 ┃━ terminal 0\n"
        string += "               ┗━━━━┛              ┗━━━━┛"

    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        if terminalPlus == 1 and terminalMinus == 0:
            return self.z1.Z(frequency) + self.z2.Z(frequency)
        elif terminalPlus == 2 and terminalMinus == 0:
            return self.z2.Z(frequency)
        elif terminalPlus == 1 and terminalMinus == 2:
            return self.z1.Z(frequency)

    def voltageAt(self, terminal=2, vs=1.0, frequency=None):
        """ Returns the voltage with respect to ground at the terminal.
        The default is between the two components.
        Vs is always connected at terminal 1, gnd at terminal 0.

        It is a simple application of Kirchoff's law: V = Z * I.
        If the vs source is at terminal 1, and gnd at terminal 0,
        then the current is I = Vs/Ztot. The drop across the component
        is simply Z*I
        """
        return Impedance.voltageAt(self, terminal, vs, frequency)

class Divider:
    def __init__(self, z1, z2):
        self.z1 = z1
        self.z2 = z2
        self.zt = z1.connectInSeriesWith(z2)

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
    Z1 = R.connectInSeriesWith(C)
    Z2 = R.connectInParallelWith(C)

    # Divider(Z1,Z2).showResponse()
    # Divider(R1,R2).showResponse()
    opamp = OpAmp(Divider(R,C),Divider(R,R))
    opamp.showResponse()
