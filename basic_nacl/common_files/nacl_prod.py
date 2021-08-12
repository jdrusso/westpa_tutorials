from simtk.openmm.app import * # PDBFile, ForceField, PME, HBonds, Simulation
from simtk.openmm import * #MonteCarloBarostat, LangevinIntegrator
from simtk.unit import * #picoseconds, picosecond, nanometer, kelvin, bar
from sys import stdout
import sys

pdb = PDBFile('bstate.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

system = forcefield.createSystem(pdb.topology, nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
                             constraints=HBonds)
system.addForce(MonteCarloBarostat(1*bar, 300*kelvin))
integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
integrator.setRandomNumberSeed(RAND)

simulation = Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)

# ### This block is no longer necessary, since I added pdb_to_xml to create the XML state files.
# This should load up the positions as well, overwriting positions that were set above
# try:
#     simulation.loadState('parent.xml')
# except OSError:
#     # This is a new segment, not a continuation, so no state to load
#     pass
simulation.loadState('parent.xml')
simulation.reporters.append(StateDataReporter('seg.log', 25, step=True, potentialEnergy=True, kineticEnergy=True, temperature=True)) 
simulation.reporters.append(DCDReporter('seg.dcd', 250)) 
simulation.step(250)
simulation.saveState('seg.xml')
