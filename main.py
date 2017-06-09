#
# LoRaNanoGateway.py
#

import socket
import struct
from network import LoRa
import time

# A basic package header
# B: 1 byte for the deviceId
# B: 1 byte for the pkg size
# B: 1 byte for the messageId
# %ds: Formated string for string
_LORA_PKG_FORMAT = "!BBB%ds"

# A basic ack package
# B: 1 byte for the deviceId
# B: 1 byte for the pkg size
# B: 1 byte for the messageId
# B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBBB"

# Let the world know we're starting up.

print("Starting LoRaNanoGateway")

# Open a Lora Socket, use rx_iq to avoid listening to our own messages
lora = LoRa(mode=LoRa.LORA, rx_iq=True)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 4)
lora_sock.setblocking(False)

while (True):

    # Since the maximum body size in the protocol is 255 the request is limited to 512 bytes
    recv_pkg = lora_sock.recv(512)
    # print("Received message, length = %d" % len(recv_pkg))

    # If at least a message with the header is received process it
    if (len(recv_pkg) > 3):
        # print("<<<<<<<<<<<<< Received VALID message, length = %d" % len(recv_pkg))

        recv_pkg_len = recv_pkg[1]

        # If message is corrupted should not continue processing
        if (not len(recv_pkg) == recv_pkg_len + 3):
            continue

        # Unpack the message based on the protocol definition
        device_id, pkg_len, msg_id, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)

        # Respond to the device with an acknowledge package
        # time.sleep(0.15)
        print("+++ Received a message: %s" % msg)
        ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id, 1, msg_id, 200)
        print("------ Sending an ACK #%d" % msg_id)
        lora_sock.send(ack_pkg)

        # Do any extra processing required for the package. Keep in mind it should be as fast as posible
        # to make sure that the other clients are not waiting too long for their messages to be acknoleged
