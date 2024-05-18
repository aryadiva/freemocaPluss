from scripts.calculate_angles import CalculateAngles
#from freemocap.data_layer.recording_models.recording_info_model import 
import pathlib as path

file_path = 'C:\\Users\\Arya\\freemocap_data\\recording_sessions\\sample1\\output_data\\mediapipe_body_3d_xyz.csv'  # CSV file path
out_path = 'C:\\Users\\Arya\\OneDrive - Universiti Sains Malaysia\\Final Year\\CAT405\\Project_Final\\out_angle5.csv'

calc_angles=CalculateAngles()
calc_angles.main(file_path, out_path)

