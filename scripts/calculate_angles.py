import csv
import numpy as np

class CalculateAngles:
    def __init__(self):
        pass

    def __read_coordinates_from_csv(self, file_path, columns):
        coordinates = {col: [] for col in columns}

        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                for col in columns:
                    coordinates[col].append(float(row[col]))
        return coordinates

    def __write_angles_to_csv(self, angles_dict, out_path):
        with open(out_path, 'w', newline='') as csv_file:
            csvwriter = csv.writer(csv_file)
            
            # Write header row
            csvwriter.writerow(angles_dict.keys())
            
            # Write data rows
            rows = zip(*angles_dict.values())
            csvwriter.writerows(rows)

    def __calculate_angle_deg(self, v1, v2):
        dot_product = np.dot(v1, v2)
        magnitude1 = np.linalg.norm(v1)
        magnitude2 = np.linalg.norm(v2)
        
        angle_radians = np.arccos(dot_product / (magnitude1 * magnitude2))
        angle_degrees = np.degrees(angle_radians)
        
        return angle_degrees

    def main(self, file_path, out_path):
        columns = {
            'nose': [0, 1, 2],
            'l_shoulder': [33, 34, 35],
            'r_shoulder': [36, 37, 38],
            'l_elbow': [39, 40, 41],
            'r_elbow': [42, 43, 44],
            'l_hip': [69, 70, 71],
            'r_hip': [72, 73, 74],
            'l_knee': [75, 76, 77],
            'r_knee': [78, 79, 80],
            'l_wrist': [45, 46, 47],
            'r_wrist': [48, 49, 50],
            'l_ankle': [81, 82, 83],
            'r_ankle': [84, 85, 86]
        }

        coordinates = {}
        for key, cols in columns.items():
            coordinates[key] = self.__read_coordinates_from_csv(file_path, cols)

        # Calculate mid points
        mid_shoulder = [(np.array(coordinates['l_shoulder'][i]) + np.array(coordinates['r_shoulder'][i])) / 2 for i in range(len(coordinates['l_shoulder'][0]))]
        mid_hip = [(np.array(coordinates['l_hip'][i]) + np.array(coordinates['r_hip'][i])) / 2 for i in range(len(coordinates['l_hip'][0]))]
        mid_knee = [(np.array(coordinates['l_knee'][i]) + np.array(coordinates['r_knee'][i])) / 2 for i in range(len(coordinates['l_knee'][0]))]

        # Angles dictionary
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

        for i in range(len(coordinates['nose'][0])):
            angles_dict['neck'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['nose'])[:, i] - np.array(mid_shoulder)[:, i],
                    np.array(mid_hip)[:, i] - np.array(mid_shoulder)[:, i]
                ) + 20
            )

            angles_dict['upper_left_arm'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['l_hip'])[:, i] - np.array(coordinates['l_shoulder'])[:, i],
                    np.array(coordinates['l_elbow'])[:, i] - np.array(coordinates['l_shoulder'])[:, i]
                )
            )
            
            angles_dict['upper_right_arm'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['r_hip'])[:, i] - np.array(coordinates['r_shoulder'])[:, i],
                    np.array(coordinates['r_elbow'])[:, i] - np.array(coordinates['r_shoulder'])[:, i]
                )
            )

            angles_dict['trunk'].append(
                self.__calculate_angle_deg(
                    np.array(mid_shoulder)[:, i] - np.array(mid_hip)[:, i],
                    np.array(mid_knee)[:, i] - np.array(mid_hip)[:, i]
                )
            )

            angles_dict['upper_left_leg'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['l_shoulder'])[:, i] - np.array(coordinates['l_hip'])[:, i],
                    np.array(coordinates['l_knee'])[:, i] - np.array(coordinates['l_hip'])[:, i]
                )
            )
            
            angles_dict['upper_right_leg'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['r_shoulder'])[:, i] - np.array(coordinates['r_hip'])[:, i],
                    np.array(coordinates['r_knee'])[:, i] - np.array(coordinates['r_hip'])[:, i]
                )
            )

            angles_dict['lower_left_arm'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['l_shoulder'])[:, i] - np.array(coordinates['l_elbow'])[:, i],
                    np.array(coordinates['l_wrist'])[:, i] - np.array(coordinates['l_elbow'])[:, i]
                )
            )
            
            angles_dict['lower_right_arm'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['r_shoulder'])[:, i] - np.array(coordinates['r_elbow'])[:, i],
                    np.array(coordinates['r_wrist'])[:, i] - np.array(coordinates['r_elbow'])[:, i]
                )
            )

            angles_dict['lower_left_leg'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['l_hip'])[:, i] - np.array(coordinates['l_knee'])[:, i],
                    np.array(coordinates['l_ankle'])[:, i] - np.array(coordinates['l_knee'])[:, i]
                )
            )
            
            angles_dict['lower_right_leg'].append(
                self.__calculate_angle_deg(
                    np.array(coordinates['r_hip'])[:, i] - np.array(coordinates['r_knee'])[:, i],
                    np.array(coordinates['r_ankle'])[:, i] - np.array(coordinates['r_knee'])[:, i]
                )
            )

        self.__write_angles_to_csv(angles_dict, out_path)
