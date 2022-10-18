from qiskit import *
from matplotlib.pyplot import draw, plot, show

def X(q):
    circuit = QuantumCircuit(q)
    circuit.x(q)
    return circuit


def Shor_error_correction(
    Circuit_FUNC, # the function creating the circuit 
                  # that is prone to produce an error
    qr            # the qubits that are affected by above circuit
):
    qr_Shor = QuantumRegister(8*len(qr),'q_Shor')
    qc_preprocess = QuantumCircuit(qr,qr_Shor)
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
    qc = QuantumCircuit.compose(qc_preprocess, Circuit_FUNC(QuantumRegister(len(qr)+len(qr_Shor))))
    qc.barrier()

    
    '''Does not work yet
    for i, qubit in enumerate(qr):
        for j in range(8):
            qc = QuantumCircuit.compose(qc,Circuit_FUNC(qr_Shor[8*i+j]))
    '''

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

q = QuantumRegister(1,'q')
qc = QuantumCircuit(q)
qc_Shore = Shor_error_correction(X, q) 

qc_Shore.draw(output='mpl')
draw()
show(block=True)
        
