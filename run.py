
import os, json
import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    return False

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
    l1_x, l1_y = [p[0] for p in l1], [p[1] for p in l1]
    l2_x, l2_y = [p[0] for p in l2], [p[1] for p in l2]
    for i in range(len(l1_x) - 1):
        plt.plot(l1_x, l1_y, 'bo-')
        plt.plot(l2_x, l2_y, 'ro-')

    current_p = 0
    for i in range(len(l2) - 1): # for each segment in the reference line
        print(f"Segment {i} on reference line: ({l2[i]},{l2[i+1]})")
        s1, s2 = l2[i], l2[i+1]
        
        while current_p < len(l1):
            p = l1[current_p]
            has_projection, proj, dbv = point_projection([s1, s2], p)

            print(f"At index {current_p} Point {p}: {has_projection}")

            if has_projection and not dbv:
                p_x1, p_x2 = proj[0][0], proj[1][0]
                p_y1, p_y2 = proj[0][1], proj[1][1]
                plt.plot([p_x1, p_x2], [p_y1, p_y2], 'go--')
                current_p = current_p + 1
            elif dbv: # don't plot a double vertex, handle it in the reverse pass
                current_p = current_p + 1
            else:
                break
    '''current_p = 0
    for i in range(len(l1) - 1): # for each segment in the reference line
        print(f"Segment {i} on reference line: ({l1[i]},{l1[i+1]})")
        s1, s2 = l1[i], l1[i+1]
        
        while current_p < len(l2):
            p = l2[current_p]
            has_projection, proj, dbv = point_projection([s1, s2], p)

            print(f"At index {current_p} Point {p}: {has_projection}")

            if has_projection and not dbv:
                p_x1, p_x2 = proj[0][0], proj[1][0]
                p_y1, p_y2 = proj[0][1], proj[1][1]
                plt.plot([p_x1, p_x2], [p_y1, p_y2], 'yo--')
                current_p = current_p + 1
            elif dbv: # don't plot a double vertex, handle it in the reverse pass
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