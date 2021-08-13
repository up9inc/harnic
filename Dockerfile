# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY setup.py .

# install dependencies

RUN pip install -r requirements.txt
RUN pip install -e .

# copy the content of the local src directory to the working directory
#COPY . .
#
#
#FROM node:13.12.0-alpine as build
#
#ENV PATH /harnic-spa/node_modules/.bin:$PATH
#
#RUN npm ci --silent
#RUN npm install react-scripts@3.4.1 -g --silent
#
#RUN npm run build

CMD ["tail", "-f", "/dev/null"]