Gateway in python3 for API servers
=======

Include load balancing (not health check available for servers)


How to use:
---------------

- Install requirements ```pip install -r requirements.txt```
- Configure paths and servers in *gateway.yaml*
- Build docker image ```docker build -t gateway .```
- Run docker container ```docker run -d -p 5000:8804 gateway```
- Test ```http://localhost:5000/```

Environment variables (optional):

- local port for gateway (default: 8804) -> ```GATEWAY_APP_LOCAL_PORT```
- log health check gateway (default: False) - ```LOG_HEALTH```
- log servers (default: False) - ```LOG_SERVICES```

License
=======
MIT