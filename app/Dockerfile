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

# TODO unfortunately it's not possible to set the context path dynamically before run time
#  maybe it can be solved with a hook https://nuxtjs.org/docs/2.x/configuration-glossary/configuration-hooks#redirect-to-routerbase-when-not-on-root
#  another option would be to build the image via docker-compose befor starting and injecting the context path variable
ENV APP_CONTEXT_PATH="/app/"

COPY . .
EXPOSE 3000

RUN npm run build

CMD [ "npm", "run", "start" ]

