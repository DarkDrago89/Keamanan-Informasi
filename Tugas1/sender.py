"""Fungsi sender untuk mengirim pesan terenkripsi."""

import socket

from config import KEY, MAX_MESSAGE_SIZE, RECEIVER_IP, RECEIVER_PORT
from encryption import encrypt_message, frame_message
from chat import run_chat


def connect_to_receiver(receiver_ip=RECEIVER_IP, port=RECEIVER_PORT):
    """Open a TCP connection to the configured receiver."""
    return socket.create_connection((receiver_ip, port))


def send_message(connection, message, key=KEY, max_message_size=MAX_MESSAGE_SIZE):
    """Encrypt and send one complete framed message."""
    encoded_message = encrypt_message(message, key)
    if len(encoded_message) > max_message_size:
        raise ValueError("Pesan terlalu besar untuk dikirim")

    connection.sendall(frame_message(encoded_message))
    return encoded_message


def run_sender(receiver_ip=RECEIVER_IP, port=RECEIVER_PORT, key=KEY):
    """Connect to the receiver and start a two-way encrypted chat."""
    with connect_to_receiver(receiver_ip, port) as connection:
        print(f"Terhubung ke receiver {receiver_ip}:{port}.")
        run_chat(connection, "Sender", "Receiver", key)


if __name__ == "__main__":
    run_sender()
