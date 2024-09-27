import face_recognition
import os

def load_and_encode_faces(dataset_path='../dataset'):
    known_face_encodings = []
    known_face_names = []

    # Iterate over the folders in dataset
    for name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, name)
        if os.path.isdir(person_path):
            # Iterate over each image in the person's folder
            for image_filename in os.listdir(person_path):
                image_path = os.path.join(person_path, image_filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(name)

    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_and_encode_faces()
