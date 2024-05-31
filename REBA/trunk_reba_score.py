class TrunkREBA:
    def __init__(self, trunk_degrees, twisted, side_bending):
        self.trunk_degrees = trunk_degrees
        self.twisted = twisted
        self.side_bending = side_bending

    def trunk_reba_score(self):

        trunk_flex_degree = self.trunk_degrees
        trunk_twist = self.twisted
        trunk_side_bend = self.side_bending
        # trunk_side_bending_degree = self.trunk_degrees[1]
        # trunk_torsion_degree = self.trunk_degrees[2]

        trunk_reba_score = 0

        if trunk_flex_degree >= 0:
            # means flexion
            if 0 <= trunk_flex_degree < 5:
                trunk_reba_score += 1
                #trunk_flex_score += 1
            elif 5 <= trunk_flex_degree < 20:
                trunk_reba_score += 2
                #trunk_flex_score += 2
            elif 20 <= trunk_flex_degree < 60:
                trunk_reba_score += 3
                #trunk_flex_score += 3
            elif 60 <= trunk_flex_degree:
                trunk_reba_score += 4
                #trunk_flex_score += 4
        else:
            # means extension
            if 0 <= abs(trunk_flex_degree) < 5:
                trunk_reba_score += 1
                #trunk_flex_score += 1
            elif 5 <= abs(trunk_flex_degree) < 20:
                trunk_reba_score += 2
                #trunk_flex_score += 2
            elif 20 <= abs(trunk_flex_degree):
                trunk_reba_score += 3
                #trunk_flex_score += 3

        if trunk_twist is True:
            trunk_reba_score += 1
            #trunk_side_score += 1
        if trunk_side_bend is True >= 1:
            trunk_reba_score += 1
            #trunk_torsion_score += 1

        return trunk_reba_score