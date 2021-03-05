
import os, json
import numpy as np
import matplotlib.pyplot as plt

def plot_pts(points, color, thickness):
    pass

def get_parallel_line(l1):
    pass

def point_projection(segment, p):

    # transform segment and point to be vectors from origin
    x0, y0 = segment[0]
    x1, y1 = segment[1][0] - x0, segment[1][1] - y0
    px, py = p[0] - x0, p[1] - y0
    projected_point = [x0, y0] # start the projection at the origin

    #print(f"orgin: ({x0},{y0}), segment: ({x1},{y1}), point: ({px},{py})")

    # S: Line segment vector to project onto, P: Vector from origin to point p
    S, P = np.array([x1,y1]), np.array([px, py])

    # Scalar projection of P onto S given by P . (S / ||S||)
    norm_S = S / np.sqrt(S.dot(S)) # the normal vector of S
    proj = P.dot(norm_S) # the projection of P onto S

    # Add back the origin translation to the projected point
    projected_point = projected_point + (proj * norm_S)

    return projected_point
    


    
    '''# get points for line segment
    x1, x2 = segment[0][0], segment[1][0]
    y1, y2 = segment[0][1], segment[1][1]
    x_p, y_p = p[0], p[1]

    # get equation of line segment: y = mx + b
    m = (y2-y1)/(x2-x1)
    b = y1 - (x1 * m)

    print(b)

    # determine equation for perpendicular line
    m_perp = -(1 / m)
    b_perp = y_p - (x_p * m_perp)

    s = [y2 - y1, x2 - x1]'''




    

def get_intersection_points(l1, l2):
    pass

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    return False

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

    l1, l2 = data['lines'][0], data['lines'][1]
    l1_x, l1_y = [p[0] for p in l1], [p[1] for p in l1]
    l2_x, l2_y = [p[0] for p in l2], [p[1] for p in l2]
    for i in range(len(l1_x) - 1):
        plt.plot(l1_x, l1_y, 'bo-')
        plt.plot(l2_x, l2_y, 'ro-')

    proj = point_projection(l2[0:2],l1[0])
    proj2 = point_projection(l2[0:2],l1[1])
    proj3 = point_projection(l2[0:2],l1[2])

    plt.plot(proj[0], proj[1], 'go-')
    plt.plot(proj2[0], proj2[1], 'go-')
    plt.plot(proj3[0], proj3[1], 'go-')

    plt.show()

    
    # Plot lines, using different colors and thicknesses

    # Step 1: Add all intersection points

    # Step 2: Sweep lines
        # a. start 

    # project all points from one line onto another

    pass

if __name__ == "__main__":
    run()