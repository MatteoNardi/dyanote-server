dyanote
=======

Dyanote is an hypertext-based note-taking application and this is the server side.


## API

The server side consists of a REST API which currently can be accessed at the following urls:

  https://dyanote.herokuapp.com/  
  https://api.dyanote.com/
  

### Login

We use OAuth2 for authenticating.
Login with an URL encoded post request to:

    POST /api/users/user@example.com/login/
        ?client_id=CLIENT_ID          // Client ID
        &client_secret=CLIENT_SECRET  // Client Secret
        &grant_type=password
        &username=USERNAME // Email of the user to login
        &password=PASSWORD // Password of the user

    -> { data: {..., access_token: "This is the token you'll need to use in every request"} }


At the time of writing, the javascript client on dyanote.com uses the following credentials:
   
   Client ID: edfd9c435154a6f75673  
   Client Secret: cf3aba97518712959062b52dc5c524dd4f6741bd

If your application is going to be used much, please contact me (I'll create new credentials for you)

### Access to protected resources

All requests requiring authentication will need the following HTTP header:

    Authorization: Bearer <token>

### User resource

#### Registration

    POST /api/users
    {
        email: "user@example.com",
        password: "..."
    }

Verification mail is sent.

    POST /api/users/user@example.com/
    {
        verification_code: "..."
    }

User is now activated.

#### Resource

    GET /api/users/user@example.com/
Returns

    {
        "url": "https://api.dyanote.com/api/users/user@example.com/", 
        "username": "user@example.com", 
        "email": "user@example.com", 
        "pages": "https://api.dyanote.com/api/users/user@example.com/pages/",
        
        "logout": "https://api.dyanote.com/api/users/user@example.com/logout/",
        "change_password": "https://api.dyanote.com/api/users/user@example.com/change_password/",
        "change_password": "https://api.dyanote.com/api/users/user@example.com/send_password_reset/",
    }

#### Logout

    POST https://api.dyanote.com/api/users/user@example.com/logout/

#### Change password

    POST https://api.dyanote.com/api/users/user@example.com/password/
    {
        old: "old password or password reset code",
        new: "new password"
    }

If the user forgot the password

    DELETE https://api.dyanote.com/api/users/user@example.com/password/

Will mail him a reset code.



### Note resource

## Implementation

[Django REST framework](http://www.django-rest-framework.org/) was used to make the REST API implementation simpler and shorter.