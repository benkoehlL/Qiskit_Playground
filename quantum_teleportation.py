'''
This is a implementation of the quantum teleportation algorithm
'''

from qiskit import *
from qiskit.visualization import plot_histogram
import os, shutil
from matplotlib.pyplot import plot, draw, show

LaTex_folder_Quantum_Teleportation = str(os.getcwd())+'/Latex_quantum_gates/Quantum_Teleportation/'
if not os.path.exists(LaTex_folder_Quantum_Teleportation):
    os.makedirs(LaTex_folder_Quantum_Teleportation)
else:
    shutil.rmtree(LaTex_folder_Quantum_Teleportation)
    os.makedirs(LaTex_folder_Quantum_Teleportation)

qc = QuantumCircuit(3,3)
# teleport |1> use -> qc.x(0)
# teleport |0> + |1> use -> qc.x(0)

qc.barrier()
qc.h(1)
qc.cx(1,2)
qc.cx(0,1)
qc.h(0)
qc.barrier()
qc.measure([0,1],[0,1])
qc.barrier()
qc.cx(1,2)
qc.cz(0,2)
qc.measure(2,2)

LaTex_code = qc.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'quantum_teleportation.tex'
with open(LaTex_folder_Quantum_Teleportation+f_name, 'w') as f:
            f.write(LaTex_code)

# simulation
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=simulator, shots=100000).result()
counts = result.get_counts()
print(counts)
plt = plot_histogram(counts)
draw()
show(block=True)