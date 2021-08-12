from simtk.openmm.app import PDBFile, ForceField, PME, HBonds, Simulation
from simtk.openmm import MonteCarloBarostat, LangevinIntegrator
from simtk.unit import picoseconds, picosecond, nanometer, kelvin, bar
from sys import stdout
import sys

# Takes inputs of bstate-file.pdb, and the random seed, and constructs parent.xml from that

parent_pdb = sys.argv[1]
seed = int(sys.argv[2])

pdb = PDBFile(parent_pdb)
forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

system = forcefield.createSystem(pdb.topology, nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
                             constraints=HBonds)
system.addForce(MonteCarloBarostat(1*bar, 300*kelvin))
integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)

integrator.setRandomNumberSeed(seed)

simulation = Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)

simulation.saveState('parent.xml')
