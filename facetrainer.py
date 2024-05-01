# import cv2
# import os
# import numpy as np

# # Using LBPH(Local Binary Patterns Histograms) recognizer
# recognizer=cv2.face.LBPHFaceRecognizer_create()
# face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# path='dataset'

# # function to read the images in the dataset, convert them to grayscale values, return samples
# def getImagesAndLabels(path):
#     faceSamples=[]
#     ids = []

#     for file_name in os.listdir(path):
#         if file_name.endswith(".jpg"):
#             id = int(file_name.split(".")[1])
#             img_path = os.path.join(path, file_name)
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

#             faces = face_detector.detectMultiScale(img)

#             for (x, y, w, h) in faces:
#                 faceSamples.append(img[y:y+h, x:x+w])
#                 ids.append(id)

#     return faceSamples, ids

# def trainRecognizer(faces, ids): 
#     recognizer.train(faces, np.array(ids))
#     # Create the 'trainer' folder if it doesn't exist
#     if not os.path.exists("trainer"):
#         os.makedirs("trainer")
#     # Save the model into 'trainer/trainer.yml'
#     recognizer.write('trainer/trainer.yml')


# print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
# # Get face samples and their corresponding labels
# faces, ids = getImagesAndLabels(path)

# #Train the LBPH recognizer using the face samples and their corresponding labels
# trainRecognizer(faces, ids)

# # Print the number of unique faces trained
# num_faces_trained = len(set(ids))
# print("\n [INFO] {} faces trained. Exiting Program".format(num_faces_trained))

import cv2
import os
import numpy as np

# Menggunakan recognizer LBPH (Local Binary Patterns Histograms)
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
base_path = 'C:/Atd2/Datasets_User'  # Path dasar untuk dataset wajah anggota

# Fungsi untuk membaca foto-foto wajah, mengonversi ke skala abu-abu, dan mengembalikan sampel-sampel wajah dan label-labelnya
def getImagesAndLabels(path):
    faceSamples = []
    ids = []

    for file_name in os.listdir(path):
        if file_name.endswith(".jpg"):
            id = int(file_name.split(".")[0])  # Mendapatkan ID dari nama file
            img_path = os.path.join(path, file_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            faces = face_detector.detectMultiScale(img)

            for (x, y, w, h) in faces:
                faceSamples.append(img[y:y+h, x:x+w])
                ids.append(id)

    return faceSamples, ids

# Fungsi untuk melatih recognizer menggunakan sampel-sampel wajah dan label-labelnya
def trainRecognizer(faces, ids, trained_path): 
    recognizer.train(faces, np.array(ids))
    # Membuat direktori untuk menyimpan model yang dilatih
    if not os.path.exists(trained_path):
        os.makedirs(trained_path)
    # Menyimpan model yang dilatih ke dalam file .yml
    recognizer.write(os.path.join(trained_path, 'trainer.yml'))

# Proses training untuk setiap folder dalam direktori dataset
print("\n [INFO] Melatih wajah. Ini akan memakan beberapa detik. Tunggu ...")
for nim_folder in os.listdir(base_path):
    nim_folder_path = os.path.join(base_path, nim_folder)
    if os.path.isdir(nim_folder_path):
        image_folder_path = os.path.join(nim_folder_path, 'image')
        trained_folder_path = os.path.join(nim_folder_path, 'trained')
        # Mendapatkan sampel-sampel wajah dan label-labelnya dari folder gambar (image)
        faces, ids = getImagesAndLabels(image_folder_path)
        # Melatih recognizer menggunakan sampel-sampel wajah dan label-labelnya
        trainRecognizer(faces, ids, trained_folder_path)
        # Mencetak jumlah wajah unik yang telah dilatih untuk setiap folder
        num_faces_trained = len(set(ids))
        print("\n [INFO] {} wajah dari folder {} telah dilatih dan disimpan di {}.".format(num_faces_trained, nim_folder, trained_folder_path))

print("\n [INFO] Selesai melakukan training untuk semua folder. Keluar dari Program")
