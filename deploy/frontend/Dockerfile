FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install -g @vue/cli@5.0.8
#RUN npm install -g http-server


COPY ./frontend/package*.json ./
RUN npm install

COPY ./frontend ./

RUN npm run build
