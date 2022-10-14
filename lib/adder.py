def Half_Adder(qc, q1, q2, qd):
    # This function carries out the addition |q0> + |q1> 
    # storing the minor bit in q2 with a carry bit qd
    qc.ccx(q1,q2,qd)
    qc.cx(q1, q2)
    

def Full_Adder(qc, q1, q2, qd, q0, c0):
    # carries out the addition of |q1> + |q2> + |qd> 
    # it measures the minor bit and stores it in c0 
    # and uses the bit |q0> (reset to |0> at the beginning) 
    # to store the carry bit  
    qc.reset(q0)
    Half_Adder(qc, q1, q2, q0)
    Half_Adder(qc, q2, qd, q0)
    qc.measure(qd,c0)