class NeckREBA:
    def __init__(self, neck_degrees, twisted, side_bending):
        self.neck_degrees = neck_degrees
        self.twisted = twisted
        self.side_bending = side_bending
        # self.lateral_flex_degree = lateral_flex_degree
        # self.twist_degree = twist_degree

    def neck_reba_score(self):
        neck_flex_degree = self.neck_degrees
        neck_twist = self.twisted
        neck_side_bend = self.side_bending
        # lateral_flex_degree = self.lateral_flex_degree
        # twist_degree = self.twist_degree

        neck_reba_score = 0

        # neck is either in flexion/extension
        if neck_flex_degree >= 0:
            if 0 <= neck_flex_degree < 20:
                neck_reba_score += 1
                #neck_flex_score += 1
            if 20 <= neck_flex_degree:
                neck_reba_score += 2
                #neck_flex_score += 2
        else:
            # neck is in extension
            neck_reba_score += 2
            #neck_flex_score += 2

        # Lateral bend scoring
        if neck_twist is True:
            neck_reba_score += 1
            #neck_twist += 1

        # Twist scoring
        if neck_side_bend is True:
            neck_reba_score += 1
            #neck_twist_score += 1

        return [neck_reba_score]