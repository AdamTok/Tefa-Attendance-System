import cv2
import os

# Fungsi untuk membuat folder jika belum ada
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Membuat detektor wajah
face_cascade = cv2.CascadeClassifier('C:/Users/User/Documents/GitHub/Tefa-Attendance-System/haarcascade_frontalface_default.xml')

# Membuat recognizer LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Path untuk folder image dan trained
image_folder = 'image'
trained_folder = 'trained'

# Membuat folder image dan trained jika belum ada
create_folder_if_not_exists(image_folder)
create_folder_if_not_exists(trained_folder)

# Mendapatkan list file gambar dalam folder image
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# Mendapatkan data training jika sudah ada
if os.path.exists('train.yml'):
    recognizer.read('train.yml')

# Mendapatkan data wajah dari gambar-gambar dalam folder image
faces = []
labels = []
for image_file in image_files:
    img = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_detected = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces_detected:
        face_roi = gray[y:y+h, x:x+w]
        faces.append(face_roi)
        labels.append(0)  # Label 0 untuk wajah Anda

# Melakukan training jika ada data wajah yang terdeteksi
if faces:
    recognizer.train(faces, np.array(labels))
    recognizer.save(os.path.join(trained_folder, 'train.yml'))

# Membuka kamera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Mengubah ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Mendeteksi wajah
    faces_detected = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces_detected:
        # Memprediksi ID dan confidence
        id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        print(id_, confidence)

        # Menampilkan kotak di sekitar wajah
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Menampilkan ID prediksi dan confidence
        cv2.putText(frame, f'ID: {id_}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Confidence: {round(confidence, 2)}', (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)
    
    # Menampilkan frame
    cv2.imshow('Webcam', frame)
    
    # Keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Membebaskan sumber daya
cap.release()
cv2.destroyAllWindows()
