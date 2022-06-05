# weather Application

*   This is a django application written in python to show current weather for any city in world, 
using API from openweathermap.org. 

*   App UI and data support 3 languages
       *   English
       *   German
       *   French

*   App shows below details for requested city
       *   City : Hyderabad IN
       *   Temperature : 32.23°C
       *   Min Temperature : 32.23°C
       *   Max Temperature : 35.73°C
       *   Humidity : 35%
       *   Pressure : 1005N/m2
       *   Wind Speed : 6.17m/s
       *   Wind Direction : NNE
       *   Description : broken clouds

*   This app is powered by docker-compose which consists of two services
      1) Web (django application micro service built using Dockerfile)
      2) redis (redis micro service run from Docker image)

*   App can be made running using below command(prerequisites: docker, docker-compose):
      *   DESKTOP-HECTSJ9:~/weather_application_django/weatherproject$ **docker-compose up**
      *   To be checked in browser using http://127.0.0.1:9091/

*   Redis cache timeout value, Port number for running application are configurable using 
docker-compose.yaml file

