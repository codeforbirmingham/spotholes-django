# Spotholes

Spotholes is a pothole tracking app, designed to allow city dwellers to more efficiently locate potholes.

## Authentication Endpoints

### /api/v1/accounts/

GET:

Return a paginated list of accounts

POST: {email: email,username:username, password:password}

Create a new account

### /api/v1/accounts/username/

GET:

Return data of account with same username

PATCH: {username: username, email:email, password:password}

Update username, email, or password or all. Only account owner or moderator has these permissions.

### /api/v1/accounts/username/status/

POST: {is_staff: (true/false), is_active:(true/false)}

Update a users permissions and active status. Only moderator has these permissions.

### /api/v1/accounts/reset-password/

POST: {email: email}

Request an email with instructions to update password.

### /api/v1/accounts/reset/uib64/token/

POST: {password:password, confirm_password:password}

Update password when forgotten.


### /api/v1/accounts/username/potholes/

GET: 

Return a list of this user's potholes

## Pothole Endpoints

### /api/v1/potholes/

GET:

Return paginated list of potholes

POST: {name:name, longitude:longitude, latitude:latitude, photo:photo}

Create a new pothole

### /api/v1/potholes/id/

GET:

Return specific pothole with the matching id

PUT:

Update entire instance
(requires owner or moderator status)


PATCH:

Partially update instance
(requires owner or moderator status)

DELETE:

Delete instance
(requires owner or moderator status)

### /api/v1/potholes/id/vote/

GET:

Return a list of votes associated with instance with matching id

POST:

{"score": (-1/1)}

### /api/v1/potholes/id/reports/

GET:

Return a list of reports associated with instance matching id

POST:

{comment:comment (<= 4000 chars)}
Create a report.

### /api/v1/potholes/id/reports/id/

GET:

Get a specific report

PATCH:

Update a report




