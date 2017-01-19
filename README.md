# EC Agent library for Python(v1.86_fukuoka)
#### Python Version
> Python 3.6.0
#### Required Libraries
```
python -m pip install cherrypy
```
# Endpoints
> /ec_version -> Retrieves the version of ECAgent being used.
> /get_ec_settings -> Retrieves the settings being used for ECAgent. 
> /start_ec_agent -> Starts ECAgent as per the defined settings in data.json
> /kill_ec_agent -> Kill ECAgent
> /check_ec_agent -> Return status of ECAgent. 

# Configuration
		- By default the server is configured to listen on port 8500.
		- All requests are GET requests.
		- All EC related configuration goes into data.json
		- If you do not need a proxy then leave it as blank string. 
	