import numpy as np
import hashlib
import random
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import orkes
from orkes import Task, Workflow
class QuantumEncryption:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')
    
    def generate_quantum_key(self, length=16):
        qc = QuantumCircuit(length, length)
        qc.h(range(length)) 
        qc.measure(range(length), range(length))
        
        job = execute(qc, self.backend, shots=1)
        result = job.result().get_counts()
        key = list(result.keys())[0]
        return key
    
    def encrypt(self, data, key):
        hashed_data = hashlib.sha256(data.encode()).hexdigest()
        encrypted_data = ''.join(chr(ord(c) ^ int(k)) for c, k in zip(hashed_data, key))
        return encrypted_data
    
    def decrypt(self, encrypted_data, key):
        decrypted_data = ''.join(chr(ord(c) ^ int(k)) for c, k in zip(encrypted_data, key))
        return decrypted_data

class BiofeedbackAuthOrkes:
    def __init__(self):
        self.qe = QuantumEncryption()
        self.biometric_data = None
    
    def capture_biofeedback(self):
        heartbeat = random.uniform(60, 100)
        brainwave = random.uniform(0.1, 30.0)
        return f"HB:{heartbeat:.2f}|BW:{brainwave:.2f}"

    def authenticate(self, biofeedback):
        key = self.qe.generate_quantum_key()
        encrypted_feedback = self.qe.encrypt(biofeedback, key)
        return encrypted_feedback, key

# This is to create Orkes Tasks for each operation in the code
class OrkesBiofeedbackWorkflow(Workflow):
    @Task
    def capture_biofeedback(self):
        return BiofeedbackAuthOrkes().capture_biofeedback()

    @Task
    def authenticate(self, biofeedback):
        return BiofeedbackAuthOrkes().authenticate(biofeedback)

# Then we will run the Orkes Workflow
workflow = OrkesBiofeedbackWorkflow()
biofeedback_data = workflow.capture_biofeedback()
encrypted_data, key = workflow.authenticate(biofeedback_data)

print(f"Captured Biofeedback: {biofeedback_data}")
print(f"Encrypted Data: {encrypted_data}")
print(f"Quantum Key: {key}")
