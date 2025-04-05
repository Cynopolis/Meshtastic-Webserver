import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from MeshtasticDataClasses import RxPacket,to_rx_packet
from MeshtasticDataClasses import NodeData,to_node_data
from datetime import datetime

class MeshtasticLogger:
    def __init__(self, interface: meshtastic.serial_interface.SerialInterface, log_path : str, channel : int = 1, message_received_callback = None):
        # Subscribe to the recieve text event topic
        pub.subscribe(self.onReceive, "meshtastic.receive.text")
        self.interface = interface
        self.channel: int = channel
        self.log_path: str = log_path
        self.message_received_callback = message_received_callback
    
    def _cap_string_length_bytes(self, message : str, max_bytes: int):
        '''
        Cap the length of a string to be under max_bytes. It will just drop the excess from the string.
        '''
        capped_message = ""
        capped_message_byte_length = 0
        for char in message:
            next_char_byte_size = len(char.encode('utf-8'))
            if capped_message_byte_length + next_char_byte_size <= max_bytes:
                capped_message_byte_length += next_char_byte_size
                capped_message += char
        return capped_message

    def _log(self, message: str):
        print(message)
        with open(self.log_path, "a") as file:
            file.write(message)
    
    def send(self, message: str):
        self.interface.sendText(message, channelIndex=self.channel)
        timestamp: str = datetime.now().strftime("%m-%d %I:%M:%S %p")
        self._log(f"{timestamp}   You on channel {self.channel}: {message}\n")
        
            
    def onReceive(self, packet: dict, interface: meshtastic.serial_interface.SerialInterface):
        # parse the packet we recieved into a data class so we have nice type hints
        try:
            parsed_packet: RxPacket = to_rx_packet(packet)
        except Exception as e:
            self._log(e)
            return
            
        # get the current time
        timestamp: str = datetime.now().strftime("%m-%d %I:%M:%S %p")
        
        # try to grab the sender's ID. Otherwise it will just be unkown sender
        sender_node_name = "Unkown Sender"
        if parsed_packet.fromId in interface.nodes:
            try:
                sender_node: NodeData = to_node_data(interface.nodes[parsed_packet.fromId])
            except Exception as e:
                self._log(e)
                return
            sender_node_name = sender_node.user.longName
        
        # construct and _log the message
        message = f"{timestamp}   {sender_node_name}: On Channel {parsed_packet.channel}, message: {parsed_packet.decoded.text}\n"
        self._log(message)

        # parrot out the message but make sure the message length doesn't go above 233 bytes
        if parsed_packet.channel == 1:
            print("Parroting message")
            interface.sendText(self._cap_string_length_bytes(message, 233), channelIndex=self.channel)
        
        if not self.message_received_callback is None:
            self.message_received_callback(message)

