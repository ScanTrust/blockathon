# docker build . -t eub
# docker run --rm -p 5000:5000 eub
# http :5000/ => {}

FROM python:3.6
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy the staging config to docker, which is what will be deployed on azure
# this should be in env settings at some point, this is just now & for dev
COPY ./conf/staging.cfg app.cfg

# copy the source code over, including the conf & startup stubs
COPY ./api/ ./api/
COPY ./mock_st_backend/ ./mock_st_backend/
COPY ./*.py ./

CMD ["python", "runserver.py"]