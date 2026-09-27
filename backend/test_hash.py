from app.core.security import (
    get_password_hash,
    verify_password
)

password = "rahul123"

hashed = get_password_hash(password)

print("Original Password :", password)
print("Hashed Password   :", hashed)

print("Correct Password :", verify_password("rahul123", hashed))
print("Wrong Password   :", verify_password("wrongpassword", hashed))