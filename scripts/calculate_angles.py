import csv
import numpy as np

class CalculateAngles:
    def __init__(self):
        pass

    def __read_coordinates_from_csv(self, file_path, columns):
        coordinates = {key: [] for key in columns}
        
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                for key, col in columns.items():
                    coordinates[key].append(float(row[col]))
        return coordinates

    def __write_angles_to_csv(self, angles_dict, out_path):
        with open(out_path, 'w', newline='') as csv_file:
            csvwriter = csv.writer(csv_file)
            headers = list(angles_dict.keys())
            csvwriter.writerow(headers)
            
            for row in zip(*angles_dict.values()):
                csvwriter.writerow(row)

    def __calculate_angle_deg(self, p1, p2, p3):
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)
        dot_product = np.dot(v1, v2)
        angle_radians = np.arccos(dot_product / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        return np.degrees(angle_radians)

    def main(self, file_path, out_path):
        columns = {
            'nose': (0, 1, 2),
            'l_shoulder': (33, 34, 35),
            'r_shoulder': (36, 37, 38),
            'l_elbow': (39, 40, 41),
            'r_elbow': (42, 43, 44),
            'l_hip': (69, 70, 71),
            'r_hip': (72, 73, 74),
            'l_knee': (75, 76, 77),
            'r_knee': (78, 79, 80),
            'l_wrist': (45, 46, 47),
            'r_wrist': (48, 49, 50),
            'l_ankle': (81, 82, 83),
            'r_ankle': (84, 85, 86)
        }
        
        coordinates = self.__read_coordinates_from_csv(file_path, columns)

        mid_shoulder = [(np.array(coordinates['l_shoulder'][i]) + np.array(coordinates['r_shoulder'][i])) / 2 for i in range(len(coordinates['l_shoulder']))]
        mid_hip = [(np.array(coordinates['l_hip'][i]) + np.array(coordinates['r_hip'][i])) / 2 for i in range(len(coordinates['l_hip']))]
        mid_knee = [(np.array(coordinates['l_knee'][i]) + np.array(coordinates['r_knee'][i])) / 2 for i in range(len(coordinates['l_knee']))]

        angles_dict = {
            'neck': [],
            'trunk': [],
            'upper_left_arm': [],
            'upper_right_arm': [],
            'upper_left_leg': [],
            'upper_right_leg': [],
            'lower_left_arm': [],
            'lower_right_arm': [],
            'lower_left_leg': [],
            'lower_right_leg': []
        }

        for i in range(len(coordinates['nose'])):
            angles_dict['neck'].append(self.__calculate_angle_deg(
                (coordinates['nose'][i], coordinates['nose'][i], coordinates['nose'][i]),
                mid_shoulder[i],
                mid_hip[i]) + 20)

            angles_dict['upper_left_arm'].append(self.__calculate_angle_deg(
                coordinates['l_hip'][i],
                coordinates['l_shoulder'][i],
                coordinates['l_elbow'][i]))

            angles_dict['upper_right_arm'].append(self.__calculate_angle_deg(
                coordinates['r_hip'][i],
                coordinates['r_shoulder'][i],
                coordinates['r_elbow'][i]))

            angles_dict['trunk'].append(self.__calculate_angle_deg(
                mid_shoulder[i],
                mid_hip[i],
                mid_knee[i]))

            angles_dict['upper_left_leg'].append(self.__calculate_angle_deg(
                coordinates['l_shoulder'][i],
                coordinates['l_hip'][i],
                coordinates['l_knee'][i]))

            angles_dict['upper_right_leg'].append(self.__calculate_angle_deg(
                coordinates['r_shoulder'][i],
                coordinates['r_hip'][i],
                coordinates['r_knee'][i]))

            angles_dict['lower_left_arm'].append(self.__calculate_angle_deg(
                coordinates['l_shoulder'][i],
                coordinates['l_elbow'][i],
                coordinates['l_wrist'][i]))

            angles_dict['lower_right_arm'].append(self.__calculate_angle_deg(
                coordinates['r_shoulder'][i],
                coordinates['r_elbow'][i],
                coordinates['r_wrist'][i]))

            angles_dict['lower_left_leg'].append(self.__calculate_angle_deg(
                coordinates['l_hip'][i],
                coordinates['l_knee'][i],
                coordinates['l_ankle'][i]))

            angles_dict['lower_right_leg'].append(self.__calculate_angle_deg(
                coordinates['r_hip'][i],
                coordinates['r_knee'][i],
                coordinates['r_ankle'][i]))

        self.__write_angles_to_csv(angles_dict, out_path)
