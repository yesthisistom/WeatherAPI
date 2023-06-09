## Sample Rest API 

A basic Rest API using FastAPI.  It will return the hourly weather or a clothing recommendation
 based on the requested city (United States only).

## Building

### Docker
This app is dockerized. To build and deploy using docker, run the following commands  

```
docker-compose build
docker-compose up -d
``` 

### Python

If you have a local python install, you can run it from python directly.  The required libraries are found in 
requirements.txt. It was developed on python 3.7, and tested up to 3.9. 
Once required libraries are installed, you can start it up running

```
uvicorn WeatherRestAPI:app --port 4001
```

## Using

To ensure the app is running, you can open up a brower, and navigate to `http://localhost:4001`.  
You should see a message "Weather Rest API is up and running"

To test using curl:

```
curl "http://localhost:4001/clothing_req/?city=Alexandria&state=Virginia"
curl "http://localhost:4001/hourly/?city=Alexandria&state=Virginia"
```

## Basic Documentation

To see the auto-generated documentation, visit

```http://localhost:4001/docs```

## Air Quality Index

To have the air quality index used for the clothing recommendation, get a token from waqi.info to use their 
Rest API, and put it in the .env file (uncomment the line for WAQI_TOKEN).
