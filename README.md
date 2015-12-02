# Inventory System
Proof of concept

## Requirements

* Docker Compose
* VirtualBox

## Getting Started

```
git clone <repo>
cd insights
docker-compose up
```

Next, open new terminal and get the docker ports

```
docker ps
```

With the ports, now you can run a curl command and check it in Kibana.

**NOTE:** You will need to create any index for Kibana for `inventory` index.

```
curl -X POST http://192.168.99.100:[port]/v1/inventory -d '{"foo": "bar"}'
```

### Development

For local development on a Docker host or local machine, you can add the following to `docker-compose.yml`

```
app:
  volumes:
  - .:/src/app/insights
```  


### Troubleshooting Tips

Running the app manually

```
docker run --rm -it -v "$PWD:/src/app" --link iota_elasticsearch_1:elasticsearch bucket_app /bin/sh
ELASTICSEARCH_PORT_9200_TCP_ADDR='172.17.0.2'
ELASTICSEARCH_PORT_9200_TCP_PORT='9200'
```