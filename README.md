# SPOTIFY GPT APP

## TODO

# Priority

# Backlog
* frontend
npm start


* Understand how you will manage state, auth, user
    * User will come from the frontend
* For now - cookies. Transition into firestore for future cases

* Endpoint to login
* Endpoint fall callback
* Endpoint to logout
* Endpoint retrieve


* Implement poetry make command to create requirements txt
* Transition into mono repo
* Backend FastAPi
* Frontend React/typescdript


Sample process

1.
http://localhost:5000/login

Initial login request
* Generates a auth object
    - has redirect url
    - has state

Hold auths[state] = auth * so we know which auth object were are using given a state


2. Once authorise on redirect link
This validates the auth object

By equating the states, you can find the authenticated auth object

Use validated auth object to generate access token


3. Perform a request on playlist route
Only needs an access token
Create a Spotify client object with the user's access token
Requests data
    