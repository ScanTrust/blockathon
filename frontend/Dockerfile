FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y curl build-essential nginx

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -y nodejs

WORKDIR /app

COPY package.json .

RUN npm install

ADD ./nginx.conf /etc/nginx/nginx.conf

COPY . .

RUN npm run build

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]