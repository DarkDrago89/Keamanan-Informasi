"""Fungsi percakapan dua arah melalui koneksi TCP yang sudah terbuka."""

import socket
import threading

from config import KEY, MAX_MESSAGE_SIZE
from encryption import decrypt_message, encrypt_message, frame_message, receive_frame


def run_chat(connection, local_name, remote_name, key=KEY):
    """Send and receive encrypted messages until either side closes."""
    stop_event = threading.Event()
    print_lock = threading.Lock()

    def receive_messages():
        while not stop_event.is_set():
            try:
                encoded_message = receive_frame(connection, MAX_MESSAGE_SIZE)
                if encoded_message is None:
                    with print_lock:
                        print(f"\n{remote_name} menutup koneksi.")
                    stop_event.set()
                    return

                plaintext = decrypt_message(encoded_message, key)
                with print_lock:
                    print(f"\nCiphertext diterima dari {remote_name}:")
                    print(encoded_message.decode("ascii"))
                    print(f"Plaintext dari {remote_name}: {plaintext}")
            except (ConnectionError, OSError, ValueError, UnicodeDecodeError) as error:
                if not stop_event.is_set():
                    with print_lock:
                        print(f"\nKoneksi penerimaan berakhir: {error}")
                    stop_event.set()
                return

    receiver_thread = threading.Thread(target=receive_messages, daemon=True)
    receiver_thread.start()
    print("Koneksi dua arah aktif. Ketik pesan; ketik 'exit' untuk keluar.")

    try:
        while not stop_event.is_set():
            try:
                message = input(f"\n{local_name}: ")
            except (EOFError, KeyboardInterrupt):
                break

            if message.lower() == "exit":
                break

            encoded_message = encrypt_message(message, key)
            if len(encoded_message) > MAX_MESSAGE_SIZE:
                print("Pesan terlalu besar untuk dikirim.")
                continue

            connection.sendall(frame_message(encoded_message))
            with print_lock:
                print("Ciphertext yang dikirim:")
                print(encoded_message.decode("ascii"))
    except (ConnectionError, OSError) as error:
        print(f"Gagal mengirim pesan: {error}")
    finally:
        stop_event.set()
        try:
            connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        connection.close()
        receiver_thread.join(timeout=1)
        print("Koneksi ditutup.")
