import numpy as np

class Beamsplitter(object):

    def __init__(self, *inputs):
        self.inputs = inputs
        self.transmission = .5
        phi = np.pi/2
        sp, cp = np.sin(phi), np.cos(phi)
        self.unitary = np.array([[cp, 1j*sp], [1j*sp, cp]], dtype=complex) 

    def __str__(self):
        return "(Beamsplitter: {:.2f})".format(self.transmission)

class PhaseShifter(object):

    def __init__(self, input, phase=np.pi/2):
        self.inputs = [input]
        self.phase = phase
        self.unitary = np.array([[np.exp(1j*phase)]], dtype=complex)

    def __str__(self):
        return "(Phasehifter: {:.2f})".format(self.phase)

class Mapping(object):

    def __init__(self, *mapping):
        self.mapping = mapping
        self.inputs = tuple(x[0] for x in mapping)
        self.outputs = tuple(x[1] for x in mapping)
        space = sorted(set(self.inputs) | set(self.outputs))
        self.d = len(space)
        t = dict(zip(space, xrange(self.d)))
        self.unitary = np.zeros((self.d, self.d), dtype = complex)
        for a, b in mapping:
            self.unitary[t[a], t[b]] = 1

    def __str__(self):
        return "(Mapping: {})".format(", ".join(str(m) for m in self.mapping))

class Circuit(object):
    def __init__(self):
        self.things = []

    def add(self, *things):
        try:
            self.things += things
        except:
            pass

    def __str__(self):
        things = ", ".join(str(t) for t in self.things)
        s = "({}: {})".format(self.__class__.__name__, things)
        return s

class FusionII(Circuit):
    def __init__(self, *modes):
        Circuit.__init__(self)
        m0, m1, m2, m3 = modes
        self.add(Beamsplitter(m0, m1),
                 Beamsplitter(m2, m3),
                 Mapping((m1, m2), (m2, m1)),
                 Beamsplitter(m0, m1),
                 Beamsplitter(m2, m3))

class TwoFusions(Circuit):
    def __init__(self):
        Circuit.__init__(self)
        self.add(FusionII(0, 1, 2, 3))
        self.add(FusionII(4,5,6,7))

f = TwoFusions()
print f
