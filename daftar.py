import RPI.GPIO as GPIO
import os
import cv2
from mfrc522 import SimpleMFRC522
import time
import mysql.connector

reader = SimpleMFRC522()

try:
    while True:
        text1 = input("Nama anggota: ")
        text2 = input("NIM atau ID Pegawai: ")
        print("Silahkan scan RFID anda.")
        reader.write(text1 + "," + text2)
        print("Scanning berhasil.")

        # Membuat folder berdasarkan nama yang baru diinputkan
        folder_name = text2.replace(" ", "_")  # Mengganti spasi dengan underscore untuk nama folder
        folder_path = os.path.join(os.getcwd(), "Datasets_User", folder_name)  # Mendapatkan path folder baru
        os.makedirs(folder_path, exist_ok=True)  # Membuat folder baru jika belum ada
        
        print(f"Folder {folder_name} telah dibuat.")

        # Validasi data yang diinputkan
        validasi = input("Apakah data yang diinputkan sudah benar? (y/n): ")
        if validasi.lower() != "y":
            continue  # Ulangi proses input jika data tidak benar

        # Koneksi ke database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="user",
            password="123",
            database="p"
        )

        # Cursor untuk menjalankan perintah SQL
        cursor = db.cursor()

        # Membuat tabel dengan nama folder_name di dalam database
        create_table_query = f"CREATE TABLE IF NOT EXISTS {folder_name} (id INT AUTO_INCREMENT PRIMARY KEY, \
                                nama VARCHAR(255), \
                                status_kehadiran VARCHAR(50), \
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        cursor.execute(create_table_query)
        db.commit()

        print(f"Tabel {folder_name} telah dibuat di database.")

        # Menanyakan apakah pengambilan foto bisa dimulai
        while True:
            start_capture = input("Apakah pengambilan foto bisa dimulai? (y/n): ")
            if start_capture.lower() == "y":
                break
            elif start_capture.lower() == "n":
                time.sleep(15)
            else:
                print("Input tidak valid.")

        # Mengambil gambar selama 15 detik dan menyimpannya di dalam folder baru
        start_time = time.time()
        capture_duration = 15  # Durasi pengambilan gambar dalam detik
        cap = cv2.VideoCapture(0)  # Buka kamera

        while time.time() - start_time < capture_duration:
            ret, frame = cap.read()  # Baca frame dari kamera
            cv2.imwrite(os.path.join(folder_path, f"foto_{int(time.time())}.jpg"), frame)  # Simpan frame sebagai gambar JPG
            time.sleep(0.1)  # Jeda singkat antara pengambilan gambar

        print("Proses pendaftaran berhasil.")

finally:
    GPIO.cleanup()
