import numpy as np
import neck_reba_score as RebaNeck
import trunk_reba_score as RebaTrunk
import leg_reba_score as RebaLeg

class DegreetoREBA:
    def __init__(self, joints_degree):
        self.joints_degree = joints_degree

    def reba_table_a(self):
        return np.array([
            [[1, 2, 3, 4], [2, 3, 4, 5], [2, 4, 5, 6], [3, 5, 6, 7], [4, 6, 7, 8]],
            [[1, 2, 3, 4], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9]],
            [[3, 3, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9], [7, 8, 9, 9]]
        ])
    def reba_computation(self):
        table_a = self.reba_table_a()

        # step1: locate neck position
        neck_degrees = self.joints_degree[0]
        m_neck_REBA = RebaNeck.NeckREBA(neck_degrees)
        neck_scores = m_neck_REBA.neck_reba_score()

        # step2: locate trunck posture
        trunk_degrees = self.joints_degree[1]
        m_trunk_REBA = RebaTrunk.TrunkREBA(trunk_degrees)
        trunk_scores = m_trunk_REBA.trunk_reba_score()

        # step3: locate legs
        leg_degrees = [self.joints_degree[2], self.joints_degree[3]]
        m_leg_REBA = RebaLeg.LegREBA(leg_degrees)
        leg_scores = m_leg_REBA.leg_reba_score()
        # leg_scores =[1]

        # step 4: Look up score in table _A
        if neck_scores[0] - 1>2:
            neck_scores[0] = 3
        if trunk_scores[0] - 1>4:
            trunk_scores[0]  = 5
        if leg_scores[0] - 1>3:
            leg_scores[0] = 4
        
        posture_score_a = table_a[neck_scores[0] - 1][trunk_scores[0] - 1][leg_scores[0] - 1]

        # step 5: load score
        # load = input("what is the load(in kg) ")
        # load = 0
        # if 5 <= int(load) < 10:
        #     posture_score_a = posture_score_a + 1
        # if 10 <= int(load):
        #     posture_score_a = posture_score_a + 2

        return(f"Score for table A is: {posture_score_a}")
    
joints_degree = [30, 80, 20, 15]
classA_obj = DegreetoREBA(joints_degree)
A_reba_score = classA_obj.reba_computation()
print(A_reba_score)