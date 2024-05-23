import numpy as np

class CalculateAngles2:
    def __init__(self):
        pass
    
    def calculate_angle_deg(self, vec1, vec2):
        # Calculate angle between two vectors in degrees
        unit_vec1 = vec1 / np.linalg.norm(vec1)
        unit_vec2 = vec2 / np.linalg.norm(vec2)
        dot_product = np.dot(unit_vec1, unit_vec2)
        angle_rad = np.arccos(dot_product)
        angle_deg = np.degrees(angle_rad)
        return angle_deg

    def calculate_twist_bend_angles(self, nose, mid_shoulder, l_shoulder, r_shoulder):
        # Calculate neck side bending (left/right flexion)
        neck_vector = nose - mid_shoulder
        vertical_vector = np.array([0, 1, 0])  # Assuming the vertical direction is the y-axis
        lateral_flex_angle = self.calculate_angle_deg(neck_vector, vertical_vector)

        # Simplified assumption: use horizontal plane (ignoring z-component) for twist
        horizontal_neck_vector = neck_vector[:2]
        horizontal_shoulder_vector = (l_shoulder - r_shoulder)[:2]
        twist_angle = self.calculate_angle_deg(horizontal_neck_vector, horizontal_shoulder_vector)

        return lateral_flex_angle, twist_angle

# Test function with dummy data
def test_calculate_twist_bend_angles():
    calc_angles = CalculateAngles2()
    
    # Dummy data for testing
    nose = np.array([1, 2, 3])
    mid_shoulder = np.array([0, 2, 0])
    l_shoulder = np.array([-1, 2, 0])
    r_shoulder = np.array([1, 2, 0])
    
    lateral_flex_angle, twist_angle = calc_angles.calculate_twist_bend_angles(nose, mid_shoulder, l_shoulder, r_shoulder)
    
    print(f"Lateral Flexion Angle: {lateral_flex_angle}")
    print(f"Twist Angle: {twist_angle}")

# Run the test
if __name__ == "__main__":
    test_calculate_twist_bend_angles()
