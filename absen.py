import cv2  # Untuk pengolahan gambar
import numpy as np  # Untuk mengonversi Gambar menjadi array Numerik
import os  # Untuk menangani direktori
import time  # Untuk menghitung waktu
from mfrc522 import SimpleMFRC522
import mysql.connector  # Library untuk koneksi MySQL

# Inisialisasi pembaca RFID
reader = SimpleMFRC522()

GPIO.setmode(GPIO.BCM)

LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

# Koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="user",
    password="qwerty",
    database="harmonikaabsen"
)

# Cursor untuk menjalankan perintah SQL
cursor = db.cursor()

# Fungsi untuk melakukan pengecekan apakah RFID telah terdaftar
def rfid_check(text2):
    folder_name = text2.replace(" ", "_")  # Mengganti spasi dengan underscore untuk nama folder
    folder_path = os.path.join(os.getcwd(), "Datasets_User", folder_name)  # Mendapatkan path folder
    return os.path.exists(folder_path)

# Load model untuk face recognition
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Inisialisasi kaskade wajah
face_cascade = cv2.CascadeClassifier('C:\Atd2\haarcascade_frontalface_default.xml')

# Dapatkan feed video dari Kamera
cap = cv2.VideoCapture(0)

while True:
    # Membaca RFID
    try:
        id, text1, text2 = reader.read()
        print(id, "|", text1, "|", text2)

        # Mengecek apakah RFID sudah terdaftar
        if not rfid_check(text2):
            print("RFID belum terdaftar.")
            continue

        # Jika RFID valid, lanjut ke proses face recognition
        start_time = time.time()
        while time.time() - start_time < 20:  # Maksimal proses face recognition selama 20 detik
            ret, img = cap.read()  # Memecah video menjadi frame
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Mengonversi frame Video ke Grayscale
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)  # Mengenali wajah

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]  # Mengonversi Wajah ke Grayscale
                id_, conf = recognizer.predict(roi_gray)  # Mengenali Wajah

                if conf >= 80:
                    font = cv2.FONT_HERSHEY_SIMPLEX  # Gaya Font untuk nama
                    name = text2  # Menggunakan NIM atau ID sebagai nama
                    cv2.putText(img, name, (x, y), font, 1, (0, 0, 255), 2)

                    # Mengirim status "hadir" ke database MySQL bersama dengan timestamp saat ini
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    folder_name = text2.replace(" ", "_")  # Mengganti spasi dengan underscore untuk nama folder
                    sql = f"INSERT INTO {folder_name} (nama, status_kehadiran, timestamp) VALUES (%s, %s, %s)"
                    val = (name, "hadir", timestamp)
                    cursor.execute(sql, val)
                    db.commit()

                    print("Status hadir telah dikirim ke database.")

                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Preview', img)  # Tampilkan Video
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(e)
        break

# Ketika semuanya selesai, lepaskan tangkapan
cap.release()
cv2.destroyAllWindows()
