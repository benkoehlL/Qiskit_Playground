'''
This program sets up the Half Adder and the Full Adder and creates a .tex file
with the gate geometry. It also evaluates the result with a qasm quantum 
simulator
'''

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, \
                    execute, result, Aer
import os
import shutil
import lib.adder as adder
import lib.quantum_logic as logic

LaTex_folder_Adder_gates = str(os.getcwd())+'/Latex_quantum_gates/Adder-gates/'
if not os.path.exists(LaTex_folder_Adder_gates):
    os.makedirs(LaTex_folder_Adder_gates)
else:
    shutil.rmtree(LaTex_folder_Adder_gates)
    os.makedirs(LaTex_folder_Adder_gates)

qubit_space = ['0','1']
    
## Half Adder (my version)
print("Test Half Adder (my version",'\n')

for add0 in qubit_space: # loop over all possible additions
    for add1 in qubit_space:            
        q  = QuantumRegister(3, name = 'q')
        c  = ClassicalRegister(2, name = 'c')
        qc = QuantumCircuit(q,c)
        for qubit in q:
            qc.reset(qubit)

        # initialisation
        if(add0== '1'):
            qc.x(q[0])
        if(add1 == '1'):
            qc.x(q[1])

        adder.Half_Adder(qc, q[0],q[1],q[2])
        qc.measure(q[0], c[0])
        qc.measure(q[2], c[1])

        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1000)
        results = job.result()
        count = results.get_counts()
        print('|0', add0, '>', '+', '|0', add1, '>', '\t', count)

## Plot a sketch of the gate
q  = QuantumRegister(3, name = 'q')
c  = ClassicalRegister(2, name = 'c')
qc = QuantumCircuit(q,c)

qc.reset(q[2])
adder.Half_Adder(qc, q[0],q[1],q[2])
qc.measure(q[1], c[0])
qc.measure(q[2], c[1])

LaTex_code = qc.draw(output='latex_source',
                     justify=None) # draw the circuit
f_name = 'Half_Adder_gate_Benjamin.tex'
with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
            f.write(LaTex_code)

## Half Adder for two qubits (Beyond Classical book version)
print("Test Half Adder Beyond Classical")
for add0 in qubit_space: # loop over all possible additions
    for add1 in qubit_space:  
        q  = QuantumRegister(5, name = 'q')
        c  = ClassicalRegister(2, name = 'c')
        qc = QuantumCircuit(q,c)
        
        # initialisation
        if(add0 == '1'):
            qc.x(q[0])
        if(add1 == '1'):
            qc.x(q[1])

        logic.XOR(qc, q[0],q[1],q[2])
        qc.barrier(q)

        logic.AND(qc, q[0], q[1], q[3])
        qc.barrier(q)

        qc.measure(q[2], c[0])
        qc.measure(q[3], c[1])

        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1000)
        results = job.result()
        count = results.get_counts()
        print('|0', add0, '>', '+', '|0', add1, '>', '\t', count)
        if(add0=='0' and add1=='1'):
            LaTex_code = qc.draw(output='latex_source', justify=None) # draw the circuit
            f_name = 'Half_Adder_gate_Beyond_Classical.tex'
            with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
                        f.write(LaTex_code)

## Full Adder for addition of a two-qubit |q1q2> and a one-qubit number |q3> 
## with a carry qubit |cq> which is initialised to |0>  
# iteration over all possible additions of |q1q2>+|q3>
print('\n',"Full Adder Test (my version)")
for qubit2_1 in qubit_space:
    for qubit1_2 in qubit_space:
        for qubit1_1 in qubit_space:
            string_q1 = str(0)+str(qubit1_2)+str(qubit1_1)
            string_q2 = str(qubit2_1)
            q1  = QuantumRegister(3, name ='q1')
            q2  = QuantumRegister(1, name = 'q2')
            cq  = QuantumRegister(1, name = 'd')
            c   = ClassicalRegister(3, name = 'c')
            qc  = QuantumCircuit(q1,q2,cq,c)

            for qubit in q1:
                qc.reset(qubit)
            for qubit in q2:
                qc.reset(qubit)

            # initialise qubits which should be added
            for i, qubit in enumerate(q1):
                if(string_q1[i] == '1'):
                    qc.x(qubit)
                    print(1,end="")
                else:
                    print(0,end="")
            print('\t',end="")
            for i, qubit in enumerate(q2):
                if(string_q2[i] == '1'):
                    qc.x(qubit)
                    print(1,end="")
                else:
                    print(0,end="")
            print('\t',end="")

            adder.Full_Adder(qc, q1[2], q1[1], q1[0], q2[0], cq, c[0])
            qc.measure(q1[1], c[1])
            qc.measure(q1[0], c[2])
            
            # check the results
            backend = Aer.get_backend('qasm_simulator')
            job = execute(qc, backend, shots=1000)
            results = job.result()
            count = results.get_counts()
            print('|0', qubit1_2, qubit1_1, '>', '+', '|0', qubit2_1, '> = ', '\t', count)
            LaTex_code = qc.draw(output='latex_source') # draw the circuit
            if(qubit1_1 == '0' and qubit1_2 == '0' and qubit2_1 == '0'):
                f_name = 'Full_Adder_gate_Benjamin.tex'
                with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
                            f.write(LaTex_code)