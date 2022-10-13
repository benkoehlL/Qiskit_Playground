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
