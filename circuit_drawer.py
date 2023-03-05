from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np
from matplotlib.pyplot import draw, plot, show
import os
import shutil

LaTex_folder = str(os.getcwd())+'/Latex_quantum_gates/circuits/'
if not os.path.exists(LaTex_folder):
    os.makedirs(LaTex_folder)

## A decomposition of the CU(theta,phi,lambda, alpha)
qr = QuantumRegister(2,name='q') 
circuit = QuantumCircuit(qr)
circuit.rz(np.pi/2,qr[1])  # angle (lambda+pi)/2
circuit.cx(qr[0],qr[1])
circuit.rz(-np.pi/2,qr[1]) # angle -(lambda+pi)/2
circuit.ry(np.pi/4,qr[1])  # angle theta/2
circuit.cx(qr[0],qr[1])
circuit.ry(-np.pi/4,qr[1]) # angle -theta/2
circuit.rz(np.pi/8,qr[1])  # angle (phi+pi)/2
circuit.cx(qr[0],qr[1])  
circuit.rz(-np.pi/8,qr[1]) # angle -(phi+pi)/2
circuit.cx(qr[0],qr[1])

# global phase gate to target qubit
circuit.x[qr[1]]
circuit.u(0,0,np.pi/16,qr[1]) # angle alpha
circuit.x[qr[1]]
circuit.u(0,0,np.pi/16,qr[1]) # angle alpha

LaTex_code = circuit.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'CU_Gate.tex'
with open(LaTex_folder+f_name, 'w') as f:
            f.write(LaTex_code)

circuit = QuantumCircuit(qr)
circuit.cu(np.pi/4,np.pi/8,np.pi/2,np.pi/16,qr[0],qr[1])
LaTex_code = circuit.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'CU_Gate_compact.tex'
with open(LaTex_folder+f_name, 'w') as f:
            f.write(LaTex_code)