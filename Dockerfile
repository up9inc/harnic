FROM node:14 as frontend

WORKDIR /app

COPY harnic-spa harnic-spa
WORKDIR /app/harnic-spa

RUN npm install
RUN npm run build


FROM python:3.8 as backend

# env var to tell the version
ENV IMG_LABEL="-image_label-"

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY --from=frontend /app/harnic-spa harnic-spa
ENV SPA_LOCATION=/app/harnic-spa

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# install backend
COPY harnic harnic
COPY setup.py .

RUN pip install -e .

WORKDIR /hars

ENTRYPOINT ["python", "-m", "harnic"]
