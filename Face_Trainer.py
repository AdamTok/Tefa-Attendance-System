# Program untuk melatih dengan wajah dan membuat file YAML

import cv2  # Untuk pengolahan gambar
import numpy as np  # Untuk mengonversi Gambar menjadi array Numerik
import os  # Untuk menangani direktori
from PIL import Image  # Library Pillow untuk menangani gambar

face_cascade = cv2.CascadeClassifier('C:/Atd/haarcascade_frontalface_default.xml')
recognizer = cv2.face.createLBPHFaceRecognizer()

Face_ID = -1
pev_person_name = ""
y_ID = []
x_train = []

Datasets_User = os.path.join(os.getcwd(), "Datasets_User")  # Beri tahu program di mana kita menyimpan gambar wajah
print(Datasets_User)

for root, dirs, files in os.walk(Datasets_User):  # masuk ke direktori gambar wajah
    for file in files:  # periksa setiap direktori di dalamnya
        if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png"):  # untuk file gambar yang berakhir dengan jpeg, jpg, atau png
            path = os.path.join(root, file)
            person_name = os.path.basename(root)
            print(path, person_name)

            if pev_person_name != person_name:  # Periksa apakah nama orang telah berubah
                Face_ID = Face_ID + 1  # Jika ya, tambahkan hitungan ID
                pev_person_name = person_name

            Gray_Image = Image.open(path).convert("L")  # konversi gambar ke grayscale menggunakan Pillow
            Crop_Image = Gray_Image.resize((800, 800), Image.ANTIALIAS)  # Potong Gambar Gray menjadi 550*550
            Final_Image = np.array(Crop_Image, "uint8")
            faces = face_cascade.detectMultiScale(Final_Image, scaleFactor=1.5, minNeighbors=5)  # Deteksi Wajah pada semua gambar sampel
            print(Face_ID, faces)

            for (x, y, w, h) in faces:
                roi = Final_Image[y:y+h, x:x+w]  # potong Region of Interest (ROI)
                x_train.append(roi)
                y_ID.append(Face_ID)

recognizer.train(x_train, np.array(y_ID))  # Buat Matriks Data Latihan
recognizer.save("face-trainner.yml")  # Simpan matriks sebagai file YML
