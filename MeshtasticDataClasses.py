from dataclasses import dataclass
from typing import Optional

@dataclass
class Message:
    portnum: str
    payload: str
    text: str
    bitfield: Optional[str] = None
    replyId: Optional[str] = None
    emoji: Optional[str] = None

@dataclass
class RxPacket:
    _from: int
    to: int
    decoded: Message
    id: int
    rxTime: int
    rxSnr: float
    rxRssi: float
    hopStart: int
    raw: str
    fromId: str
    toId: str
    hopLimit: Optional[int] = None
    channel: Optional[int] = None
    

@dataclass
class Position:
    latitudeI: int
    longitudeI: int
    altitude: float
    time: int
    locationSource: str
    PDOP: int
    groundSpeed: int
    groundTrack: int
    satsInView: int
    precisionBits: int
    raw: str
    latitude: float
    longitude: float

@dataclass
class User:
    id: str
    longName: str
    shortName: str
    macaddr: str
    hwModel: str
    publicKey: str
    role: Optional[str] = None
    raw: Optional[str] = None

@dataclass
class DeviceMetrics:
    batteryLevel: float
    voltage: float
    channelUtilization: float
    airUtilTx: float
    uptimeSeconds: int

@dataclass
class NodeData:
    num: int
    user: User
    snr: float
    lastHeard: int
    hopsAway: int
    deviceMetrics: Optional[DeviceMetrics] = None
    position: Optional[Position] = None
    lastReceived: Optional[str] = None
    hopLimit: Optional[int] = None
    
def to_rx_packet(rawPacket: dict) -> RxPacket:
    if "from" in rawPacket:
        rawPacket["_from"] = rawPacket.pop("from")
    
    parsed_packet = RxPacket(**rawPacket)
    parsed_packet.decoded = Message(**parsed_packet.decoded)
    return parsed_packet

def to_node_data(rawNode: dict) -> NodeData:
    # parse the dictionary into a dataclass
    parsed_node = NodeData(**rawNode)
    parsed_node.user = User(**parsed_node.user)
    parsed_node.deviceMetrics = DeviceMetrics(**parsed_node.deviceMetrics)
    return parsed_node

if __name__ == "__main__":
    test_packet = {
        'from': 541024136, 
        'to': 4294967295, 
        'channel': 1, 
        'decoded': 
            {
                'portnum': 'TEXT_MESSAGE_APP', 
                'payload': b'Test', 
                'bitfield': 0, 
                'text': 'Test'
            }, 
        'id': 1489259583, 
        'rxTime': 1743434610, 
        'rxSnr': 6.25, 
        'hopLimit': 3, 
        'rxRssi': -32, 
        'hopStart': 3,
        'raw':"",
        'fromId':"",
        'toId':"",
        }
    
    test = to_rx_packet(test_packet)
    print(test)
    
    
    