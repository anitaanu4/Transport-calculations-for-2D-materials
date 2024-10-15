import sys
import re
import math
#import matplotlib.pyplot as plt

def get_real_lattice_vectors(filename):
    real_lattice_vectors = []
    try:
        with open(filename, 'r') as file:
            content = file.read()
            
            # Find the block using regular expressions
            block_pattern = r'%block\s+LatticeVectors\s+(.*?)\s+%endblock\s+LatticeVectors'
            block_match = re.search(block_pattern, content, re.DOTALL)
            
            if block_match:
                block_content = block_match.group(1)
                
                # Split the block content into lines
                lines = block_content.strip().split('\n')
                
                # Extract the first two numbers of the first two lines
                for line in lines[:2]:
                    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                    if len(numbers) >= 2:
                        real_lattice_vectors.extend([float(num) * 1.88973 for num in numbers[:2]])
                
            else:
                print("Error: Block not found in file.")
                
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    
    return real_lattice_vectors

def get_reciprocal_lattice_vectors(real_lattice_vectors):
    #this constructs the real lattice vectors according to wikipedia page for a reciprocal lattice. See the 2D section of https://en.wikipedia.org/wiki/Reciprocal_lattice
    reciprocal_lattice_vectors = [0, 0 , 0, 0]
    prefactor = 2 * math.pi / (real_lattice_vectors[1] * real_lattice_vectors[2] - real_lattice_vectors[0] * real_lattice_vectors[3])
    reciprocal_lattice_vectors[0] = - prefactor * real_lattice_vectors[3]    
    reciprocal_lattice_vectors[1] = prefactor * real_lattice_vectors[2]     
    reciprocal_lattice_vectors[2] = prefactor * real_lattice_vectors[1]     
    reciprocal_lattice_vectors[3] = - prefactor * real_lattice_vectors[0]     
    
    return reciprocal_lattice_vectors

def get_start_index(m):
    if m == 0:
        return 0
    if m == 1:
        return 7
    if m == 2:
        return 13
    if m == 3:
        return 18    
    if m == 4:
        return 22
    if m == 5:
        return 25
    if m == 6:
        return 27
    else:
        return None
        
    
def get_all_intercepts(h1, k1, reciprocal_lattice_vectors, intercept, m):
    i = 0
    p = 0
    start_index = get_start_index(m)
    for h2 in range(-1, 2, 1):
        for k2 in range(-1, 2, 1):
            if (((k2 != 0) or (h2 != 0)) and ((k1 != k2) or (h1 != h2))):
                if (i >= m):                   
                    #print("in if statement")
                    #this calculates the intercept between a single line
                    m1, b1 = get_slope_and_y_intercept(k1, h1, reciprocal_lattice_vectors)
                    m2, b2 = get_slope_and_y_intercept(k2, h2, reciprocal_lattice_vectors)
      #              print(m1, b1, m2, b2)    
                    #print("i = ", i, "m = ", m, start_index, p, h1, k1, h2, k2)
                    x_intercept, y_intercept =  calculate_intercept(m1, b1, m2, b2)
                    intercept[start_index + p][0] = x_intercept
                    intercept[start_index + p][1] = y_intercept
                    p = p + 1
     #               print(intercept[i]) 
                i = i + 1
    return intercept

def calculate_intercept(m1, b1, m2, b2):
    # Check if lines are parallel
    if (abs(m1 - m2) < 1e-8):
        #print("Lines are parallel, no intercept.")
        return 1000, 1000
    
    # Calculate x-coordinate of the intercept
    x_intercept = (b2 - b1) / (m1 - m2)
    
    # Calculate y-coordinate of the intercept using one of the lines
    y_intercept = m1 * x_intercept + b1
    
    return x_intercept, y_intercept

def get_indices(intercept_reordered):
    distance = [0 for _ in range(28)]
    for i in range(0, 28):
        distance[i] = intercept_reordered[i][0] * intercept_reordered[i][0] + intercept_reordered[i][1] * intercept_reordered[i][1]
        #print(intercept_reordered[i][0], intercept_reordered[i][1], distance[i], i)

    smallest_indices = [0, 1, 2, 3, 4, 5]
    #print("finding the smallest values")
    for i in range(6, 28):
        for j in range(0, 6):
            #print(i, j, smallest_indices[j], distance[i], distance[smallest_indices[j]])
            if ((distance[i] + 0.000001 < distance[smallest_indices[j]])):
                    #if (((abs(intercept_reordered[i][0]) -abs(intercept_reordered[smallest_indices[j]][0]) > 0.00000001) or 
                    #    (abs(intercept_reordered[i][1]) -abs(intercept_reordered[smallest_indices[j]][1]) > 0.00000001))):
                    #print("entered loop")
                    smallest_indices[j] = i
                    break

    return smallest_indices

def find_max_min_points(intercept):
    if not intercept:
        return None, None, None, None  # Return None if intercept is empty

    max_x = max(intercept, key=lambda x: x[0])[0]  # Maximum x-value
    min_x = min(intercept, key=lambda x: x[0])[0]  # Minimum x-value
    max_y = max(intercept, key=lambda x: x[1])[1]  # Maximum y-value
    min_y = min(intercept, key=lambda x: x[1])[1]  # Minimum y-value

    return max_x, min_x, max_y, min_y

def get_slope_and_y_intercept(k, h, reciprocal_lattice_vectors):
    #print("get_slope_and_y_intercept")
    g_x =  k * reciprocal_lattice_vectors[2] + h * reciprocal_lattice_vectors[0]
    g_y =  k * reciprocal_lattice_vectors[3] + h * reciprocal_lattice_vectors[1]
    #print(k, h, reciprocal_lattice_vectors, g_x, g_y)

    m = - g_x / g_y
    b = 0.5 * (g_y + g_x * g_x / g_y)
    #print(k, h, g_x, g_y, reciprocal_lattice_vectors, m, b)

    return m, b

def write_k_mesh(output_filename, num_kx, num_ky, max_x, min_x, max_y, min_y):
    # Sample lines to write to the file
    delta_x = 1.25 * (max_x - min_x) / num_kx
    delta_y = 1.25 * (max_y - min_y) / num_ky
    m =0
    try:
        # Open the file in write mode ('w')
        with open(output_filename, 'w') as file:
            # Write the sample lines to the file
            for i in range(0, num_kx):
                for j in range(0, num_ky):
                    file.write(f"{m} {1.25 * min_x + i * delta_x} {1.25 * min_y + j * delta_y} {0.00000} {1/ (num_kx * num_ky)}\n")
                    m = m + 1
        print(f"File '{output_filename}' created successfully.")
    except Exception as e:
        print(f"Error occurred while creating file '{output_filename}': {e}")



if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <input.fdf> <output_k mesh name> <number_of_kx_points> <number_of_ky_points>")
    else:
        filename = sys.argv[1]
        output_filename = sys.argv[2]
        num_kx = int(sys.argv[3])
        num_ky = int(sys.argv[4])
        
        print(filename, output_filename, num_kx, num_ky)
        #this only returns the x and y compontents of the lattice vectors which are required to construct the 2d brillioun zone
        real_lattice_vectors = get_real_lattice_vectors(filename)
        print("real_lattice_vectors:", real_lattice_vectors)

        reciprocal_lattice_vectors = get_reciprocal_lattice_vectors(real_lattice_vectors)
        print("reciprocal_lattice_vectors:", reciprocal_lattice_vectors)
        intercept = [[0 for _ in range(2)] for _ in range(28)]
        
        i = 0
        for k in range(-1, 2, 1):
            for h in range(-1, 2, 1):
                if (k !=0 or h != 0):
                    get_all_intercepts(k, h, reciprocal_lattice_vectors, intercept, i)
                    i = i + 1       

        index = get_indices(intercept)
        brillioun_zone_boundaries = [[0 for _ in range(2)] for _ in range(6)]

        with open('brillioun_zone.dat', 'w') as f:
            f.write("#kx     ky\n")  # Add newline character to separate header from data
            for i in range(len(index)):
                brillioun_zone_boundaries[i][0] = intercept[index[i]][0]
                brillioun_zone_boundaries[i][1] = intercept[index[i]][1]
                kx = brillioun_zone_boundaries[i][0]
                ky = brillioun_zone_boundaries[i][1]
                f.write(f"{kx} {ky}\n")  # Using f-string to format the values and add a newline

        max_x, min_x, max_y, min_y = find_max_min_points(brillioun_zone_boundaries)
        print("Maximum x-value:", max_x)
        print("Minimum x-value:", min_x)
        print("Maximum y-value:", max_y)
        print("Minimum y-value:", min_y)

        write_k_mesh(output_filename, num_kx, num_ky, max_x, min_x, max_y, min_y)

