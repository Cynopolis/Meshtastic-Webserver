from flask import Flask, render_template, request, jsonify
import meshtastic
from MeshtasticLogger import MeshtasticLogger
import os

messages = []
app = Flask(__name__)
interface = meshtastic.serial_interface.SerialInterface()
log_path = "logs/mesh_logs.log"

try:
    with open(log_path, 'r') as file:
        for line in file:
            messages.append(line)
except FileNotFoundError:
    # make the log directory if it isn't already there
    with open(log_path, "w") as file:
        file.write("Begin logs")

def web_print(message: str):
    with app.app_context():
        print(message)
        messages.append(message)
        get_messages()
    
def callback(message: str):
    web_print(message)

def help_response():
    help_message: str = "Commands:\nhelp - show this message\clear - clear the text log\nsend <text> - sends text to all channels\nchannel <number> - sets the current channel (0-7)\n"
    web_print(help_message)

logger = MeshtasticLogger(interface, "logs/mesh_logs.log", channel=1, message_received_callback=callback)

def channel_response(args: list[str]):
    if(len(args) < 2):
        web_print(f"Current channel number: {logger.channel}")
        return
    channel: int = int(args[1])
    if channel > 7 or channel < 0:
        web_print("Channel must be between 0 and 7")
    else:
        try:
            logger.channel = channel
        except Exception as e:
            web_print(e)
        else:
            web_print(f"Channel set to {channel}")

def send_response(args: list[str], command: str):
    if len(args) < 2:
        web_print("Please provide text to send")
    else:
        logger.send(command[5:])
        web_print(f"Sent: {command[5:]}")

def parse_command(command):
    args = command.split(" ")
    if len(args) < 1:
        return True
    
    if args[0] == "clear":
        messages.clear()
    elif args[0] == "help":
        help_response()
    elif args[0] == "channel":
        channel_response(args)
    elif args[0] == "send":
        send_response(args, command)
    else:
        web_print("Command not recognized. Type \'help\' for a list of commands.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    message = data.get("message", "")
    parse_command(message)
    return jsonify({"messages": messages})

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)