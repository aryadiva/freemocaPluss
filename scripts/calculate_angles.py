import configparser
import csv
import numpy as np

from REBA.calculate_reba import DegreetoREBA
class CalculateAngles:
    def __init__(self):
        self.config_check_path = "config_check.ini"
        pass

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_check_path)
        
        option_values = []
        for key, value in config.items('DEFAULT'):
            if value.lower() == 'unchecked':
                option_values.append(False)
            elif value.lower() == 'checked':
                option_values.append(True)
            else:
                option_values.append(value)
        
        return option_values

    def read_coordinates_from_csv(self, file_path, columns):
        coordinates = {key: [] for key in columns}
        
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Read the header
            for row in csv_reader:
                for key, (x_col, y_col, z_col) in columns.items():
                    try:
                        coordinates[key].append((float(row[x_col]), float(row[y_col]), float(row[z_col])))
                    except IndexError as e:
                        print(f"Error with row: {row}, key: {key}, columns: {(x_col, y_col, z_col)}")
                        raise e
        return coordinates

    def write_angles_to_csv(self, angles_dict, out_path):
        with open(out_path, 'w', newline='') as csv_file:
            csvwriter = csv.writer(csv_file)
            headers = list(angles_dict.keys())
            csvwriter.writerow(headers)
            
            for row in zip(*angles_dict.values()):
                csvwriter.writerow(row)

    def calculate_angle_deg(self, p1, p2, p3):
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)
        dot_product = np.dot(v1, v2)
        angle_radians = np.arccos(dot_product / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        return np.degrees(angle_radians)

    def calculate_and_transform_angle(self, p1, p2, p3):
        return 180 - self.calculate_angle_deg(p1, p2, p3)
    
    def calculate_reba(self, angles_dict, i):
        def append_reba(tf, data, param):
            if tf:
                calc_reba = DegreetoREBA(data + [param])
                angles_dict['REBA'].append(calc_reba)

        if self.dataTF[0]:
            base_data = [
                angles_dict['neck'][i], self.dataTF[3], self.dataTF[4],
                angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6],
                angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                self.dataTF[0], angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i],
                self.dataTF[7], self.dataTF[8], self.dataTF[9], angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10]
            ]
            append_reba(self.dataTF[11], base_data, 0)
            append_reba(self.dataTF[12], base_data, 1)
            append_reba(self.dataTF[13], base_data, 2)
            append_reba(self.dataTF[14], base_data, 3)

        if self.dataTF[1]:
            base_data = [
                angles_dict['neck'][i], self.dataTF[3], self.dataTF[4],
                angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6],
                angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                self.dataTF[1], angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i],
                self.dataTF[7], self.dataTF[8], self.dataTF[9], angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10]
            ]
            append_reba(self.dataTF[11], base_data, 0)
            append_reba(self.dataTF[12], base_data, 1)
            append_reba(self.dataTF[13], base_data, 2)
            append_reba(self.dataTF[14], base_data, 3)

        if self.dataTF[2]:
            base_data = [
                angles_dict['neck'][i], self.dataTF[3], self.dataTF[4],
                angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6],
                angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                self.dataTF[2], angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i],
                self.dataTF[7], self.dataTF[8], self.dataTF[9], angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10]
            ]
            append_reba(self.dataTF[11], base_data, 0)
            append_reba(self.dataTF[12], base_data, 1)
            append_reba(self.dataTF[13], base_data, 2)
            append_reba(self.dataTF[14], base_data, 3)

    def main(self, file_path, out_path):
        self.calc_angles = CalculateAngles()
        self.dataTF = self.calc_angles.read_config()

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
            'r_ankle': (84, 85, 86),
            'l_index': (57, 58, 59),
            'r_index': (60, 61, 62)
        }

        coordinates = self.read_coordinates_from_csv(file_path, columns)

        # Calculate mid points
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
            'lower_right_leg': [],
            'left_wrist': [],
            'right_wrist': [],
            'REBA': []
        }
        #print("Asumming all limbs condition doesn't require adjustments since initial weight isn't checked")
        for i in range(len(coordinates['nose'])):
            angles_dict['neck'].append(self.calculate_and_transform_angle(
                coordinates['nose'][i], mid_shoulder[i], mid_hip[i])-35)
            angles_dict['trunk'].append(self.calculate_and_transform_angle(
                mid_shoulder[i], mid_hip[i], mid_knee[i]))
            angles_dict['upper_left_arm'].append(self.calculate_angle_deg(
                coordinates['l_hip'][i], coordinates['l_shoulder'][i], coordinates['l_elbow'][i]))
            angles_dict['upper_right_arm'].append(self.calculate_angle_deg(
                coordinates['r_hip'][i], coordinates['r_shoulder'][i], coordinates['r_elbow'][i]))
            angles_dict['upper_left_leg'].append(self.calculate_and_transform_angle(
                coordinates['l_shoulder'][i], coordinates['l_hip'][i], coordinates['l_knee'][i]))
            angles_dict['upper_right_leg'].append(self.calculate_and_transform_angle(
                coordinates['r_shoulder'][i], coordinates['r_hip'][i], coordinates['r_knee'][i]))
            angles_dict['lower_left_arm'].append(self.calculate_and_transform_angle(
                coordinates['l_shoulder'][i], coordinates['l_elbow'][i], coordinates['l_wrist'][i]))
            angles_dict['lower_right_arm'].append(self.calculate_and_transform_angle(
                coordinates['r_shoulder'][i], coordinates['r_elbow'][i], coordinates['r_wrist'][i]))
            angles_dict['lower_left_leg'].append(self.calculate_and_transform_angle(
                coordinates['l_hip'][i], coordinates['l_knee'][i], coordinates['l_ankle'][i]))
            angles_dict['lower_right_leg'].append(self.calculate_and_transform_angle(
                coordinates['r_hip'][i], coordinates['r_knee'][i], coordinates['r_ankle'][i]))
            angles_dict['left_wrist'].append(self.calculate_and_transform_angle(
                coordinates['l_elbow'][i], coordinates['l_wrist'][i], coordinates['l_index'][i]))
            angles_dict['right_wrist'].append(self.calculate_and_transform_angle(
                coordinates['r_elbow'][i], coordinates['r_wrist'][i], coordinates['r_index'][i]))
            # default is 0
            angles_dict['REBA'].append(0)
            #self.calculate_reba(angles_dict, i)
            
            # if self.dataTF[0] is True:
            #         if self.dataTF[11] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[0],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 0
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[12] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[0],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 1
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[13] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[0],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 2
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[14] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[0],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 3
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         else:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 False,
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 0
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            # if self.dataTF[1] is True:
            #         if self.dataTF[11] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[1],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 0
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[12] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[1],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 1
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[13] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[1],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 2
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[14] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[1],
            #                angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 3
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         else:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 False,
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 0
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            # if self.dataTF[2] is True:
            #         if self.dataTF[11] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[2],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 0
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[12] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[2],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 1
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[13] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[2],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 2
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         if self.dataTF[14] is True:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 self.dataTF[2],
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 3
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            #         else:
            #             calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
            #                 angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 False,
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
            #                 0
            #                 ])
            #             angles_dict['REBA'].append(calc_reba)
            # else:
            #     print("Asumming all limbs condition doesn't require adjustments since initial weight isn't checked")
            #     calc_reba = DegreetoREBA([
            #                 angles_dict['neck'][i], False, False, 
            #                 angles_dict['trunk'][i], False, False, 
            #                 angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
            #                 False,
            #                 angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], False, False, False,
            #                 angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
            #                 angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], False,
            #                 0
            #                 ])
            #     angles_dict['REBA'].append(calc_reba)

        self.write_angles_to_csv(angles_dict, out_path)

# angles_csv_path = "C:\\Users\\Arya\\freemocap_data\\recording_sessions\\session_2024-06-03_12_30_30\\recording_12_35_58_gmt+8\\output_data\\mediapipe_body_3d_xyz.csv"
# out_path = "C:\\Users\\Arya\\freemocap_data\\recording_sessions\\session_2024-06-03_12_30_30\\recording_12_35_58_gmt+8\\output_data\\angles.csv"

# calc_angles = CalculateAngles()
# data = calc_angles.read_config()
# calc_angles.main(angles_csv_path, out_path)
#print(data[1])