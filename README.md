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

    POST /api/oauth2/access_token/
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
        email: "matteo@dyanote.com",
        password: "..."
    }

Verification mail is sent.

    POST /api/users/matteo@dyanote.com/
    {
        verification_code: "..."
    }

User is now activated.

#### Resource

    GET /api/users/matteo@dyanote.com/
Returns

    {
        "url": "https://api.dyanote.com/api/users/matteo@dyanote.com/", 
        "username": "matteo@dyanote.com", 
        "email": "matteo@dyanote.com", 
        "pages": "https://api.dyanote.com/api/users/matteo@dyanote.com/pages/",
        
        "logout": "https://api.dyanote.com/api/users/matteo@dyanote.com/logout/",
        "change_password": "https://api.dyanote.com/api/users/matteo@dyanote.com/change_password/",
        "change_password": "https://api.dyanote.com/api/users/matteo@dyanote.com/send_password_reset/",
    }

#### Logout

    POST https://api.dyanote.com/api/users/matteo@dyanote.com/logout/

#### Change password

    POST https://api.dyanote.com/api/users/matteo@dyanote.com/change_password/
    {
        old: "old password or password reset code",
        new: "new password"
    }

If the user forgot the password

    POST https://api.dyanote.com/api/users/matteo@dyanote.com/send_password_reset/

Will mail him a reset code.



### Note resource

## Implementation

[Django REST framework](http://www.django-rest-framework.org/) was used to make the REST API implementation simpler and shorter.