import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # registers the 3d projection
from matplotlib.animation import FuncAnimation

# --------------------------
# 1. Define the tesseract (4-D hypercube)
# --------------------------

# Generate the 16 vertices: each coordinate is either -1 or +1.
vertices = []
for i in range(16):
    # For each bit position j, choose 1 if the jth bit of i is 1, otherwise -1.
    v = np.array([1 if (i >> j) & 1 else -1 for j in range(4)])
    vertices.append(v)
vertices = np.array(vertices)  # shape (16, 4)

# Determine the edges: two vertices are connected if they differ in exactly one coordinate.
edges = []
for i, v in enumerate(vertices):
    for d in range(4):
        neighbor = np.copy(v)
        neighbor[d] *= -1  # flip the sign in coordinate d
        # Find the index of the neighbor vertex.
        j = np.where(np.all(vertices == neighbor, axis=1))[0][0]
        # To avoid drawing the same edge twice, only add if i < j.
        if i < j:
            edges.append((i, j))

# --------------------------
# 2. Set up the ball simulation in 4D
# --------------------------

# Start the ball near the center with a small random velocity.
ball_pos = np.random.uniform(-0.5, 0.5, 4)
ball_vel = np.random.uniform(-0.05, 0.05, 4)

# Time step for the simulation:
dt = 0.05

# --------------------------
# 3. Define projection and rotation functions
# --------------------------

def project_point(point4d, d=3.0):
    """
    Project a 4D point (x, y, z, w) into 3D using a simple perspective projection.
    The parameter d is the distance from the 4D viewer to the projection hyperplane.
    """
    factor = d / (d - point4d[3])
    return point4d[:3] * factor

def rotation_matrix_4d(a, b):
    """
    Build a 4x4 rotation matrix that applies two independent rotations:
      - In the xw-plane by angle 'a'
      - In the yz-plane by angle 'b'
    These rotations act on separate pairs of coordinates so they commute.
    """
    R_xw = np.array([
        [ np.cos(a), 0, 0, -np.sin(a)],
        [ 0,         1, 0,  0         ],
        [ 0,         0, 1,  0         ],
        [ np.sin(a), 0, 0,  np.cos(a)]
    ])
    R_yz = np.array([
        [1, 0,          0,           0],
        [0, np.cos(b), -np.sin(b),   0],
        [0, np.sin(b),  np.cos(b),   0],
        [0, 0,          0,           1]
    ])
    return R_yz @ R_xw

# --------------------------
# 4. Set up the matplotlib figure and animation
# --------------------------

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Ball bouncing inside a tesseract")

# Set fixed axis limits. (Depending on the projection these may need adjusting.)
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-3, 3])
# For newer versions of matplotlib you can try to force equal aspect ratio:
try:
    ax.set_box_aspect([1,1,1])
except Exception:
    pass  # if not available, ignore

def update(frame):
    global ball_pos, ball_vel

    # --- Update the ball simulation ---
    ball_pos += ball_vel * dt

    # Bounce off any face of the hypercube (i.e. if coordinate exceeds �1, reverse velocity).
    for i in range(4):
        if ball_pos[i] > 1:
            ball_pos[i] = 1
            ball_vel[i] *= -1
        elif ball_pos[i] < -1:
            ball_pos[i] = -1
            ball_vel[i] *= -1

    # --- Determine the 4D rotation for visualization ---
    # Let the rotation angles vary with time (frame number).
    a = frame * 0.03  # rotation in the xw-plane
    b = frame * 0.02  # rotation in the yz-plane
    R = rotation_matrix_4d(a, b)

    # --- Project and draw the tesseract edges ---
    projected_vertices = []
    for v in vertices:
        # Rotate the vertex in 4D:
        v_rot = R @ v
        # Project the rotated vertex from 4D to 3D:
        proj = project_point(v_rot)
        projected_vertices.append(proj)
    projected_vertices = np.array(projected_vertices)  # shape (16, 3)

    # Clear the axes to redraw
    ax.cla()
    ax.set_title("Ball bouncing inside a tesseract")
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])
    try:
        ax.set_box_aspect([1,1,1])
    except Exception:
        pass

    # Draw each edge of the tesseract as a thin black line.
    for i, j in edges:
        p1 = projected_vertices[i]
        p2 = projected_vertices[j]
        ax.plot([p1[0], p2[0]],
                [p1[1], p2[1]],
                [p1[2], p2[2]], color='black', lw=0.5)

    # --- Project and draw the ball ---
    ball_rot = R @ ball_pos
    ball_proj = project_point(ball_rot)
    ax.scatter(ball_proj[0], ball_proj[1], ball_proj[2], color='red', s=50)

    # (Optional) Turn off grid lines or set a background color:
    ax.grid(False)

# Create the animation. Adjust the number of frames and interval as desired.
ani = FuncAnimation(fig, update, frames=range(0, 1000), interval=50)

plt.show()
