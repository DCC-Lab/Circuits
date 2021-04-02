from numpy import angle, linspace,pi
import matplotlib.pyplot as plt

""" A simple Python script to look at components and very simple circuits.
This is by no means a complete module to study systems: it only looks
at very basic aspects of components: their impedance, its frequency response
and it provides simple tools to connect things in series or in parallel.

Who is this for?
================

If you really want to simulate a circuit, use circuitlab.com or others. There
are tons of such web sites that are excellent. However, they may be excellent
but sometimes, students have questions that are simple but require a bit of
experimenting with components. It is therefore the purpose of this script 
to allow visualizing the impedance of components and some combinations.

Notes on programming
====================

This may also be an example of how to use object-oriented programming to
simplify  the code: here, we know that any component will have an impedance,
and we will be interested in its frequency response.  Hence, the base class
Component provides all the necessary tools to do so. """

class Component:
    def __init__(self, label=None):
        """ Any 2-terminal electrical component.
        
        We label the terminals in order to allow connections in series and
        parallel later, which will force us to identify more terminals.
        """

        self.terminals = (1,0)
        self.label = label if label is not None else "Component"

    def __repr__(self):
        """ Representation of the component with its terminals """
        string  = "\n"
        string += "               ┏━━━┓ \n"
        string += " terminal 1 ━━━┫ Z ┣━━━ terminal 0\n"
        string += "               ┗━━━┛ "
        return string

    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        """ Subclasses must override this and provide the complex impedance
        for the component between the terminals.  By default, Component does not know anything about the
        impedance. """
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

    def connectInParallelWith(self, component):
        """ Return this component connected in parallel with another component """
        return Parallel(z1=self, z2=component)
    def connectInSeriesWith(self, component):
        """ Return this component connected in series with another component """
        return Series(z1=self, z2=component)

    def showImpedanceResponse(self, terminal=1):
        """ Shows the frequency dependence (Bode plot) of the component
        between the requested terminal and terminal 0, typically the ground. For any
        2-terminal component, this will simply be the impedance of the component. 
        However, in a multi-terminal component, it is possible to use any other
        terminal. """

        amplitude = []
        phase = []

        frequencies = 10**(linspace(-1,6,100))
        for frequency in frequencies:
            z = self.impedance(frequency=frequency, terminalPlus=terminal)
            amplitude.append(abs(z))
            phase.append(angle(z))

        fig,(axis1,axis2) = plt.subplots(1,2, sharex=True,figsize=(10,5))
        axis1.plot(frequencies, amplitude,'k')
        plt.xscale('log')
        axis2.plot(frequencies, phase,'k')
        plt.xscale('log')

        axis1.set_title(self.label)
        axis1.set_xlabel("Frequency [Hz]")
        axis2.set_xlabel("Frequency [Hz]")
        axis1.set_ylabel(r"Component [$\Omega$]")
        axis2.set_ylabel("Phase [rad]")
        axis1.grid(True)
        axis2.grid(True)
        plt.show()

    def showVoltageResponse(self, terminal=2):
        """ Shows the Bode plot at the requested  terminal of the component
        (or components) with a unit voltage source of 1V connected to terminal 1 of
        the device.  For now, this graph will be trivially 1V across the spectrum for
        a 2-terminal device: the drop from Vs to GND through any component  is always
        Vs.  However, with two components in Series, the response  at terminal 2
        (between the components) is interesting and worht plotting.    """
        amplitude = []
        phase = []

        frequencies = 10**(linspace(-1,6,100))
        for f in frequencies:
            v = self.voltageAt(terminal=terminal, frequency=f, vs=1.0)
            amplitude.append(abs(v))
            phase.append(angle(f))
        fig,(axis1,axis2) = plt.subplots(1,2, sharex=True,figsize=(10,5))
        axis1.plot(frequencies, amplitude,'k')
        plt.xscale('log')
        axis2.plot(frequencies, phase,'k')
        plt.xscale('log')
        axis1.set_title(self.label)
        axis1.set_xlabel("Frequency [Hz]")
        axis2.set_xlabel("Frequency [Hz]")
        axis1.set_ylabel("Response with 1V source")
        axis2.set_ylabel("Phase [rad]")
        axis1.grid(True)
        axis2.grid(True)
        plt.show()


class Resistor(Component):
    def __init__(self, R, label=None):
        """ A resistor of R Ohms """
        Component.__init__(self, label)
        self.R = R
        self.label = label if (label is not None) else "Resistor"

    def __repr__(self):
        """ Representation of the component with its terminals """
        string  = "\n"
        string += "               ┏━━━┓ \n"
        string += " terminal 1 ━━━┫ R ┣━━━ terminal 0\n"
        string += "               ┗━━━┛ "
        return string
    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        """ The impedance of a resistor is constant across all frequencies """
        return self.R

class Capacitor(Component):
    def __init__(self, C, label=None):
        """ A capacitor of C Farads (typically ~1e-6)"""
        Component.__init__(self, label)
        self.C = C
        self.label = label if (label is not None) else "Capacitor"

    def __repr__(self):
        """ Representation of the component with its terminals """
        string  = "\n"
        string += "               ┃   ┃ \n"
        string += " terminal 1 ━━━┫ C ┣━━━ terminal 0\n"
        string += "               ┃   ┃ \n"
        return string
    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        """ The impedance of a capacitor varies across all frequencies: it is
        infinite at DC and nearly zero at very high frequency. """
        if frequency is None:
            return None
        return 1/(1j*2*pi*frequency*self.C)

class Inductor(Component):
    def __init__(self, L, label=None):
        """ Am inductor of L Henry (typically ~1e-3)"""
        Component.__init__(self, label)
        self.L = L       
        self.label = label if (label is not None) else "Inductor"

    def __repr__(self):
        """ Representation of the component with its terminals """
        string  = "\n"
        string += "               ︗︗︗\n"
        string += " terminal 1 ━━━  L   ━━━ terminal 0\n"
        string += "               ︘︘︘"
        return string
    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        """ The impedance of an inductor varies across all frequencies: it is
        very high at high frequencies and nearly zero at very low frequency. """
        if frequency is None:
            return None
        return 1j*2*pi*frequency*self.L


class Parallel(Component):
    def __init__(self, z1, z2, label=None):
        """ Two components in parallel. The component remains a 2-terminal component."""
        Component.__init__(self, label=label)
        self.z1 = z1
        self.z2 = z2
        self.label = label if (label is not None) else "z1 z2 in parallel"
    def __repr__(self):
        """ Representation of the component with its terminals """        
        string  = "                ┏━━━━┓\n"
        string += "            ┏━━━┫ Z1 ┣━━━┓\n"
        string += "            ┃   ┗━━━━┛   ┃\n"
        string += "terminal 1 ━┫            ┣━ terminal 0\n"
        string += "            ┃   ┏━━━━┓   ┃\n"
        string += "            ┗━━━┫ Z2 ┣━━━┛\n"
        string += "                ┗━━━━┛ "

    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        """ The impedance of the two components is the inverse of the sum of
        their inverses. """
        return 1/(1/self.z1.impedance(frequency) + 1/self.z2.impedance(frequency))

class Series(Component):
    def __init__(self, z1, z2, label=None):
        """ Two components in series, z1 first then z2. The point in between
        is terminal 2.  This is also a synonym for Divider."""
        Component.__init__(self, label=label)
        self.z1 = z1
        self.z2 = z2
        self.label = label if (label is not None) else "Z1+Z2 divider"

    def __repr__(self):
        """ Representation of the component with its terminals. The terminal
        between the components is terminal 2."""        
        string  = "               ┏━━━━┓              ┏━━━━┓\n"
        string += " terminal 1 ━━━┫ Z1 ┣━ terminal 2 ━┫ Z2 ┣━ terminal 0\n"
        string += "               ┗━━━━┛              ┗━━━━┛"

    def impedance(self, frequency=None, terminalPlus=1, terminalMinus=0):
        """ Returns the impedance of the components in series depending on the
        terminals requested. """
        if terminalPlus == 1 and terminalMinus == 0:
            return self.z1.impedance(frequency) + self.z2.impedance(frequency)
        elif terminalPlus == 2 and terminalMinus == 0:
            return self.z2.impedance(frequency)
        elif terminalPlus == 1 and terminalMinus == 2:
            return self.z1.impedance(frequency)

    def voltageAt(self, terminal=2, vs=1.0, frequency=None):
        """ Returns the voltage with respect to ground at the terminal.
        The default is between the two components.
        Vs is always connected at terminal 1, gnd at terminal 0.

        It is a simple application of Kirchoff's law: V = Z * I.
        If the vs source is at terminal 1, and gnd at terminal 0,
        then the current is I = Vs/Ztot. The drop across the component
        is simply Z*I
        """
        return Component.voltageAt(self, terminal, vs, frequency)


class OpAmpAnalysis:
    def __init__(self, vp, pTerm, vn, nTerm):
        self.vp = vp
        self.pTerm = pTerm
        self.vn = vn
        self.nTerm = nTerm
    def showInputs(self):
        vps = []
        phaseps = []
        vns = []
        phasens = []

        frequencies = 10**(linspace(-1,6,100))
        for f in frequencies:
            vp = self.vp.voltageAt(frequency=f, terminal=self.pTerm)
            vps.append(abs(vp))
            phaseps.append(angle(vp))
            vn = self.vn.voltageAt(frequency=f, terminal=self.nTerm)
            vns.append(abs(vn))
            phasens.append(angle(vn))
        fig,(axis1,axis2) = plt.subplots(1,2, sharex=True,figsize=(10,5))
        axis1.plot(frequencies, vps,'k+')
        axis1.plot(frequencies, vns,'k|')
        plt.xscale('log')
        axis2.plot(frequencies, phaseps,'k+')
        axis2.plot(frequencies, phasens,'k|')
        plt.xscale('log')

        axis1.set_title("+ input of OpAmp")

        axis2.set_title("- input of OpAmp")
        axis1.set_xlabel("Frequency [Hz]")
        axis2.set_xlabel("Frequency [Hz]")
        axis1.set_ylabel("Response")
        axis2.set_ylabel("Phase [rad]")
        axis1.grid(True)
        axis2.grid(True)
        plt.show()


if __name__ == "__main__":

    R = Resistor(10000)
    C = Capacitor(1e-6)
    C.showImpedanceResponse()
    
    divider = Series(R, C, "Low pass RC filter")
    divider.showImpedanceResponse()

    R = Resistor(10000)
    C = Capacitor(1e-6)
    opamp = OpAmpAnalysis(vp=Series(R,C), pTerm=2, vn=Series(R,R), nTerm=2)
    opamp.showInputs()
