from qiskit import *

print("GHZ")
c2 = QuantumCircuit(3,3)
c2.h(0)
c2.h(1)
c2.ccz(0,1,2)
c2.x(2)
c2.ccz(0,1,2)
c2.x(2)
c2.h(1)
c2.h(2)
c2.ccz(0,1,2)
c2.h(2)
c2.measure([i for i in range(3)], [i for i in range(3)])
simulator = Aer.get_backend('qasm_simulator')
result = execute(c2, backend=simulator, shots=1000).result()
answer = result.get_counts()
print(answer)