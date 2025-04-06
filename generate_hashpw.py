import bcrypt

passwords = ["1234"]  # Replace with actual passwords
for password in passwords:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(f"Hashed password: {hashed}")  # Copy this and store it in your code
