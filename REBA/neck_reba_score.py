class NeckREBA:
    def __init__(self, neck_degrees, lateral_flex_degree, twist_degree):
        self.neck_degrees = neck_degrees
        self.lateral_flex_degree = lateral_flex_degree
        self.twist_degree = twist_degree

    def neck_reba_score(self):
        neck_flex_degree = self.neck_degrees
        lateral_flex_degree = self.lateral_flex_degree
        twist_degree = self.twist_degree

        neck_reba_score = 0
        neck_flex_score = 0
        neck_lateral_flex_score = 0
        neck_twist_score = 0

        # neck is either in flexion/extension
        if neck_flex_degree >= 0:
            if 0 <= neck_flex_degree < 20:
                neck_reba_score += 1
                neck_flex_score += 1
            if 20 <= neck_flex_degree:
                neck_reba_score += 2
                neck_flex_score += 2
        else:
            # neck is in extension
            neck_reba_score += 2
            neck_flex_score += 2

        # Lateral flexion scoring
        if abs(lateral_flex_degree) >= 1:
            neck_reba_score += 1
            neck_lateral_flex_score += 1
            if abs(lateral_flex_degree) > 20:
                neck_reba_score += 1
                neck_lateral_flex_score += 1

        # Twist scoring
        if abs(twist_degree) >= 1:
            neck_reba_score += 1
            neck_twist_score += 1

        return [neck_reba_score]