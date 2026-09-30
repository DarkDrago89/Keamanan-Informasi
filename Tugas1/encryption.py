"""Fungsi enkripsi, dekripsi, dan framing pesan."""

import base64
import struct

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

from config import KEY


def validate_key(key=KEY):
    """Validate the 8-byte DES key and return it."""
    if len(key) != DES.key_size:
        raise ValueError("Key DES harus berukuran 8 byte")
    return key


def encrypt_message(message, key=KEY):
    """Encrypt a UTF-8 message with DES-CBC and return Base64 bytes."""
    validate_key(key)
    cipher = DES.new(key, DES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(message.encode("utf-8"), DES.block_size))
    return base64.b64encode(cipher.iv + encrypted_data)


def decrypt_message(encoded_message, key=KEY):
    """Decode and decrypt a Base64 DES-CBC message into UTF-8 text."""
    validate_key(key)
    ciphertext = base64.b64decode(encoded_message, validate=True)
    if len(ciphertext) < DES.block_size * 2 or len(ciphertext) % DES.block_size:
        raise ValueError("Panjang ciphertext tidak valid")

    cipher = DES.new(key, DES.MODE_CBC, ciphertext[:DES.block_size])
    plaintext = unpad(cipher.decrypt(ciphertext[DES.block_size:]), DES.block_size)
    return plaintext.decode("utf-8")


def frame_message(encoded_message):
    """Add a 4-byte network-order length header to an encoded message."""
    if not encoded_message:
        raise ValueError("Pesan tidak boleh kosong")
    return struct.pack("!I", len(encoded_message)) + encoded_message


def receive_exact(connection, size):
    """Read exactly size bytes, or return None when the peer closes cleanly."""
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


def receive_frame(connection, max_message_size=1_048_576):
    """Read one length-prefixed Base64 message from a socket."""
    header = receive_exact(connection, 4)
    if header is None:
        return None

    message_size = struct.unpack("!I", header)[0]
    if message_size == 0 or message_size > max_message_size:
        raise ValueError("Ukuran pesan tidak valid")

    encoded_message = receive_exact(connection, message_size)
    if encoded_message is None:
        raise ConnectionError("Koneksi terputus sebelum pesan lengkap")
    return encoded_message
