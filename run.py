
import os, json
import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    return False

def generate_base_plot():
    fig = plt.figure(figsize=(15,10))
    ax = plt.axes()
    plt.grid()
    plt.xlim([0,30])
    plt.ylim([0,17])
    ax.set_xticks(np.arange(0, 30, 1))
    ax.set_yticks(np.arange(0, 17, 1))

    return plt

def point_to_segment_projection(point, segment, verbose=False):
    projection = 0.0
    projected_point = None

    # Re-origin points for vector calculations
    S, P = np.subtract(segment[1], segment[0]), np.subtract(point, segment[0])

    # Determine projection
    norm_S = S / np.sqrt(S.dot(S)) # the normal vector of S
    projection = P.dot(norm_S) # the projection of P onto S
    magnitude_S = np.sqrt(S.dot(S))

    if verbose: print(f"...projection is {projection}")

    # We have a projection onto this segment
    #if projection <= magnitude_S:
    projected_point = segment[0] + (projection * norm_S) # add back origin
    if verbose: print(f"...point successfully projected to {projected_point}")

    return projection, projected_point, magnitude_S

# Should replace this search by a kd-tree search as the full loop is too inefficient
def check_intersection(projection_line, all_segs):
    for S_idx in range(len(all_segs) - 1):
        S1, S2 = all_segs[S_idx], all_segs[S_idx + 1]
        print(f"projection line {projection_line} intersection with segment {[S1, S2]}")
        A = {'x': projection_line[0][0], 'y': projection_line[0][1]}
        B = {'x': projection_line[1][0], 'y': projection_line[1][1]}
        C = {'x': S1[0], 'y': S1[1]}
        D = {'x': S2[0], 'y': S2[1]}
        intersection = ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
        if intersection:
            return True
    return False

# Segment intersection check, note this doesn't handle colinear segments or overlapping segments, more work needed!
def ccw(A,B,C):
    return (C['y']-A['y']) * (B['x']-A['x']) > (B['y']-A['y']) * (C['x']-A['x'])

# End segments/points are missing their projections, they should connect to the points 
def projection_by_segment_walk(ref_line, proj_line, verbose=False):
    projections = list()

    # We only need to look at each point for projection, hold the current segment seperately
    current_S = 0
    for P in proj_line:
        for S_idx in range(current_S, len(ref_line) - 1):
            # Grab the current segment we are working with
            S1, S2 = ref_line[S_idx], ref_line[S_idx + 1]

            # Project the current point onto a segment
            projection, projected_point, magnitude_S = point_to_segment_projection(P, [S1, S2])

            if verbose:
                print(f"******* Working on point: {P}, segment: {[S1, S2]}")

            # Check if the projection intersects with another segment on the projecting line
            if projection < 0: # The point is before this segment, go to next point, stay on the same segment
                if verbose:
                    print(f"   projection NEGATIVE, check intersections first")

                any_intersections = check_intersection([P,S1], proj_line[:S_idx])
                if any_intersections:
                    if verbose:
                        print('...found intersecting projection, moving to next segment')
                    current_S += 1
                else:
                    projections.append([P, S1])
                    break

            if projection > 0 and projection < magnitude_S: # Sweet spot, we have a valid projection
                projections.append([P, projected_point])
                if verbose:
                    print(f"   projection OK, projecting to segment at point {projected_point}")
                break

            if projection > magnitude_S: # The point is after this segment, go to next segment, keep same point
                if verbose:
                    print("   projection TOO LARGE, moving to next segment")
                current_S += 1

    return projections

def run():
    data_file = os.path.join(os.getcwd(), "sample-data", "sample-data.json")
    data = load_data(data_file)
    
    plt = generate_base_plot()

    l1, l2 = data['lines'][0], data['lines'][1]
    l1.reverse()
    l2.reverse()
    l1_x, l1_y = [p[0] for p in l1], [p[1] for p in l1]
    l2_x, l2_y = [p[0] for p in l2], [p[1] for p in l2]
    plt.plot(l1_x, l1_y, 'go-')
    plt.plot(l2_x, l2_y, 'ro-')

    projections = projection_by_segment_walk(l2, l1, verbose=True)
    projections2 = projection_by_segment_walk(l1, l2, verbose=True)

    for p in projections:
        plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], 'bo--')
        plt.annotate(f"({p[0][0]},{p[0][1]})", (p[0][0], p[0][1]), textcoords="offset points", xytext=(0,15), ha='center', color='green')
        plt.annotate(f"({p[1][0]:.2f},{p[1][1]:.2f})", (p[1][0], p[1][1]), textcoords="offset points", xytext=(0,-25), ha='center', color='green')
  
    for p in projections2:
        plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], 'mo--')
        plt.annotate(f"({p[0][0]},{p[0][1]})", (p[0][0], p[0][1]), textcoords="offset points", xytext=(0,15), ha='center', color='magenta')
        plt.annotate(f"({p[1][0]:.2f},{p[1][1]:.2f})", (p[1][0], p[1][1]), textcoords="offset points", xytext=(0,-25), ha='center', color='magenta')

    print("Done")

    plt.show()

if __name__ == "__main__":
    run()