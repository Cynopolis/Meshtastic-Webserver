from flask import Flask, render_template, request, jsonify
import meshtastic
from MeshtasticLogger import MeshtasticLogger
from CommandHandler import CommandHandler
import os

# -------------------------------
#   Initialize data and objects
# -------------------------------
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

command_handler: CommandHandler = CommandHandler(web_print)
logger = MeshtasticLogger(interface, "logs/mesh_logs.log", channel=1, message_received_callback=web_print)

# -------------------------
# Command Callback Handlers
# -------------------------
def help_response(args: list[str]):
    return "Commands:\nhelp - show this message\clear - clear the text log\nsend <text> - sends text to all channels\nchannel <number> - sets the current channel (0-7)\n"

def channel_response(args: list[str]):
    if len(args) < 1:
        return f"Current channel number: {logger.channel}"
    channel: int = int(args[0])
    if channel > 7 or channel < 0:
        return "Channel must be between 0 and 7"

    try:
        logger.channel = channel
    except Exception as e:
        return e
    
    return f"Channel set to {channel}"

def send_response(args: list[str]):
    if len(args) == 0:
        return "Please provide text to send"
    
    command = ""
    for arg in args:
        command += arg + " "
        
    command = command[:-1] # remove the trailing space
    
    logger.send(command)
    return_message = f"Sent: {command}"
    return return_message

def clear_response(args):
    messages.clear()
    return None

# register callbacks
command_handler.register_callback("clear", clear_response)
command_handler.register_callback("help", help_response)
command_handler.register_callback("channel", channel_response)
command_handler.register_callback("send", send_response)

# -----------------------
# Flask Callback Handlers
# -----------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    message = data.get("message", "")
    command_handler.parse_command(message)
    return jsonify({"messages": messages})

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})

