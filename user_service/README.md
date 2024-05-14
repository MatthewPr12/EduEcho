PostgreSQL-based service that manages user authorization.

## Endpoints
### POST: `/login`
Takes in [UserCredentials](./user_credentials.py). Returns whether the authorization was successful.

### POST: `/signup`
Takes in [UserCredentials](./user_credentials.py), and, optionally, faculty and program.
Fails if the login is already taken.



