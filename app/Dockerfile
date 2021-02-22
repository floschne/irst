FROM node:14
MAINTAINER Florian Schneider "florian.schneider.1992@gmx.de"

WORKDIR /usr/src/app

COPY package.json ./
RUN npm install

# Make sure those variables get set before starting the app
# (in most cases in docker-compose.yml / .env)
#ENV APP_DEPLOY="docker"
#ENV API_HOST="study_api"
#ENV API_PORT="80"

COPY . .
EXPOSE 3000

RUN npm run build

CMD [ "npm", "run", "start" ]

