# import cv2
# import os
# import time
# import mysql.connector
# from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()

# # Constants
# COUNT_LIMIT = 30
# POS = (30, 60)  # top-left
# FONT = cv2.FONT_HERSHEY_COMPLEX  # font type for text overlay
# HEIGHT = 1.5  # font_scale
# TEXTCOLOR = (0, 0, 255)  # BGR- RED
# BOXCOLOR = (255, 0, 255)  # BGR- BLUE
# WEIGHT = 3  # font-thickness
# FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# # # For each person, enter one numeric face id
# # face_id = input('\n----Enter User-id and press <return>----')
# # print("\n [INFO] Initializing face capture. Look at the camera and wait!")

# # Create an instance of the VideoCapture object for webcam
# cap = cv2.VideoCapture(0)

# count = 0

# while True:
#     text1 = input("Nama anggota: ")
#     text2 = input("NIM atau ID Pegawai: ")
    
#     # Membuat folder berdasarkan nama yang baru diinputkan
#     folder_name = text2.replace(" ", "_")  # Mengganti spasi dengan underscore untuk nama folder
#     folder_path = os.path.join(os.getcwd(), "Datasets_User", folder_name)  # Mendapatkan path folder baru
    
#     # Validasi apakah folder dataset sudah ada
#     if os.path.exists(folder_path):
#         print("Gagal mendaftar, NIM sudah terdaftar.")
#         continue

#     # Validasi apakah tabel di database sudah ada
#     db = mysql.connector.connect(
#         host="localhost",
#         user="admin",
#         password="123",
#         database="AttendanceTefa"
#     )
#     cursor = db.cursor()
#     cursor.execute(f"SHOW TABLES LIKE '{folder_name}'")
#     if cursor.fetchone():
#         print("Gagal mendaftar, NIM sudah terdaftar.")
#         continue
    
#     print("Silahkan scan RFID anda.")
#     reader.write(text1 + "," + text2)
#     print("Scanning berhasil.")

#     # Membuat folder baru
#     os.makedirs(folder_path, exist_ok=True)  # Membuat folder baru jika belum ada

#     print(f"Folder {folder_name} telah dibuat.")

#     # Validasi data yang diinputkan
#     validasi = input("Apakah data yang diinputkan sudah benar? (y/n): ")
#     if validasi.lower() != "y":
#         continue  # Ulangi proses input jika data tidak benar

#     # Membuat tabel dengan nama folder_name di dalam database
#     create_table_query = f"CREATE TABLE IF NOT EXISTS {folder_name} (id INT AUTO_INCREMENT PRIMARY KEY, \
#                             nama VARCHAR(255), \
#                             status_kehadiran VARCHAR(50), \
#                             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
#     cursor.execute(create_table_query)
#     db.commit()

#     print(f"Tabel {folder_name} telah dibuat di database.")

#     # Menanyakan apakah pengambilan foto bisa dimulai
#     while True:
#         start_capture = input("Apakah pengambilan foto bisa dimulai? (y/n): ")
#         if start_capture.lower() == "y":
#             break
#         elif start_capture.lower() == "n":
#             time.sleep(15)
#         else:
#             print("Input tidak valid.")

#     # Mengambil gambar selama 15 detik dan menyimpannya di dalam folder baru
#     start_time = time.time()
#     capture_duration = 15  # Durasi pengambilan gambar dalam detik

#     while time.time() - start_time < capture_duration:
#         ret, frame = cap.read()  # Baca frame dari kamera

#         # Display count of images taken
#         cv2.putText(frame, 'Count:' + str(int(count)), POS, FONT, HEIGHT, TEXTCOLOR, WEIGHT)

#         # Convert frame from BGR to grayscale
#         frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Create a DS faces- array with 4 elements- x,y coordinates (top-left corner), width and height
#         faces = FACE_DETECTOR.detectMultiScale(
#             frameGray,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30)
#         )

#         for (x, y, w, h) in faces:
#             # Create a bounding box across the detected face
#             cv2.rectangle(frame, (x, y), (x + w, y + h), BOXCOLOR, 3)
#             count += 1  # increment count

#             # Save the captured bounded-grayscale image into the datasets folder only if the same file doesn't exist
#             file_path = os.path.join(folder_path, f"foto_{int(time.time())}.jpg")
#             if not os.path.exists(file_path):
#                 cv2.imwrite(file_path, frameGray[y:y + h, x:x + w])

#         # Display the original frame to the user
#         cv2.imshow('Pendaftaran Anggota', frame)

#         # Wait for 30 milliseconds for a key event (extract sigfigs) and exit if 'ESC' or 'q' is pressed
#         key = cv2.waitKey(100) & 0xff
#         if key == 27:  # ESCAPE key
#             break
#         elif key == 113:  # q key
#             break

#     if key == 27 or key == 113:
#         break

# # Release the webcam and close all windows
# print("\n [INFO] Exiting Program and cleaning up stuff")
# cap.release()
# cv2.destroyAllWindows()

import cv2
import os
import time
import mysql.connector
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# Konstanta
COUNT_LIMIT = 30
POS = (30, 60)  # kiri-atas
FONT = cv2.FONT_HERSHEY_COMPLEX  # jenis font untuk teks
HEIGHT = 1.5  # skala font
TEXTCOLOR = (0, 0, 255)  # BGR- MERAH
BOXCOLOR = (255, 0, 255)  # BGR- BIRU
WEIGHT = 3  # ketebalan font
FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# # Untuk setiap orang, masukkan satu id wajah numerik
# face_id = input('\n----Masukkan User-id dan tekan <enter>----')
# print("\n [INFO] Menginisialisasi pengambilan wajah. Lihat ke kamera dan tunggu!")

# Membuat instance objek VideoCapture untuk webcam
cap = cv2.VideoCapture(0)

count = 0

while True:
    text1 = input("Nama anggota: ")
    text2 = input("NIM atau ID Pegawai: ")
    
    # Membuat folder berdasarkan NIM yang baru diinputkan
    folder_name = text2.replace(" ", "_")  # Mengganti spasi dengan underscore untuk nama folder
    folder_path = os.path.join(os.getcwd(), "Datasets_User", folder_name)  # Mendapatkan path folder baru
    
    # Validasi apakah folder dataset sudah ada
    if os.path.exists(folder_path):
        print("Gagal mendaftar, NIM sudah terdaftar.")
        continue

    # Validasi apakah tabel di database sudah ada
    db = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="123",
        database="AttendanceTefa"
    )
    cursor = db.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{folder_name}'")
    if cursor.fetchone():
        print("Gagal mendaftar, NIM sudah terdaftar.")
        continue
    
    print("Silahkan scan RFID anda.")
    reader.write(text1 + "," + text2)
    print("Scanning berhasil.")

    # Membuat folder baru
    os.makedirs(folder_path, exist_ok=True)  # Membuat folder baru jika belum ada
    # Membuat folder 'image' dan 'trained' di dalam folder anggota
    os.makedirs(os.path.join(folder_path, 'image'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'trained'), exist_ok=True)

    print(f"Folder {folder_name} telah dibuat.")

    # Validasi data yang diinputkan
    validasi = input("Apakah data yang diinputkan sudah benar? (y/n): ")
    if validasi.lower() != "y":
        continue  # Ulangi proses input jika data tidak benar

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

    while time.time() - start_time < capture_duration:
        ret, frame = cap.read()  # Baca frame dari kamera

        # Tampilkan jumlah gambar yang diambil
        cv2.putText(frame, 'Count:' + str(int(count)), POS, FONT, HEIGHT, TEXTCOLOR, WEIGHT)

        # Convert frame dari BGR ke skala abu-abu
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Buat array faces dengan 4 elemen- koordinat x,y (kiri-atas), lebar, dan tinggi
        faces = FACE_DETECTOR.detectMultiScale(
            frameGray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            # Buat bounding box di sekitar wajah yang terdeteksi
            cv2.rectangle(frame, (x, y), (x + w, y + h), BOXCOLOR, 3)
            count += 1  # increment count

            # Simpan gambar berwarna yang dibatasi ke dalam folder 'image' hanya jika file yang sama belum ada
            file_path = os.path.join(folder_path, 'image', f"foto_{int(time.time())}.jpg")
            if not os.path.exists(file_path):
                cv2.imwrite(file_path, frame[y:y + h, x:x + w])

        # Tampilkan frame asli kepada pengguna
        cv2.imshow('Pendaftaran Anggota', frame)

        # Tunggu selama 30 milidetik untuk kejadian tombol (ambil digit penting) dan keluar jika 'ESC' atau 'q' ditekan
        key = cv2.waitKey(100) & 0xff
        if key == 27:  # tombol ESC
            break
        elif key == 113:  # tombol q
            break

    if key == 27 or key == 113:
        break

# Bebaskan webcam dan tutup semua jendela
print("\n [INFO] Keluar dari Program dan membersihkan hal-hal")
cap.release()
cv2.destroyAllWindows()
