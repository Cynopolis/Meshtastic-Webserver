#!/bin/bash
CURRENT_DIRECTORY=$(pwd)
echo "Current directory: $CURRENT_DIRECTORY"

cd $CURRENT_DIRECTORY

if test -f "meshtastic"; then
    echo "Virtual environment already exists. Skipping venv creation."
else
    echo "Making virtual environment..."
    python3 -m venv meshtastic
fi

echo "Installing venv requirements"
meshtastic/bin/python -m pip install -r requirements.txt

echo "Generating service file from template"

read -p "Do you want to continue? (y/n): " choice

# Check if the user typed 'n' or 'N'
if [[ "$choice" == "n" || "$choice" == "N" ]]; then
  echo "Exiting the script..."
  exit 0
fi
echo "Continuing...\n Creating Service file..."
# Replace all instances of ${WORKING_DIRECTORY} with the actual working directory and write to the new file
sed "s|\${WORKING_DIRECTORY}|$CURRENT_DIRECTORY|g" "service-template/MeshtasticLogger-template.service" > "MeshtasticLogger.service"

echo "Deploying service"
sudo cp "$CURRENT_DIRECTORY/MeshtasticLogger.service" /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl start MeshtasticLogger


