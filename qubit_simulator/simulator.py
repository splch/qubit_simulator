import numpy as np
import collections
from . import gates


class QubitSimulator:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state_vector = np.zeros(2**num_qubits, dtype=complex)
        self.state_vector[0] = 1

    def _apply_gate(self, gate, target, control=None):
        target_mask = 1 << (self.num_qubits - target - 1)
        for state in range(2**self.num_qubits):
            if control is None or (state & (1 << (self.num_qubits - control - 1))):
                if (state & target_mask) == 0:
                    target_state = state | target_mask
                    self.state_vector[state], self.state_vector[target_state] = gate @ [
                        self.state_vector[state],
                        self.state_vector[target_state],
                    ]

    def H(self, target):
        self._apply_gate(gates.H, target)

    def T(self, target):
        self._apply_gate(gates.T, target)

    def X(self, target):
        self._apply_gate(gates.X, target)

    def CNOT(self, control, target):
        self._apply_gate(gates.X, target, control)

    def U(self, target, theta, phi, lambda_):
        U = gates.U(theta, phi, lambda_)
        self._apply_gate(U, target)

    def CU(self, control, target, theta, phi, lambda_):
        U = gates.U(theta, phi, lambda_)
        self._apply_gate(U, target, control)

    def Measure(self, shots=1):
        probabilities = np.abs(self.state_vector) ** 2
        result = np.random.choice(2**self.num_qubits, p=probabilities, size=shots)
        return [format(r, f"0{self.num_qubits}b") for r in result]

    def run(self, shots=100):
        results = self.Measure(shots)
        return collections.Counter(results)
