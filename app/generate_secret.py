import secrets

# Generate a 32-byte (256-bit) random string
jwt_secret = secrets.token_hex(32)
print(f"Your JWT secret: {jwt_secret}")

refresh_secret = secrets.token_hex(32)
print(f"Your REFRESH_token_Secret: {refresh_secret}")