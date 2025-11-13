from PIL import Image
"""
Write your code below.  You may (and should) create
as many helper functions as you want.
However, the program must have main() and running it should make 
the program work as expected.
"""
filename = "colorado.dat"
grid = []

file = open(filename, 'r')
for line in file:
    row = []
    numbers = line.split()
    for num in numbers:
        row.append(int(num))
    grid.append(row)
file.close()

print("Rows:", len(grid))
print("Cols:", len(grid[0]))

def find_min(grid):
    min_elev = grid[0][0]
    for row in grid:
        for value in row:
            if value < min_elev:
                min_elev = value
    return min_elev

def find_max(grid):
    max_elev = grid[0][0]
    for row in grid:
        for value in row:
            if value > max_elev:
                max_elev = value
    return max_elev


def elevation_to_gray(elevation, min_elev, max_elev):
    gray = (elevation - min_elev) / (max_elev - min_elev) * 255
    gray = int(gray)
    return gray

def create_image(grid, min_elev, max_elev):
    rows = len(grid)
    cols = len(grid[0])

    img = Image.new('RGB', (cols, rows))

    for row in range(rows):
        for col in range(cols):
            elevation = grid[row][col]
            gray = elevation_to_gray(elevation, min_elev, max_elev)
            img.putpixel((col, row), (gray, gray, gray))

    img.save("elevation_map.png")
    print("Image saved as elevation_map.png")
    return img

def find_best_path(grid, start_row):
    """
    Finds a finds from west to east that tries to stay flat.
    """
    rows = len(grid)
    cols = len(grid[0])
    path = []
    current_row = start_row

    for col in range(cols):
        path.append((current_row, col))

        if col < cols - 1:
            current_elevation = grid[current_row][col]
            
            # Look at 3 possible next moves
            # Option 1: Forward (same row)
            forward_row = current_row
            
            # Forward-up (row - 1)
            forward_up_row = current_row - 1
            
            # Forward-down (row + 1)
            forward_down_row = current_row + 1
            
            # Calculate elevation change for each option
            # Start with forward
            best_row = forward_row
            forward_elev = grid[forward_row][col + 1]
            best_change = abs(forward_elev - current_elevation)
            
            if forward_up_row >= 0:
                up_level = grid[forward_up_row][col + 1]
                up_change = abs(up_level - current_elevation)
                if up_change < best_change:
                    best_change = up_change
                    best_row = forward_up_row

            current_row = best_row
    
    return path

def calculate_cost(grid, path):
    """
    Calculates the total elevation change along a path.
    Lower cost = flatter path (better!)
    """
    total_change = 0
    
    for i in range(len(path) - 1):
        current_row, current_col = path[i]
        next_row, next_col = path[i + 1]
        
        current_elev = grid[current_row][current_col]
        next_elev = grid[next_row][next_col]
        
        change = abs(next_elev - current_elev)
        total_change = total_change + change
    
    return total_change


def draw_path_on_image(grid, path, min_elev, max_elev):
    """
    Creates image with the path drawn in red
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Create the grayscale image first
    img = Image.new('RGB', (cols, rows))
    
    for row in range(rows):
        for col in range(cols):
            elevation = grid[row][col]
            gray = elevation_to_gray(elevation, min_elev, max_elev)
            img.putpixel((col, row), (gray, gray, gray))
    
    # Draw the path in red
    for row, col in path:
        img.putpixel((col, row), (255, 0, 0))  # Red!
    
    img.save("best_path_map.png")
    print("Path image saved as best_path_map.png")
    return img


def save_path_data(grid, path):

    file = open("best_path.dat", 'w')

    for row, col in path:
        elevation = grid[row][col]
        file.write(str(row) + " " + str(col) + " " + str(elevation) + "\n")

    file.close()
    print("Path data saved as best_path.dat")

def save_metric(cost):
    "Saves cost metric"
    file = open("best_path_metric.txt", 'w')
    file.write("Metric name: Total Elevation Change\n")
    file.write("Best Path Metric: " + str(cost) + "\n")
    file.close()
    print("Metric saved as best_path_metric.txt")

def main():
    min_elev = find_min(grid)
    max_elev = find_max(grid)
    create_image(grid, min_elev, max_elev)

    print("\n=== PART 2: Finding Best Path ===")
    start_row = len(grid) // 2  # Start in the middle
    print("Starting from row:", start_row)
    
    print("Finding path...")
    path = find_best_path(grid, start_row)
    
    print("Calculating cost...")
    cost = calculate_cost(grid, path)
    print("Total elevation change:", cost)
    
    print("Drawing path on map...")
    draw_path_on_image(grid, path, min_elev, max_elev)
    
    print("Saving path data...")
    save_path_data(grid, path)
    
    print("Saving metric...")
    save_metric(cost)
    
    print("\n=== ALL DONE! ===")
    print("Check your folder for:")
    print("  - elevation_map.png")
    print("  - best_path_map.png")
    print("  - best_path.dat")
    print("  - best_path_metric.txt")


        
    




if __name__ == "__main__":
    main()