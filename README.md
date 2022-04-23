# Simple project with Django DjangoChannel WebSocket Jwt Vue3/Vuex4 ...
# Backend

## Django project (with Django channels)

### run server in development
> - virtualenv -p python3 venv
> - source /venv/bin/activate
> - pip install -r requiremnts.txt
> - python /manage.py migrate
> - python /manage.py runserver

admin can create a group(all , admin created by default)
users can joind a new group
admin create a notification for a group it send with django channel and receive with Websocket (in vanilla js) or receive in frontend

### Api
login/logout/register a user
authentication with JWT ( [dj_rest_auth](https://dj-rest-auth.readthedocs.io) )

---
# FrontEnd

## Vue 3 project (with REST API)

### Compiles and hot-reloads for development
> npm run serve

### APIs
* register user ``` /api/auth/register/ ```
* login user ``` /api/auth/login/ ```
* logout user ``` /api/auth/logout/ ```
* refresh token ``` /api/auth/token/refresh/ ```

### Tokens
### use [jwt](https://dj-rest-auth.readthedocs.io) in server side
> - get AccessToken & RefreshToken when user logged in 
> - get new AccessToken with RefreshToken every few minutes
> - set Tokens in Cookie-HttpOnly **(javascript cat reach tokens for protect against XSS vulnerability)**

### Socket
1. open a WebSocket for geting new Notifications (store notificatios in Localstorage) ``` ws://{host}/ws/notification/ ```

2. chat with other users by Socket (use DjangoChannels) ``` ws://{host}/ws/chat/{User}/ ```

