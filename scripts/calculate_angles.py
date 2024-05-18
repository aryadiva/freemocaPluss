import csv
import math
import numpy as np

class CalculateAngles:
    def __init__(self):
        pass

    def __read_coordinates_from_csv(self, file_path, x_column, y_column, z_column):
        coordinates = {'x': [], 'y': [], 'z': []}
        
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                coordinates['x'].append(float(row[x_column]))
                coordinates['y'].append(float(row[y_column]))
                coordinates['z'].append(float(row[z_column]))
        return coordinates

    def __write_angles_to_csv(self, list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, out_path):
        with open(out_path, 'w', newline='') as csv_file:
            csvwriter = csv.writer(csv_file)
            
            # Write header row
            csvwriter.writerow(['neck', 'trunk', 'upper_left_arm', 'upper_right_arm', 'upper_left_leg', 'upper_right_leg', 
                                'lower_left_arm', 'lower_right_arm','lower_left_leg', 'lower_right_leg'])
            
            # Write data rows
            for i in range(len(list1)):
                csvwriter.writerow([list1[i], list2[i], list3[i], list4[i], list5[i], list6[i], list7[i], list8[i], list9[i], list10[i]])

    def __calculate_angle_deg(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        # Calculate vectors
        # Assuming coord 2 is the middle and coord 1 & 3 move away from coord 2 
        #   and thus coord 1 - 2 and coord 3 - 2
        v1 = np.array([x1 - x2, y1 - y2, z1 - z2])
        v2 = np.array([x3 - x2, y3 - y2, z3 - z2])

        dot_product = np.dot(v1, v2)

        magnitude1 = np.linalg.norm(v1)
        magnitude2 = np.linalg.norm(v2)
        
        angle_radians = np.arccos(dot_product / (magnitude1 * magnitude2))
        
        angle_degrees = np.degrees(angle_radians)
        
        return angle_degrees

    def main(self, file_path, out_path):
        #file_path = 'C:\\Users\\Arya\\freemocap_data\\recording_sessions\\sample1\\output_data\\mediapipe_body_3d_xyz.csv'  # CSV file path
        # file_path = 'mediapipe_body_3d_xyz.csv'
        #out_path = 'C:\\Users\\Arya\\OneDrive - Universiti Sains Malaysia\\Final Year\\CAT405\\Project_Final\\out_angle4.csv'

        #nose
        x_column, y_column, z_column = 0, 1, 2 
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        nose_x_coord = coordinates['x']
        nose_y_coord = coordinates['y']
        nose_z_coord = coordinates['z']

        #shoulder
        x_column, y_column, z_column = 33, 34, 35 
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        l_shoulder_x_coord = coordinates['x']
        l_shoulder_y_coord = coordinates['y']
        l_shoulder_z_coord = coordinates['z']

        x_column, y_column, z_column = 36, 37, 38 
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        r_shoulder_x_coord = coordinates['x']
        r_shoulder_y_coord = coordinates['y']
        r_shoulder_z_coord = coordinates['z']
        #mid shoulder
        mid_shoulder_x_coord = (np.array(l_shoulder_x_coord) + np.array(r_shoulder_x_coord))/2
        mid_shoulder_y_coord = (np.array(l_shoulder_y_coord) + np.array(r_shoulder_y_coord))/2
        mid_shoulder_z_coord = (np.array(l_shoulder_z_coord) + np.array(r_shoulder_z_coord))/2

        #elbow
        x_column, y_column, z_column = 39, 40, 41
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        l_elbow_x_coord = coordinates['x']
        l_elbow_y_coord = coordinates['y']
        l_elbow_z_coord = coordinates['z']

        x_column, y_column, z_column = 42, 43, 44
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)

        r_elbow_x_coord = coordinates['x']
        r_elbow_y_coord = coordinates['y']
        r_elbow_z_coord = coordinates['z']

        #hip
        x_column, y_column, z_column = 69, 70, 71
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        l_hip_x_coord = coordinates['x']
        l_hip_y_coord = coordinates['y']
        l_hip_z_coord = coordinates['z']

        x_column, y_column, z_column = 72, 73, 74
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        r_hip_x_coord = coordinates['x']
        r_hip_y_coord = coordinates['y']
        r_hip_z_coord = coordinates['z']
        #mid hip
        mid_hip_x_coord = (np.array(l_hip_x_coord) + np.array(r_hip_x_coord))/2
        mid_hip_y_coord = (np.array(l_hip_y_coord) + np.array(r_hip_y_coord))/2
        mid_hip_z_coord = (np.array(l_hip_z_coord) + np.array(r_hip_z_coord))/2

        #knees
        x_column, y_column, z_column = 75, 76, 77
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        l_knee_x_coord = coordinates['x']
        l_knee_y_coord = coordinates['y']
        l_knee_z_coord = coordinates['z']

        x_column, y_column, z_column = 78, 79, 80
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        r_knee_x_coord = coordinates['x']
        r_knee_y_coord = coordinates['y']
        r_knee_z_coord = coordinates['z']
        #mid knee
        mid_knee_x_coord = (np.array(l_knee_x_coord) + np.array(r_knee_x_coord))/2
        mid_knee_y_coord = (np.array(l_knee_y_coord) + np.array(r_knee_y_coord))/2
        mid_knee_z_coord = (np.array(l_knee_z_coord) + np.array(r_knee_z_coord))/2

        #wrist
        x_column, y_column, z_column = 45, 46, 47
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        l_wrist_x_coord = coordinates['x']
        l_wrist_y_coord = coordinates['y']
        l_wrist_z_coord = coordinates['z']

        x_column, y_column, z_column = 48, 49, 50
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        r_wrist_x_coord = coordinates['x']
        r_wrist_y_coord = coordinates['y']
        r_wrist_z_coord = coordinates['z']

        #ankle
        x_column, y_column, z_column = 81, 82, 83
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        l_ankle_x_coord = coordinates['x']
        l_ankle_y_coord = coordinates['y']
        l_ankle_z_coord = coordinates['z']

        x_column, y_column, z_column = 84, 85, 86
        coordinates = self.__read_coordinates_from_csv(file_path, x_column, y_column, z_column)
        
        r_ankle_x_coord = coordinates['x']
        r_ankle_y_coord = coordinates['y']
        r_ankle_z_coord = coordinates['z']

        # lines to generate list of desired joints angle
        head_angles_arr = []
        trunk_angles_arr= []

        upper_l_arm_angles_arr = []
        upper_r_arm_angles_arr = []
        upper_l_leg_angles_arr = []
        upper_r_leg_angles_arr = []

        lower_l_arm_angles_arr = []
        lower_r_arm_angles_arr = []
        lower_l_leg_angles_arr = []
        lower_r_leg_angles_arr = []

        for i in range(len(coordinates['x'])):
            head_angle_degrees = self.__calculate_angle_deg(nose_x_coord[i], nose_y_coord[i], nose_z_coord[i],
                                                        mid_shoulder_x_coord[i], mid_shoulder_y_coord[i], mid_shoulder_z_coord[i],
                                                        mid_hip_x_coord[i], mid_hip_y_coord[i], mid_hip_z_coord[i])
            head_angles_arr.append(head_angle_degrees+20)

            upper_l_arm_angle_degrees = self.__calculate_angle_deg(l_hip_x_coord[i], l_hip_y_coord[i], l_hip_z_coord[i],
                                                        l_shoulder_x_coord[i], l_shoulder_y_coord[i], l_shoulder_z_coord[i],
                                                        l_elbow_x_coord[i], l_elbow_y_coord[i], l_elbow_z_coord[i])
            upper_l_arm_angles_arr.append(upper_l_arm_angle_degrees)
        
            upper_r_arm_angle_degrees = self.__calculate_angle_deg(r_hip_x_coord[i], r_hip_y_coord[i], r_hip_z_coord[i],
                                                        r_shoulder_x_coord[i], r_shoulder_y_coord[i], r_shoulder_z_coord[i],
                                                        r_elbow_x_coord[i], r_elbow_y_coord[i], r_elbow_z_coord[i])
            upper_r_arm_angles_arr.append(upper_r_arm_angle_degrees)

            trunk_angle_degrees = self.__calculate_angle_deg(mid_shoulder_x_coord[i], mid_shoulder_y_coord[i], mid_shoulder_z_coord[i],
                                                        mid_hip_x_coord[i], mid_hip_y_coord[i], mid_hip_z_coord[i],
                                                        mid_knee_x_coord[i], mid_knee_y_coord[i], mid_knee_z_coord[i])
            trunk_angles_arr.append(trunk_angle_degrees)

            upper_l_leg_angle_degrees = self.__calculate_angle_deg(l_shoulder_x_coord[i], l_shoulder_y_coord[i], l_shoulder_z_coord[i],
                                                        l_hip_x_coord[i], l_hip_y_coord[i], l_hip_z_coord[i],
                                                        l_knee_x_coord[i], l_knee_y_coord[i], l_knee_z_coord[i])
            upper_l_leg_angles_arr.append(upper_l_leg_angle_degrees)
        
            upper_r_leg_angle_degrees = self.__calculate_angle_deg(r_shoulder_x_coord[i], r_shoulder_y_coord[i], r_shoulder_z_coord[i],
                                                        r_hip_x_coord[i], r_hip_y_coord[i], r_hip_z_coord[i],
                                                        r_knee_x_coord[i], r_knee_y_coord[i], r_knee_z_coord[i])
            
            upper_r_leg_angles_arr.append(upper_r_leg_angle_degrees)

            lower_l_arm_angle_degrees = self.__calculate_angle_deg(l_shoulder_x_coord[i], l_shoulder_y_coord[i], l_shoulder_z_coord[i],
                                                        l_elbow_x_coord[i], l_elbow_y_coord[i], l_elbow_z_coord[i],
                                                        l_wrist_x_coord[i], l_wrist_y_coord[i], l_wrist_z_coord[i])
            lower_l_arm_angles_arr.append(lower_l_arm_angle_degrees)
        
            lower_r_arm_angle_degrees = self.__calculate_angle_deg(r_shoulder_x_coord[i], r_shoulder_y_coord[i], r_shoulder_z_coord[i],
                                                        r_elbow_x_coord[i], r_elbow_y_coord[i], r_elbow_z_coord[i],
                                                        r_wrist_x_coord[i], r_wrist_y_coord[i], r_wrist_z_coord[i])
            lower_r_arm_angles_arr.append(lower_r_arm_angle_degrees)

            lower_l_leg_angle_degrees = self.__calculate_angle_deg(l_hip_x_coord[i], l_hip_y_coord[i], l_hip_z_coord[i],
                                                        l_knee_x_coord[i], l_knee_y_coord[i], l_knee_z_coord[i],
                                                        l_ankle_x_coord[i], l_ankle_y_coord[i], l_ankle_z_coord[i])
            lower_l_leg_angles_arr.append(lower_l_leg_angle_degrees)
        
            lower_r_leg_angle_degrees = self.__calculate_angle_deg(r_hip_x_coord[i], r_hip_y_coord[i], r_hip_z_coord[i],
                                                        r_knee_x_coord[i], r_knee_y_coord[i], r_knee_z_coord[i],
                                                        r_ankle_x_coord[i], r_ankle_y_coord[i], r_ankle_z_coord[i])
            lower_r_leg_angles_arr.append(lower_r_leg_angle_degrees)

        return(self.__write_angles_to_csv(head_angles_arr, trunk_angles_arr, upper_l_arm_angles_arr, upper_r_arm_angles_arr, upper_l_leg_angles_arr, 
                            upper_r_leg_angles_arr, lower_l_arm_angles_arr, lower_r_arm_angles_arr, lower_l_leg_angles_arr, lower_r_leg_angles_arr, out_path))