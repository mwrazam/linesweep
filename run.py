
import os, json
import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    return False

def intersects(segment1, segment2):

    # Segments are coincident
    if segment1 == segment2:
        return False

    # Segments are parallel

    # Calculate intersection if it exists

def project_line(proj_line, ref_line, verbose=True):
    # Collate points that project and double vertices seperately
    projections, double_vertices = list(), list()

    p_line = proj_line.copy()

    # Project points of l2 onto segments of l1
    for i in range(len(ref_line) - 1):
        S1, S2 = ref_line[i], ref_line[i+1] # Reference line segment

        if verbose: print(f"Reference line segment: ({S1}, {S2})")

        # Re-origin reference line segments
        S = np.array(np.subtract(S2,S1))

        for i, P in enumerate(p_line):
            # Re-origin point
            P = np.array(np.subtract(P,S1))

            # Determine projection
            norm_S = S / np.sqrt(S.dot(S)) # the normal vector of S
            proj = P.dot(norm_S) # the projection of P onto S

            print(f"{i}: Projecting ({np.add(P,S1)}) onto ({S1}, {S2})...")

            if proj <= np.sqrt(S.dot(S)):
                p_line.pop(i)
                if proj >= 0:
                    if verbose: print(f"...Yay projection!")
                    projected_point = S1 + (proj * norm_S)
                    projections.append([np.add(P, S1), projected_point])
                    break
                else:
                    if verbose: print(f"... No good, Projection is negative...")
                    double_vertices.append([np.add(P, S1), S1])
                    break
            else:
                if verbose: print(f"...Projection too large, out of bounds!")
                break

    return projections, double_vertices

# @segment: 2 point list of start and end points comprising segment
# @p : The point we want to project onto the segment
def point_projection(segment, p):
    projection = None
    has_projection = False # if the projection is outside of the segment, we can't project it
    double_vertex = False # if we get this, we just proceed in the list and ignore this point

    # Transform both into vectors, re-origin for vector calculations
    S, P = np.array(np.subtract(segment[1],segment[0])), np.array(np.subtract(p,segment[0]))

    # Determine projection
    norm_S = S / np.sqrt(S.dot(S)) # the normal vector of S
    proj = P.dot(norm_S) # the projection of P onto S

    if proj <= 0:
        double_vertex = True

    if proj <= np.sqrt(S.dot(S)):
        has_projection = True
        projected_point = segment[0] + (proj * norm_S) # add back origin
        projection = [p, projected_point]

    return has_projection, projection, double_vertex

def projection_walk(ref_line, proj_line):

    # Determine start end point for projections
    start_distances = list()
    end_distances = list()
    for j in proj_line:
        start_v_x, start_v_y = j[0] - ref_line[0][0], j[1] - ref_line[0][1]
        start_distances.append(np.sqrt(start_v_x**2 + start_v_y**2))
        end_v_x, end_v_y = j[0] - ref_line[-1][0], j[1] - ref_line[-1][1]
        end_distances.append(np.sqrt(end_v_x**2 + end_v_y**2))

    # The smallest distance is now our 
    start_idx, end_idx = np.argmin(start_distances), np.argmin(end_distances)

    # Evaluate over all segments on the reference line
    current = start_idx
    for i in range(len(ref_line) - 1):
        S1, S2 = ref_line[i], ref_line[i+1]

        for j in range(start_idx, end_idx):
            P = proj_line[current]
            proj, mag_S = point_to_segment_projection(P, [S1, S2])

            if proj > mag_S:
                break

            current += 1
            print(f"Projecting point: {P} onto segment: {S1} --- {S2} value is: {proj}, and S magnitude: {mag_S}")



def point_to_segment_projection(point, segment):
    projection = 0.0
    # Re-origin points for vector calculations
    S, P = np.subtract(segment[1], segment[0]), np.subtract(point, segment[0])

    # Determine projection
    norm_S = S / np.sqrt(S.dot(S)) # the normal vector of S
    projection = P.dot(norm_S) # the projection of P onto S

    magnitude_S = np.sqrt(S.dot(S))

    return projection, magnitude_S




def run():
    data_file = os.path.join(os.getcwd(), "sample-data", "sample-data.json")
    data = load_data(data_file)
    
    fig = plt.figure(figsize=(15,10))
    
    ax = plt.axes()
    plt.grid()
    plt.xlim([0,30])
    plt.ylim([0,17])
    ax.set_xticks(np.arange(0, 30, 1))
    ax.set_yticks(np.arange(0, 17, 1))

    #l1, l2 = np.array(data['lines'][0]), np.array(data['lines'][1])
    l1, l2 = data['lines'][0], data['lines'][1]
    l1.reverse()
    l2.reverse()
    l1_x, l1_y = [p[0] for p in l1], [p[1] for p in l1]
    l2_x, l2_y = [p[0] for p in l2], [p[1] for p in l2]
    for i in range(len(l1_x) - 1):
        plt.plot(l1_x, l1_y, 'bo-')
        plt.plot(l2_x, l2_y, 'ro-')

    projection_walk(l2, l1)


    #proj, dbv = project_line(l1, l2, verbose=True)
    #for l in proj:
    #    print(l)

    '''# FORWARD PASS
    current_p = 0
    for i in range(len(l2) - 1): # for each segment in the reference line
        print(f"Segment {i} on reference line: ({l2[i]},{l2[i+1]})")
        s1, s2 = l2[i], l2[i+1]
        
        while current_p < len(l1):
            p = l1[current_p]
            has_projection, proj, dbv = point_projection([s1, s2], p)

            print(f"At index {current_p} Point {p}: {has_projection}")

            if has_projection:
                p_x1, p_x2 = proj[0][0], proj[1][0]
                p_y1, p_y2 = proj[0][1], proj[1][1]
                if dbv:
                    plt.plot([p_x1, p_x2], [p_y1, p_y2], 'mo--')
                else:
                    plt.plot([p_x1, p_x2], [p_y1, p_y2], 'go:')
                current_p = current_p + 1
            else:
                break'''

    # FLIP PASS
    '''current_p = 0
    for i in range(len(l1) - 1): # for each segment in the reference line
        print(f"Segment {i} on reference line: ({l1[i]},{l1[i+1]})")
        s1, s2 = l1[i], l1[i+1]
        
        while current_p < len(l2):
            p = l2[current_p]
            has_projection, proj, dbv = point_projection([s1, s2], p)

            print(f"At index {current_p} Point {p}: {has_projection} dbv: {dbv}")

            if has_projection and not dbv:
                p_x1, p_x2 = proj[0][0], proj[1][0]
                p_y1, p_y2 = proj[0][1], proj[1][1]
                plt.plot([s1[0],p[0]], [s1[1],p[1]], 'mo--')
                current_p = current_p + 1
            else:
                break'''
    
    

    plt.show()

    
    # Plot lines, using different colors and thicknesses

    # Step 1: Add all intersection points

    # Step 2: Sweep lines
        # a. start 

    # project all points from one line onto another

if __name__ == "__main__":
    run()