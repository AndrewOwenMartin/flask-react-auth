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
