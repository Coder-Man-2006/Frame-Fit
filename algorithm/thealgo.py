import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
from PIL import Image

class FaceMap:
    def __init__(self, filtered_landmarks):
        self.filtered_landmarks = filtered_landmarks

class Skeleton(FaceMap):
    def __init__(self, points):
        self.points = points
        self.total_distance_list = []

    def find_distance(self):
        total_distance = 0.0
        for i in range(len(self.points) - 1):
            if len(self.total_distance_list) >= 10:
                break
            point1 = self.points[i]
            point2 = self.points[i + 1]
            distance = np.sqrt((point2 - point1) ** 2)
            total_distance += distance
            self.total_distance_list.append(distance)

class FaceAnalyzer:
    def __init__(self):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=1)
        self.scaling_factor = 400 / 63
        self.max_landmarks = 400
        self.all_indices = self.get_all_indices()

    def get_all_indices(self):
        chin_indices = list(range(0, int(17 * self.scaling_factor)))
        left_eyebrow_indices = list(range(int(22 * self.scaling_factor), int(27 * self.scaling_factor)))
        right_eyebrow_indices = list(range(int(17 * self.scaling_factor), int(22 * self.scaling_factor)))
        nose_bridge_indices = list(range(int(27 * self.scaling_factor), int(31 * self.scaling_factor)))
        nose_tip_indices = list(range(int(31 * self.scaling_factor), int(36 * self.scaling_factor)))
        left_eye_indices = list(range(int(36 * self.scaling_factor), int(42 * self.scaling_factor)))
        right_eye_indices = list(range(int(42 * self.scaling_factor), int(48 * self.scaling_factor)))
        top_lip_indices = list(range(int(48 * self.scaling_factor), int(55 * self.scaling_factor)))
        bottom_lip_indices = list(range(int(55 * self.scaling_factor), self.max_landmarks))
        return chin_indices + left_eyebrow_indices + right_eyebrow_indices + \
               nose_bridge_indices + nose_tip_indices + left_eye_indices + \
               right_eye_indices + top_lip_indices + bottom_lip_indices
               
    def detect_face_shape(self, filtered_landmarks):
        distances = self.calculate_distances(filtered_landmarks, 10)
        non_none_distances = [d for d in distances if d is not None]

        if len(non_none_distances) > 1:
            min_dist = np.min(non_none_distances)
            max_dist = np.max(non_none_distances)
            return "Oval" if max_dist - min_dist < 0.02 else "Other Shape"
        else:
            return "Shape Detection Not Possible"
    
    def calculate_distances(self, filtered_landmarks, ppi):
        distances = []

        # List of landmark indices for different measurements
        length_of_face_indices = [10, 9, 8, 6, 5, 4, 1, 2, 0, 12, 14, 15, 16, 175]
        temple_to_temple_indices = [68, 104, 69, 119, 299, 333, 298]
        cheekbone_to_cheekbone_indices = [280, 371, 281, 51, 110, 50]
        jawline_indices = [366, 361, 288, 397, 365, 379, 378, 369, 377, 120, 176, 117, 118, 168, 172, 58, 164, 93, 234]

        for indices in [length_of_face_indices, temple_to_temple_indices, cheekbone_to_cheekbone_indices, jawline_indices]:
            distance = 0.0
            for i in range(len(indices) - 1):
                point1 = filtered_landmarks[indices[i]]
                point2 = filtered_landmarks[indices[i + 1]]
                pixel_distance = np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
                real_distance = pixel_distance / ppi
                distance += real_distance
            distances.append(distance)

        return distances
<<<<<<< HEAD:algorithm/app.py
=======

>>>>>>> 0e012ddcdb7721a5fd088bc6176c857d78da5207:algorithm/thealgo.py
    
    def draw_landmarks(self, frame, filtered_landmarks, distances): 
           # Draw lines for specific measurements
        if distances[0] is not None:
            cv2.line(frame, filtered_landmarks[0], filtered_landmarks[8], (0, 255, 0), 2)  # Green line for "Length of Face"
        if distances[1] is not None:
            cv2.line(frame, filtered_landmarks[68], filtered_landmarks[104], (0, 255, 0), 2)  # Green line for "Temple to Temple"
        if distances[2] is not None:
            cv2.line(frame, filtered_landmarks[69], filtered_landmarks[119], (0, 255, 0), 2)  # Green line for "Cheekbone to Cheekbone"
        if distances[3] is not None:
            length_of_face = [10, 9, 8, 6, 5, 4, 1, 2, 0, 12, 14, 15, 16, 175] # List of Points across length of face
            temple_to_temple = [68, 104, 69, 119, 299, 333, 298]
            cheekbone_to_cheekbone = [280, 371, 281, 51, 110, 50]
            jawline_points = [366, 361, 288, 397, 365, 379, 378, 369, 377, 120, 176, 117, 118, 168, 172, 58, 164, 93, 234]
            for i in range(len(length_of_face) - 1):
                cv2.line(frame, filtered_landmarks[length_of_face[i]], filtered_landmarks[length_of_face[i + 1]], (245, 245, 220), 2)
            for i in range(len(temple_to_temple) - 1):
                cv2.line(frame, filtered_landmarks[temple_to_temple[i]], filtered_landmarks[temple_to_temple[i + 1]], (0, 255, 0), 2)
            for i in range(len(cheekbone_to_cheekbone) - 1):
                cv2.line(frame, filtered_landmarks[cheekbone_to_cheekbone[i]], filtered_landmarks[cheekbone_to_cheekbone[i + 1]], (176,224,230), 2)
            for i in range(len(jawline_points) - 1):
                cv2.line(frame, filtered_landmarks[jawline_points[i]], filtered_landmarks[jawline_points[i + 1]], (128,0,128), 2)
                
        print("Distances:", distances)  # Print the distances array to debug
        for landmark in filtered_landmarks:
            cv2.circle(frame, landmark, 2, (0, 0, 255), -1)

        if distances[0] is not None:
            cv2.putText(frame, f"Length of Face: {distances[0]:.2f}", (20, 100), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 0), 2)
        if distances[1] is not None:
            cv2.putText(frame, f"Temple to Temple: {distances[1]:.2f}", (20, 150), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 0), 2)
        if distances[2] is not None:
            cv2.putText(frame, f"Cheekbone to Cheekbone: {distances[2]:.2f}", (20, 200), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 0), 2)
        if distances[3] is not None:
            cv2.putText(frame, f"Jawline: {distances[3]:.2f}", (20, 250), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 0), 2)
            
            face_shape = self.detect_face_shape(filtered_landmarks)
            cv2.putText(frame, f"Face Shape: {face_shape}", (20, 300), cv2.FONT_HERSHEY_PLAIN,
                        2, (0, 0, 255), 2)
            cv2.imshow('Face Landmarks', frame)

    def process_single_image(self, pil_image):
        """Process an individual PIL Image."""
        frame = np.array(pil_image)
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                face_landmarks = [(int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                                for landmark in faceLms.landmark]
                filtered_landmarks = [face_landmarks[i] for i in self.all_indices]
                distances = self.calculate_distances(filtered_landmarks)
                self.draw_landmarks(frame, filtered_landmarks, distances)
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def run(self):
        screenshot_folder = "gallery"
        os.makedirs(screenshot_folder, exist_ok=True)
        screenshot_count = 1
        
        measurement_columns = ["Length of Face", "Temple to Temple", "Cheekbone to Cheekbone", "Jawline"]
        measurement_df = pd.DataFrame(columns=measurement_columns)
        
        while True:
            key = cv2.waitKey(1)
            ret, frame = self.cap.read()
            if not ret:
                break
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.faceMesh.process(imgRGB)
                    
            if results.multi_face_landmarks:
                for faceLms in results.multi_face_landmarks:
                    face_landmarks = [(int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                                    for landmark in faceLms.landmark]
                    filtered_landmarks = [face_landmarks[i] for i in self.all_indices]
                    distances = self.calculate_distances(filtered_landmarks, 10)
                    self.draw_landmarks(frame, filtered_landmarks, distances)
                    
                    total_distance = 0.0
            
            measurements = [distances[0], distances[1], distances[2], distances[3]]
            measurement_df.loc[len(measurement_df)] = measurements

                
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Press 's' to capture and save a screenshot
                screenshot_path = os.path.join(screenshot_folder, f"capture{str(screenshot_count)}.jpg")
                cv2.imwrite(screenshot_path, frame)
                print(f"Screenshot saved as {screenshot_path}")
                screenshot_count += 1
            
        measurement_df.to_csv("measurements.csv", index=False)


        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_analyzer = FaceAnalyzer()
    face_analyzer.run()

