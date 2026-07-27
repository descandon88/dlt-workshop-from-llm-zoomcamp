cd homework-workshop
docker build -t workshop-hw-dlt:1.0 .
docker run --rm --env-file .env workshop-hw-dlt:1.0
