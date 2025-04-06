import bcrypt

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Predefined users with their hashed passwords and roles
users = {
    "pavani@nmims.in": {
        "password": hash_password("1234"),
        "role": "coordinator"
    },
    "chandrakant@nmims.in": {
        "password": hash_password("1234"),
        "role": "schoolhead"
    },
    "vidyasagar@nmims.in": {
        "password": hash_password("1234"),
        "role": "faculty"
    },
    "wasiha@nmims.in": {
        "password": hash_password("1234"),
        "role": "faculty"
    },
    "vinayak@nmims.in": {
        "password": hash_password("1234"),
        "role": "faculty"
    }
    "sanjay@nmims.in": {
        "password": hash_password("1234"),
        "role": "faculty"
    }
}
