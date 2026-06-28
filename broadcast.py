import sys
import hashlib
payload = sys.argv[1] if len(sys.argv) > 1 else "ORGANICS_OF_BIOHICSL_FLESH"
target = sys.argv[2] if len(sys.argv) > 2 else "neural_network"
print(f"📡 Broadcasting: {payload} to {target}")
hash_val = hashlib.sha256(payload.encode()).hexdigest()
print(f"🔑 Signature: {hash_val[:16]}...")
