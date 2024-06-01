class LegREBA:
    def __init__(self, r_leg_degrees, l_leg_degrees):
        self.r_leg_degrees = r_leg_degrees
        self.l_leg_degrees = l_leg_degrees

    def leg_reba_score(self):
        leg_reba_score = 0
        right_leg_degree = self.r_leg_degrees
        left_leg_degree = self.l_leg_degrees

        if right_leg_degree >= right_leg_degree:
            if right_leg_degree < 30:
                leg_reba_score = leg_reba_score + 1
            if 30 <= right_leg_degree < 60:
                leg_reba_score = leg_reba_score + 1
            if 60 <= right_leg_degree:
                leg_reba_score = leg_reba_score + 2

        else:
            if left_leg_degree < 30:
                leg_reba_score = leg_reba_score + 1
            if 30 <= left_leg_degree < 60:
                leg_reba_score = leg_reba_score + 1
            if 60 <= left_leg_degree:
                leg_reba_score = leg_reba_score + 2

        return leg_reba_score