'''
This program sets up the Half Adder and the Full Adder and creates a .tex file
with the gate geometry. It also evaluates the result with a qasm quantum 
simulator
'''

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, \
                    execute, result, Aer
import os
import shutil

LaTex_folder_Adder_gates = str(os.getcwd())+'/Latex_quantum_gates/Adder-gates/'
if not os.path.exists(LaTex_folder_Adder_gates):
    os.makedirs(LaTex_folder_Adder_gates)
else:
    shutil.rmtree(LaTex_folder_Adder_gates)
    os.makedirs(LaTex_folder_Adder_gates)

qubit_space = ['0','1']

## define the previous logic gates
def AND(qc, q0, q1, q2):
    qc.reset(q2)
    qc.ccx(q0,q1,q2)

def OR(qc, q0, q1, q2):
    qc.reset(q2)
    qc.ccx(q0, q1, q2)
    qc.cx(q0,q2)
    qc.cx(q1,q2)

def XOR(qc, q0, q1, q2):
    qc.reset(q2)
    qc.cx(q0,q2)
    qc.cx(q1,q2)

def NOR(qc, q0, q1, q2):
    qc.reset(q2)
    qc.ccx(q0, q1, q2)
    qc.cx(q0,q2)
    qc.cx(q1,q2)
    qc.x(q2)

def Half_Adder(qc, q0, q1, qd):
    # This function carries out the addition with a carry bit cq
    # It also measures the minor bit q0 in the addition
    qc.ccx(q0,q1,qd)
    qc.cx(q1, q0)
    

def Full_Adder(qc, q1_0, q1_1, q1_2, q2_0, qd, c0):
    # carries out the addition of |q1_2 q1_1 q1_0> + |0 q2_0> and measures the
    Half_Adder(qc, q1_0, q2_0, qd)
    qc.measure(q1_0,c0)
    Half_Adder(qc, q1_1, qd, q1_2)
    

## Half Adder (my version)
# long version
'''
addend0 = '1' 
addend1 = '1'
q  = QuantumRegister(3, name = 'q')
c  = ClassicalRegister(2, name = 'c')
qc = QuantumCircuit(q,c)
for qubit in q:
    qc.reset(qubit)

# initialisation
if(addend0== '1'):
    qc.x(q[0])
if(addend1 == '1'):
    qc.x(q[1])

qc.ccx(q[0], q[1], q[2])
qc.cx(q[0], q[1])
qc.measure(q[1], c[0])
qc.measure(q[2], c[1])

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
results = job.result()
count = results.get_counts()
#print(count)
'''

## Half Adder (my version)
# short version
print("Test Half Adder",'\n')

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

        Half_Adder(qc, q[0],q[1],q[2])
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
Half_Adder(qc, q[0],q[1],q[2])
qc.measure(q[1], c[0])
qc.measure(q[2], c[1])

LaTex_code = qc.draw(output='latex_source',
                     justify=None) # draw the circuit
f_name = 'Half_Adder_gate_Benjamin.tex'
with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
            f.write(LaTex_code)

## Half Adder for two qubits (Beyond Classical book version)
q  = QuantumRegister(5, name = 'q')
c  = ClassicalRegister(2, name = 'c')
qc = QuantumCircuit(q,c)
addend0 = '1'
addend1 = '0'
# initialisation
if(addend0 == '1'):
    qc.x(q[0])
if(addend1 == '1'):
    qc.x(q[1])

XOR(qc, q[0],q[1],q[2])
qc.barrier(q)

AND(qc, q[0], q[1], q[3])
qc.barrier(q)

qc.measure(q[2], c[0])
qc.measure(q[3], c[1])

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
results = job.result()
count = results.get_counts()
#print(count)

LaTex_code = qc.draw(output='latex_source', justify=None) # draw the circuit
f_name = 'Half_Adder_gate_Beyond_Classical.tex'
with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
            f.write(LaTex_code)

## Full Adder for addition of a two-qubit |q1q2> and a one-qubit number |q3> 
## with a carry qubit |cq> which is initialised to |0>  
# iteration over all possible additions of |q1q2>+|q3>
'''
print('\n',"Full Adder Test (long version)")
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

            # determin and measure the least digit
            Half_Adder(qc, q1[2], q2[0], cq, c[0])
            
            # determine and measure the most significant digits
            qc.ccx(cq, q1[1], q1[0])
            qc.cx(cq, q1[1])
            
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
'''

## Full Adder for addition of a two-qubit |q1q2> and a one-qubit number |q3> 
## with a carry qubit |cq> which is initialised to |0>  
# iteration over all possible additions of |q1q2>+|q3>
print('\n',"Full Adder Test (short version)")
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

            Full_Adder(qc, q1[2], q1[1], q1[0], q2[0], cq, c[0])
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

## general adder
'''
print("General Adder")
for qubit2_2 in qubit_space:
    for qubit2_1 in qubit_space:
        for qubit1_3 in qubit_space:    
            for qubit1_2 in qubit_space:
                for qubit1_1 in qubit_space:
                    string_q1 = str(0)+str(qubit1_3)+str(qubit1_2)+str(qubit1_1)
                    string_q2 = str(qubit2_2)+str(qubit2_1)
                    q1  = QuantumRegister(len(string_q1), name ='q1')
                    q2  = QuantumRegister(len(string_q2), name = 'q2')
                    qd  = QuantumRegister(1, name = 'd')
                    c   = ClassicalRegister(len(string_q1)+1, name = 'c')
                    qc  = QuantumCircuit(q1,q2,cq,c)

                    for qubit in q1:
                        qc.reset(qubit)
                    for qubit in q2:
                        qc.reset(qubit)
                    
                    # initialise qubits which should be added
                    for i, qubit in enumerate(q1):
                        if(string_q1[i] == '1'):
                            qc.x(qubit)
                    for i, qubit in enumerate(q2):
                        if(string_q2[i] == '1'):
                            qc.x(qubit)
                    
                    Half_Adder(qc, q1[-1], q2[-1], qd)
                    qc.measure(q[-1], c[0])
                    Full_Adder(qc, q1[-1], q1[-2], q1[-3], q2[-2], qd, c[1], c[2])

                    for i in range(1,len(c)-1):
                        qc.measure(q1[-i], c[i])

                    # check the results
                    backend = Aer.get_backend('qasm_simulator')
                    job = execute(qc, backend, shots=1000)
                    results = job.result()
                    count = results.get_counts()
                    print('|0', qubit1_3, qubit1_2, qubit1_1, '>', '+', '|0', qubit2_2, qubit2_1, '> = ', '\t', count)
'''