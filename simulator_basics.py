from qiskit import Aer, execute, QuantumRegister, ClassicalRegister,\
                    QuantumCircuit

# list all the available simulation environments
for backend in Aer.backends():
    print(backend.name())
    if(backend.name() == 'pulse_simulator'
    or backend.name() == 'statevector_simulator'):
        print("I do not know how to deal with this yet :)")
    else:
        # load a arbitrary quantum circuit of your choice (here Bell state preparation)
        for not0 in [False,True]:
            for not1 in [False,True]:
                print(not0, '\t', not1,'\t', end='')
                qr = QuantumRegister(2,name='q')
                cr = ClassicalRegister(2, name='c')
                qc = QuantumCircuit(qr, cr) 
                if(not0):
                    qc.x(qr[0])
                if(not1):
                    qc.x(qr[1])
                qc.h(qr[0]) 
                qc.cx(qr[0],qr[1]) 
                if(backend.name() != 'aer_simulator_unitary'
                and backend.name() != 'aer_simulator_superop'
                and backend.name() != 'unitary_simulator'):
                    qc.measure(qr,cr)
            
                job = execute(qc, backend, shots=1000)
                result = job.result()
                if(backend.name() != 'aer_simulator_unitary'
                and backend.name() != 'aer_simulator_superop'
                and backend.name() != 'unitary_simulator'):
                    count = result.get_counts()
                    print(count) 