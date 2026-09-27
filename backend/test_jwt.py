from app.core.auth import create_access_token

token = create_access_token(
    {
        "sub": "1",
        "email": "rahul@gmail.com",
        "role": "Admin"
    }
)

print(token)