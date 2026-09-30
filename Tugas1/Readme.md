# Tugas 1: Fungsi Enkripsi DES Sender-Receiver

## Nama     : Agil Lukman Hakim Muchdi
## NRP      : 5025241037

> **Catatan keamanan:** DES sudah tidak aman untuk melindungi data nyata. Implementasi ini hanya untuk pembelajaran dan demonstrasi konsep enkripsi simetris. Gunakan AES-GCM atau protokol TLS untuk aplikasi sungguhan.

File Python dipisahkan berdasarkan peran. Sender mengirim pesan yang sudah dienkripsi, receiver menerima dan mendekripsinya, sedangkan seluruh proses DES berada di `encryption.py`. Framing 4-byte disediakan agar batas pesan TCP tetap jelas.
Setelah tersambung, koneksi bersifat dua arah: sender dan receiver sama-sama dapat mengirim serta menerima pesan. Ciphertext ditampilkan di terminal pihak pengirim dan penerima.

## Isi Folder

- `encryption.py`: fungsi DES-CBC, Base64, validasi key, dan framing.
- `sender.py`: fungsi koneksi dan pengiriman pesan terenkripsi.
- `receiver.py`: fungsi socket receiver, penerimaan, dan dekripsi pesan.
- `chat.py`: loop komunikasi dua arah dan tampilan ciphertext/plaintext.
- `config.py`: alamat IP, host, port, key, dan batas ukuran pesan.
- `requirements.txt`: dependensi PyCryptodome.

## Fungsi Encryption

```python
from encryption import decrypt_message, encrypt_message, frame_message

encoded = encrypt_message("Pesan rahasia", key)
packet = frame_message(encoded)
plaintext = decrypt_message(encoded, key)
```

`encrypt_message()` menghasilkan ciphertext Base64. `decrypt_message()` mengembalikan plaintext. `frame_message()` menambahkan header panjang 4-byte.

## Fungsi Sender

```python
from sender import connect_to_receiver, send_message

connection = connect_to_receiver()
send_message(connection, "Pesan rahasia", key)
```

`send_message()` memakai fungsi dari `encryption.py`, lalu mengirim frame melalui TCP.

## Fungsi Receiver

```python
from receiver import create_receiver_socket, receive_decrypted_message

receiver_socket = create_receiver_socket()
connection, address = receiver_socket.accept()
plaintext = receive_decrypted_message(connection, key)
```

`receive_decrypted_message()` membaca satu frame lengkap, lalu memakai fungsi dekripsi dari `encryption.py`.

## Konfigurasi IP

Edit hanya `config.py`. Pada komputer receiver, gunakan:

```python
RECEIVER_HOST = "0.0.0.0"
RECEIVER_PORT = 5000
```

Pada komputer sender, ubah `RECEIVER_IP` menjadi IPv4 komputer receiver pada Wi-Fi yang sama:

```python
RECEIVER_IP = "192.168.1.20"
RECEIVER_PORT = 5000
```

`RECEIVER_IP` pada sender harus berisi IPv4 receiver, bukan IP sender. Cari IPv4 receiver dengan `ipconfig` pada Windows. `KEY` harus sama di kedua komputer.

## Prasyarat

- Python 3.9 atau lebih baru di kedua komputer.
- Kedua komputer terhubung ke jaringan yang sama, atau receiver dapat dijangkau melalui jaringan.
- Port TCP `5000` diizinkan oleh firewall komputer receiver.

## Instalasi di Kedua Komputer

Buka terminal di folder `tugas 1`, lalu jalankan:

```powershell
py -m pip install -r requirements.txt
```

Di macOS/Linux, gunakan:

```sh
python3 -m pip install -r requirements.txt
```

Key demo berada di `config.py` dan harus berukuran 8 byte. Nilai contoh `12345678` hanya untuk tugas; jangan gunakan sebagai key untuk informasi nyata.

## Menjalankan Program

Pastikan `config.py` memiliki IP receiver yang benar pada komputer sender dan `KEY` yang sama di kedua komputer.

Di komputer receiver, jalankan:

```powershell
py receiver.py
```

Di komputer sender, jalankan:

```powershell
py sender.py
```

Setelah muncul pesan koneksi dua arah aktif, kedua pihak dapat mengetik pesan pada terminalnya masing-masing. Setiap sisi menampilkan ciphertext yang dikirim dan ciphertext yang diterima, lalu menampilkan plaintext hasil dekripsi. Ketik `exit` pada salah satu sisi untuk menutup koneksi.

## Demonstrasi dengan Wireshark Nanti

1. Mulai capture pada interface jaringan yang aktif di salah satu komputer.
2. Gunakan display filter `tcp.port == 5000`.
3. Jalankan receiver dan sender, lalu kirim pesan dari salah satu atau kedua terminal.
4. Pilih paket koneksi tersebut, lalu pilih **Follow > TCP Stream**.

Stream berisi header panjang 4-byte diikuti teks Base64 untuk setiap pesan. Header dapat tampak sebagai karakter non-cetak; bagian Base64 adalah IV dan ciphertext, bukan plaintext. Pastikan pesan rahasia yang diketik tidak muncul sebagai teks biasa pada data aplikasi.

Base64 hanya encoding agar byte mudah ditampilkan, bukan enkripsi. Enkripsinya dilakukan oleh DES-CBC. IV dikirim bersama ciphertext dan bukan merupakan key rahasia.

## Alur Program

```text
Sender/Receiver: plaintext -> UTF-8 -> padding -> DES-CBC -> IV + ciphertext -> Base64 -> header panjang + TCP
Penerima di sisi lain: TCP -> baca header/pesan lengkap -> Base64 decode -> DES-CBC decrypt -> unpadding -> plaintext
```
