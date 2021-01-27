# Coffee Shop Full Stack

This is a full stack drink menu application using third-party authentication (AUTH0) and an api to provide the app with data.

## Functionalities

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

## Getting Started
## Frontend
### Installing Dependencies
#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI  is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Backend
### Installing Dependencies
From `Backend` directory run the command:

```pip install -r requirements.txt```

## Running The Server
### Frontend
From `Frontend` directory run the command:

```
ionic serve
```

### Backend
From `Backend/src` directory

Run the following when a new terminal is opened
```
export FLASK_APP=api
export FLASK_ENV=development

export AUTH0_DOMAIN='your_auth0_domain'
export API_AUDIENCE='auth0_audience'
```
Then run the server by running this command:
```
flask run
```
## Endpoints

### GET /drinks
* General: Return a list of all drinks with short description.
* Sample: `curl -X GET http://127.0.0.1:5000/drinks`
```
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

### GET /drinks-detail
* General: Return list of drinks with full description.
* Sample: `curl -X GET http://127.0.0.1:5000/drinks-detail`

```
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

### POST /drinks
* General: Create a new drink.
* Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Water4", "recipe": {"name": "Water", "color": "blue", "parts": 1}]}' http://127.0.0.1:5000/drinks
`
```
{
    "drinks": [
        {
            "id": 3,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water4"
        }
    ],
    "success": true
}
```

### PATCH /drinks/{id}
* General: Partially update a drink.
* Sample: `curl -X PATCH -d '{"title": "Water5"}' http://127.0.0.1:5000/drinks/3`

```
{
    "drinks": [
        {
            "id": 3,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```

### DELETE /drinks/{id}
* General: Delete a drink.
* Sample: `curl -X DELETE http://127.0.0.1:5000/drinks/3`

```
{
    "delete": 3,
    "success": true
}
```
