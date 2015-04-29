#!/bin/sh

export ADMIN_TOKEN=0c97448e8aaed2a9bcc9
export AUTH_URL=http://localhost:35357/v3
# export AUTH_URL=http://localhost:5000/v3

# create project
# curl -si -H"X-Auth-Token:$ADMIN_TOKEN" -H "Content-type: application/json" "$AUTH_URL"/projects -d@playkeystone-project.json
# create user
# curl -si -H"X-Auth-Token:$ADMIN_TOKEN" -H "Content-type: application/json" "$AUTH_URL"/users -d@playks-user.json

curl -s -H"X-Auth-Token:$ADMIN_TOKEN" -H "Content-type: application/json" "$AUTH_URL"/users | python -mjson.tool
curl -s -H"X-Auth-Token:$ADMIN_TOKEN" -H "Content-type: application/json" "$AUTH_URL"/projects | python -mjson.tool
# curl -si -H"X-Auth-Token:$ADMIN_TOKEN" -H "Content-type: application/json" "$AUTH_URL"/users
# curl -si -H"X-Auth-Token:$ADMIN_TOKEN" -H "Content-type: application/json" "$AUTH_URL"/projects

