class WristREBA:
    # For calculating REBA score based on degrees
    def __init__(self, r_wrist_degree, l_wrist_degree, bent):
        self.r_wrist_degree = r_wrist_degree
        self.l_wrist_degree = l_wrist_degree
        self.bent = bent

    def wrist_reba_score(self):
        wrist_reba_score = 0
        # wrist_flex_score = 0
        # wrist_side_bend_score = 0
        # wrist_torsion_score = 0

        right_wrist = self.r_wrist_degree
        left_wrist = self.l_wrist_degree
        bent = self.bent

        if right_wrist > left_wrist:
            if -15 <= right_wrist < 15:
                wrist_reba_score += 1
                # wrist_flex_score += 1
            if 15 <= right_wrist or right_wrist < -15:
                wrist_reba_score += 2
                # wrist_flex_score += 2
        else:
            if -15 <= left_wrist < 15:
                wrist_reba_score += 1
                # wrist_flex_score += 1
            if 15 <= left_wrist or left_wrist < -15:
                wrist_reba_score += 2
                # wrist_flex_score += 2

        if bent is True :
            wrist_reba_score += 1
            # wrist_side_bend_score += 1

        # if right_twist != 0 or left_twist !=0 :
        #     wrist_torsion_score +=1
        #     wrist_reba_score += 1

        return wrist_reba_score