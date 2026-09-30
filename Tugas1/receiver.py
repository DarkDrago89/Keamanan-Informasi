"""Fungsi receiver untuk menerima dan mendekripsi pesan."""

import socket
from config import KEY, MAX_MESSAGE_SIZE, RECEIVER_HOST, RECEIVER_PORT
from encryption import decrypt_message, receive_exact, receive_frame
from chat import run_chat


def receive_exact(connection, size):
    """Read exactly size bytes, or return None when the sender closes cleanly."""
    if size < 0:
        raise ValueError("Ukuran data tidak boleh negatif")

    data = bytearray()
    while len(data) < size:
        chunk = connection.recv(size - len(data))
        if not chunk:
            if not data:
                return None
            raise ConnectionError("Koneksi terputus di tengah pesan")
        data.extend(chunk)
    return bytes(data)


def receive_message(connection, max_message_size=MAX_MESSAGE_SIZE):
    """Receive one framed Base64 message from the sender."""
    return receive_frame(connection, max_message_size)


def receive_decrypted_message(connection, key=KEY, max_message_size=MAX_MESSAGE_SIZE):
    """Receive one message and return its decrypted plaintext."""
    encoded_message = receive_message(connection, max_message_size)
    if encoded_message is None:
        return None
    return decrypt_message(encoded_message, key)


def create_receiver_socket(host=RECEIVER_HOST, port=RECEIVER_PORT, backlog=5):
    """Create, bind, and listen on the configured receiver address."""
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_socket.bind((host, port))
    receiver_socket.listen(backlog)
    return receiver_socket


def run_receiver(host=RECEIVER_HOST, port=RECEIVER_PORT, key=KEY):
    """Run the receiver loop until interrupted by the user."""
    with create_receiver_socket(host, port) as receiver_socket:
        print(f"Receiver berjalan pada {host}:{port}")
        print("Menunggu koneksi sender...")

        while True:
            connection, address = receiver_socket.accept()
            print(f"Sender terhubung: {address}")
            run_chat(connection, "Receiver", "Sender", key)
            print("Menunggu koneksi sender berikutnya...")


if __name__ == "__main__":
    run_receiver()
