#initialization
import matplotlib.pyplot as plt
import numpy as np

# importing Qiskit
from qiskit import *
from qiskit.providers.ibmq import least_busy

# import basic plot tools
from qiskit.visualization import plot_histogram

# Oracle circuit
oracle = QuantumCircuit(2,name='oracle')
oracle.cz(0,1)
oracle.to_gate()
oracle.draw()

# q_0: ─■─
#       │ 
# q_1: ─■─

# Reflection circuit
reflection = QuantumCircuit(2,name='reflection')
reflection.h([0,1]) # Hadamard
reflection.z([0,1])
reflection.cz(0,1)
reflection.h([0,1])
reflection.to_gate()
reflection.draw()

#      ┌───┐┌───┐   ┌───┐
# q_0: ┤ H ├┤ Z ├─■─┤ H ├
#      ├───┤├───┤ │ ├───┤
# q_1: ┤ H ├┤ Z ├─■─┤ H ├
#      └───┘└───┘   └───┘

grover_circuit = QuantumCircuit(2,2)
grover_circuit.h([0,1])
grover_circuit.append(oracle, [0,1])
grover_circuit.append(reflection, [0,1])
grover_circuit.measure([0,1], [0,1])
grover_circuit.draw()

#      ┌───┐┌─────────┐┌─────────────┐┌─┐   
# q_0: ┤ H ├┤0        ├┤0            ├┤M├───
#      ├───┤│  oracle ││  reflection │└╥┘┌─┐
# q_1: ┤ H ├┤1        ├┤1            ├─╫─┤M├
#      └───┘└─────────┘└─────────────┘ ║ └╥┘
# c: 2/════════════════════════════════╩══╩═
#                                     0  1 


token = "YOUR_TOKEN"
IBMQ.save_account(token)
provider = IBMQ.load_account()

device = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 3 and 
                                      not x.configuration().simulator and x.status().operational==True)


job = execute(grover_circuit, backend=device, shots=1)
plot_histogram(job.result().get_counts(), color='skyblue', title="").savefig('out.png')
