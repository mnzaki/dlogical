# DLogical
A Digital Logic Simulation in python.

The simulation is capable of modeling a digital logic circuit and its components
at any level varying from the behavioral to the gate level.

An example of a circuit instance is inside [mips/arch.py](mips/arch.py). This is a simple MIPS
system simulation.

The simulation application is currently hardcoded to run the mips simulation
against an assembly file. It can be run like so:  
`sim.py tests/test_mips_asm1.asm1`

## Component Definition
All components inherit from the `Component` abstract base class. A new component
needs to specify its `inputs` and `outputs` and the `simulate` method at the
bare minimum. An example component, the D Register:

```
class DRegister32(Component):
  delay = 100

  inputs = {'q': '32'}
  outputs = {'d': '32'}

  def simulate(self, inputs, outputs):
    if 'q' in inputs:
      outputs.d = inputs.q
```

The `simulate` method is called with two `Message` objects (specialized `dict`s
really). The `inputs` object contains all inputs that have changed. The
`outputs` object is expected to be filled with outputs that should change. The
component may also need to access its port data directly, but it should never
assign to it directly:

```
self.q.data
self.d.data
```

## Parametrized Components
A Parametrized Component can be used as a class factory to create components of
varied widths for example. Example of the above D Register (from
[components/registers.py](components/registers.py)):

```
class DRegister(ParametrizedComponent):
  delay = 100
  shape = Rectangle(150, 200)

  parameters = {'width': 8}
  inputs = {'q': 'width'}
  outputs = {'d': 'width'}

  def simulate(self, inputs, outputs):
    if 'q' in inputs:
      outputs.d = inputs.q

DRegister32 = DRegister.with_parameters(width = 32)
```

## Circuit Specification
[mips/arch.py](mips/arch.py) contains a good detailed example. A quick extract:

```
clk = Oscillator.with_parameters(freq = 10000)()

# It starts with a counter :')
pc = DRegisterSync32(clk = clk.clk[:])

imem = Mem.with_parameters(width = 32, size = 1024)(
        addr = pc.d[:],
        write_en = 0,
        read_en = 1)

control = ControlUnit(opcode = imem.read[31:26],
                      funct  = imem.read[5:0])
```

