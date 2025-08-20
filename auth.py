from argon2 import PasswordHasher, exceptions


ph = PasswordHasher(
    time_cost=3,          # iteraciones
    memory_cost=64 * 1024, # 64 MB
    parallelism=2,
    hash_len=32
)

def hash_password(password: str) -> str:
    
    return ph.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    
    try:
        return ph.verify(hashed, password)
    except (exceptions.VerifyMismatchError, exceptions.VerificationError, exceptions.InvalidHash):
        return False

def needs_rehash(hashed: str) -> bool:
    
    try:
        return ph.check_needs_rehash(hashed)
    except Exception:
        return True
