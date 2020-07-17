# flask-react-auth
Minimal example of using authentication with React in the front and Flask in the back.

# GNU Make targets

`make readme` runs the grip server at localhost:6419 to see README updates live (if port is in use it will exit).

`make backend` runs the flask dev server at localhost:5001 (if port is in use, it will exit).

`make frontend` runs the node create-react-app server at localhost:3001 (if port is in use, it will prompt to use the next port)

# Project structure

This project is split into two main parts, the Flask backend (Python3) in [./fra-back](./fra-back) and the React frontend (Javascript initialised with create-react-app) in [./fra-front](./fra-front). To learn more, view the README in either of those directories.

Additional to those main parts are the Python Virtual Environment `fra-venv` and a few other files.

# OAuth registrations

## Google

I visited the [Google API Console](https://console.developers.google.com/) to register the app. This first required me to request the permissions `resourcemanager.projects.get` and `serviceusage.services.list` in the 'project' domain.

On the API Console I went to "credentials", then created a new Client ID.
 - Application Type: Web application.
 - Name: fra-test-001
 - Authorised redirect URIs:
   - http://localhost:5001/login/google/authorized

This created the token:
 - Client ID: 67742121830-bvd5ab9j87180hg22mqgu8pk75rhba6p.apps.googleusercontent.com
 - Client Secret: SBxXnxT_oytQvATcaWmHduw1

I added these values to the the [Flask instance config file](./fra-back/instance/config.py) under the keys `GOOGLE_CLIENT_ID` and `GOOGLE_SECRET`

## Microsoft Azure

I went to `azure.portal.com` and logged in as `andrew.martin@fact360.co`, clicked through to Azure Active Directory. This is a Tenant with ID f8cdef31-a31e-4b4a-93e4-5f571e91255a. I registered an app called `fra-back` with a client id 38d63387-7cb0-4620-a539-e9849b5b8b33. When asked "Who can use this application or access this API?" I answered "Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)". I added the redirect url:
 - type: web
 - url: http://localhost:5001/login/azure/authorized

I then went to "certificates & secrets", and chose to add a new client secret:
 - Description: OAuth2 for Azure fra-back
 - Expires: Never

API Permissions were left at their default: Microsoft Graph -> User.Read.

I added branding:
 - name: fra-back,
 - home page url: http://localhost:5001
