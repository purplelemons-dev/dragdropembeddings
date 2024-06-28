FROM node:20.10.0-bookworm-slim

RUN apt update -y && apt upgrade -y

WORKDIR /app

COPY package.json /app

RUN npm i

COPY . .

CMD ["npm", "run", "dev2"]
