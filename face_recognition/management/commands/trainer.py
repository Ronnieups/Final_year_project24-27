import os
import cv2
import numpy as np
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Train face recognizer model'

    def handle(self, *args, **options):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        path = "dataset"

        def get_images_with_id(path):
            images_paths = [os.path.join(path, f) for f in os.listdir(path)]
            faces = []
            Ids = []
            for single_image_path in images_paths:
                faceImg = cv2.imread(single_image_path, cv2.IMREAD_GRAYSCALE)
                id = int(os.path.split(single_image_path)[-1].split(".")[1])
                faces.append(faceImg)
                Ids.append(id)

            return np.array(Ids), faces 

        ids, faces = get_images_with_id(path)
        recognizer.train(faces, ids)
        recognizer.save("recognizer/trainingdata.yml")
        self.stdout.write(self.style.SUCCESS('Face recognizer model trained successfully'))
