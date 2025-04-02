# Create a Virtual Environment
Create the virtual environment and activate it:

`python -m venv meshtastic && source meshtastic/bin/activate`

Install the requirements: `pip install requirements.txt`

Try it out before deploying it as a service: `flask run --host=0.0.0.0 --port=5000`

# Deploying Service Script Changes
Type the following commands:

`sudo cp ~/Projects/Meshtastic-Webserver/MeshtasticLogger.service /etc/systemd/system/ && sudo systemctl daemon-reload`

To start the service run
`sudo systemctl start MeshtasticLogger`

You can get the status of the service by running:

`sudo systemctl status MeshtasticLogger`

And you can stop the service by running:

`sudo systemctl stop MeshtasticLogger`