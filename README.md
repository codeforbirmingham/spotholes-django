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




