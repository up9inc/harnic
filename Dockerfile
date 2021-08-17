FROM node:14 as frontend

WORKDIR /app

COPY harnic-spa harnic-spa
WORKDIR /app/harnic-spa

RUN npm run build


FROM python:3.8 as backend

# env var to tell the version
ENV IMG_LABEL="-image_label-"

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY --from=frontend /app/harnic-spa harnic-spa
COPY harnic harnic
COPY requirements.txt .
COPY setup.py .

# install dependencies
RUN pip install -r requirements.txt
RUN pip install -e .

ENTRYPOINT ["python", "harnic/main.py"]
