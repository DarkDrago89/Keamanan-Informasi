"""Konfigurasi jaringan dan kriptografi untuk sender-receiver."""

# Ubah nilai ini di komputer sender menjadi IPv4 komputer receiver pada Wi-Fi.
RECEIVER_IP = "192.168.1.2"

# Receiver mendengarkan semua interface jaringan komputer receiver.
RECEIVER_HOST = "0.0.0.0"
RECEIVER_PORT = 5000

# Key harus sama persis di komputer sender dan receiver serta berukuran 8 byte.
KEY = b"12345678"
MAX_MESSAGE_SIZE = 1_048_576