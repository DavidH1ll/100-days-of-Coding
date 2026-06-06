import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("=" * 60)
print("NUMPY COMPUTATION & N-DIMENSIONAL ARRAYS")
print("=" * 60)

# 1. Array Creation
print("\n--- Array Creation ---")
zeros = np.zeros((3, 4))
print(f"Zeros (3x4):\n{zeros}")

ones = np.ones((2, 5))
print(f"\nOnes (2x5):\n{ones}")

identity = np.eye(4)
print(f"\nIdentity (4x4):\n{identity}")

random_arr = np.random.rand(3, 3)
print(f"\nRandom (3x3):\n{random_arr.round(3)}")

range_arr = np.arange(0, 20, 2)
print(f"\nArange (0-20 step 2): {range_arr}")

linspace_arr = np.linspace(0, 1, 10)
print(f"Linspace (0-1, 10 points): {linspace_arr.round(2)}")

# 2. Reshaping
print("\n--- Reshaping ---")
arr_1d = np.arange(1, 13)
arr_2d = arr_1d.reshape(3, 4)
arr_3d = arr_1d.reshape(2, 2, 3)

print(f"1D ({arr_1d.shape}): {arr_1d}")
print(f"2D ({arr_2d.shape}):\n{arr_2d}")
print(f"3D ({arr_3d.shape}):\n{arr_3d}")

# 3. Broadcasting
print("\n--- Broadcasting ---")
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
row_vector = np.array([10, 20, 30])
result = matrix + row_vector
print(f"Matrix:\n{matrix}")
print(f"\nMatrix + [{row_vector}]:\n{result}")

# 4. Universal Functions
print("\n--- Universal Functions ---")
arr = np.array([1, 4, 9, 16, 25])
print(f"Array: {arr}")
print(f"sqrt: {np.sqrt(arr)}")
print(f"log: {np.log(arr).round(3)}")
print(f"exp: {np.exp(np.array([0, 1, 2])).round(3)}")
print(f"sin: {np.sin(np.array([0, np.pi/2, np.pi])).round(3)}")

# 5. Boolean Indexing
print("\n--- Boolean Indexing ---")
scores = np.random.randint(40, 100, 10)
print(f"Scores: {scores}")
print(f"Passing (>=60): {scores[scores >= 60]}")
print(f"Top scores (>85): {scores[scores > 85]}")

# 6. Linear Algebra
print("\n--- Linear Algebra ---")
A = np.array([[3, 1], [1, 2]])
B = np.array([9, 8])

print(f"Matrix A:\n{A}")
print(f"Determinant: {np.linalg.det(A):.1f}")
print(f"Inverse:\n{np.linalg.inv(A).round(2)}")

eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"Eigenvalues: {eigenvalues.round(2)}")

solution = np.linalg.solve(A, B)
print(f"Solution to Ax=B: x={solution.round(2)}")
print(f"Verify: A@x = {A @ solution.round(2)}")

# 7. Statistical Functions
print("\n--- Statistics ---")
data = np.random.normal(50, 15, 1000)
print(f"Mean: {data.mean():.2f}")
print(f"Median: {np.median(data):.2f}")
print(f"Std: {data.std():.2f}")
print(f"Min: {data.min():.2f}, Max: {data.max():.2f}")
print(f"90th percentile: {np.percentile(data, 90):.2f}")

# 8. Image as 3D Array
print("\n--- Image as 3D Array ---")
image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
print(f"Image shape: {image.shape}")
print(f"Red channel mean: {image[:,:,0].mean():.1f}")
print(f"Green channel mean: {image[:,:,1].mean():.1f}")
print(f"Blue channel mean: {image[:,:,2].mean():.1f}")

grayscale = (image[:,:,0] * 0.299 + image[:,:,1] * 0.587 + image[:,:,2] * 0.114).astype(np.uint8)
print(f"Grayscale shape: {grayscale.shape}")

# Visualization
fig, axes = plt.subplots(2, 3, figsize=(14, 10))
fig.suptitle("NumPy Array Visualizations", fontsize=14, fontweight="bold")

axes[0, 0].imshow(image)
axes[0, 0].set_title("Random RGB Image")

axes[0, 1].imshow(image[:,:,0], cmap="Reds")
axes[0, 1].set_title("Red Channel")

axes[0, 2].imshow(grayscale, cmap="gray")
axes[0, 2].set_title("Grayscale")

matrix_viz = np.random.rand(10, 10)
axes[1, 0].imshow(matrix_viz, cmap="viridis")
axes[1, 0].set_title("Heatmap")

axes[1, 1].hist(data, bins=30, color="steelblue", edgecolor="white")
axes[1, 1].set_title("Normal Distribution")

x = np.linspace(0, 4*np.pi, 100)
axes[1, 2].plot(x, np.sin(x), label="sin(x)", linewidth=2)
axes[1, 2].plot(x, np.cos(x), label="cos(x)", linewidth=2)
axes[1, 2].set_title("Trig Functions")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Day076/numpy_visualizations.png", dpi=150, bbox_inches="tight")
print("\nChart saved to Day076/numpy_visualizations.png")
plt.close()
