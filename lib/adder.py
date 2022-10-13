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