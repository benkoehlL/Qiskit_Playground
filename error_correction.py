import os, shutil
from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit.visualization import circuit_drawer as drawer
import numpy as np
from matplotlib.pyplot import draw, plot, show

LaTex_folder_Error_Correction = str(os.getcwd())+'/Latex_quantum_gates/Error_Correction/'
if not os.path.exists(LaTex_folder_Error_Correction):
    os.makedirs(LaTex_folder_Error_Correction)
else:
    shutil.rmtree(LaTex_folder_Error_Correction)
    os.makedirs(LaTex_folder_Error_Correction)

def ERROR_X(circuit, q):
    if(np.random.rand()<0.2):
        circuit.x(q)

def ERROR_Y(circuit, q):
    if(np.random.rand()<0.2):
        circuit.y(q)

def ERROR_Z(circuit, q):
    if(np.random.rand()<0.2):
        circuit.z(q)

def Error_CX_Gate(circuit, q):
    circuit.cx(q[0],q[1])
    ran = np.random.rand()
    if(ran < 1/3):
        ERROR_X(circuit, q[0])
    elif(ran < 2/3):
        ERROR_Y(circuit, q[0])
    else:
        ERROR_Z(circuit, q[0])
    
    ran = np.random.rand()
    if(ran < 1/3):
        ERROR_X(circuit, q[1])
    elif(ran < 2/3):
        ERROR_Y(circuit, q[1])
    else:
        ERROR_Z(circuit, q[1])
    
def Shor_error_correction(Circuit_FUNC, qr, qr_Shor):
    # This function creates the Shor error correction circuit
    # for a error-prone function Circuit_FUNC and its related
    # qubit(s) qr (qr_Shor are the ancilla qubits)
    # it returns this error corrected circuit
    
    qc_preprocess = QuantumCircuit(qr, qr_Shor)
    for i, qubit in enumerate(qr):
        qc_preprocess.cx(qubit, qr_Shor[8*i+2])
        qc_preprocess.cx(qubit, qr_Shor[8*i+5])
        
        qc_preprocess.h(qubit)
        qc_preprocess.h(qr_Shor[8*i+2])
        qc_preprocess.h(qr_Shor[8*i+5])
        
        qc_preprocess.cx(qubit, qr_Shor[8*i])
        qc_preprocess.cx(qubit, qr_Shor[8*i+1])
        qc_preprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+3])
        qc_preprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+4])
        qc_preprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+6])
        qc_preprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+7])
        #qc_preprocess.barrier()
    qc_preprocess.barrier()
    qc = qc_preprocess

    # apply main function (with possible errors) to qr 
    # and the error ancilla qubits
    Circuit_FUNC(qc, qr)
    for j in range(8):
        Circuit_FUNC(qc, qr_Shor[j:j+8*len(qr):8])
    qc.barrier()

    qc_postprocess = QuantumCircuit(qr,qr_Shor)
    for i, qubit in enumerate(qr):
        qc_postprocess.cx(qubit, qr_Shor[8*i])
        qc_postprocess.cx(qubit, qr_Shor[8*i+1])
        qc_postprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+3])
        qc_postprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+4])
        qc_postprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+6])
        qc_postprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+7])
        
        qc_postprocess.ccx(qr_Shor[8*i], qr_Shor[8*i+1], qubit)
        qc_postprocess.ccx(qr_Shor[8*i+3], qr_Shor[8*i+4], qr_Shor[8*i+2])
        qc_postprocess.ccx(qr_Shor[8*i+6], qr_Shor[8*i+7], qr_Shor[8*i+5])

        qc_postprocess.h(qubit)
        qc_postprocess.h(qr_Shor[8*i+2])
        qc_postprocess.h(qr_Shor[8*i+5])

        qc_postprocess.cx(qubit, qr_Shor[8*i+2])
        qc_postprocess.cx(qubit, qr_Shor[8*i+5])
        qc_postprocess.ccx(qubit, qr_Shor[8*i+2], qr_Shor[8*i+5])

        #qc_postprocess.barrier()
    
    qc = QuantumCircuit.compose(qc, qc_postprocess)


    return qc

## X-Error
for qubit in [0, 1]:
    print("|",qubit,'> : ',end='')
    q = QuantumRegister(1,'q')
    q_Shor = QuantumRegister(8*len(q),'q_shor')
    c = ClassicalRegister(len(q), 'c')
    qc = QuantumCircuit(q,q_Shor, c)
    if(qubit):
        qc.x(q)
    qc_Shor = Shor_error_correction(ERROR_X, q, q_Shor)
    qc_Shor.barrier()
    qc_Shor = QuantumCircuit.compose(qc, qc_Shor)

    LaTex_code = qc_Shor.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
    f_name = 'Shor_error_correction_XERROR.tex'
    with open(LaTex_folder_Error_Correction+f_name, 'w') as f:
                f.write(LaTex_code)

    qc_Shor.measure(q, c)

    # evaluate result
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc_Shor, backend=simulator, shots=1000).result()
    counts = result.get_counts()
    print(counts)

## Y-Error
for qubit in [0, 1]:
    print("|",qubit,'> : ', end='')
    q = QuantumRegister(1,'q')
    q_Shor = QuantumRegister(8*len(q),'q_shor')
    c = ClassicalRegister(len(q), 'c')
    qc = QuantumCircuit(q,q_Shor, c)
    if(qubit):
        qc.x(q)
    qc_Shor = Shor_error_correction(ERROR_Y, q, q_Shor) 
    qc_Shor.barrier()
    qc_Shor = QuantumCircuit.compose(qc, qc_Shor)

    LaTex_code = qc_Shor.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
    f_name = 'Shor_error_correction_YERROR.tex'
    with open(LaTex_folder_Error_Correction+f_name, 'w') as f:
                f.write(LaTex_code)

    qc_Shor.measure(q, c)

    # evaluate result
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc_Shor, backend=simulator, shots=1000).result()
    counts = result.get_counts()
    print(counts)

## Z-Error
for qubit in [0, 1]:
    print("|",qubit,'> : ',end='')
    q = QuantumRegister(1,'q')
    q_Shor = QuantumRegister(8*len(q),'q_shor')
    c = ClassicalRegister(len(q), 'c')
    qc = QuantumCircuit(q,q_Shor, c)
    if(qubit):
        qc.x(q)
    qc_Shor = Shor_error_correction(ERROR_Z, q, q_Shor) 
    qc_Shor.barrier()
    qc_Shor = QuantumCircuit.compose(qc, qc_Shor)

    LaTex_code = qc_Shor.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
    f_name = 'Shor_error_correction_ZERROR.tex'
    with open(LaTex_folder_Error_Correction+f_name, 'w') as f:
                f.write(LaTex_code)

    qc_Shor.measure(q, c)

    # evaluate result
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc_Shor, backend=simulator, shots=1000).result()
    counts = result.get_counts()
    print(counts)

## All three errors possible in CX-gate
for qubit1 in [0, 1]:
    for qubit2 in [0, 1]:
        print("|",qubit1,qubit2,'> : ',end='')
        q = QuantumRegister(2,'q')
        c = ClassicalRegister(len(q), 'c')
        q_Shor = QuantumRegister(8*len(q),'q_shor')
        qc = QuantumCircuit(q, q_Shor, c)
        
        if(qubit1):
            qc.x(q[0])
        if(qubit2):
            qc.x(q[1])
        qc.barrier()
        qc_Shor = Shor_error_correction(Error_CX_Gate, q, q_Shor)
        qc_Shor.barrier()

        qc_Shor = QuantumCircuit.compose(qc, qc_Shor)
        qc_Shor.measure(q, c)

        # evaluate result
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc_Shor, backend=simulator, shots=1000).result()
        counts = result.get_counts()
        print(counts)