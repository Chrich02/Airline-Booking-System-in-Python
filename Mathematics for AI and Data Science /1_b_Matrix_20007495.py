
import numpy as np

#Define the matrix (8 digits of student number + 1). 

matrix = np.array([
    [2, 0, 0],
    [0, 7, 4],
    [9, 5, 1]
])

#1. Calculate the determinant of the matrix ]. 
determinant = np.linalg.det(matrix)
print(f"Determinant: {determinant}\n")

#2. Determine whether the matrix is singular.
if np.isclose(determinant, 0): # using np.isclose for numerical stability. 
    print("The matrix is singular.\n")
else:
    print("The matrix is not singular.\n")

#3. Determine singularity. 
if not np.isclose(determinant, 0):
    inverse_matrix = np.linalg.inv(matrix)
    print(f"Inverse matrix: \n {inverse_matrix}\n")
else:
    inverse_matrix = "The matrix is singular and cannot be inverted."

#4. Multiply the original matrix by its transpose, print the result.
transposed_matrix = matrix.T
product_matrix = np.dot(matrix, transposed_matrix)
print(f"Product of the matrix and its transpose: \n {product_matrix}\n")

#5. Calculate the sum of the diagonal elements of the matrix obtained in step 4.
sum_diagonal = np.trace(product_matrix)
print(f"Sum of diagonal elements: {sum_diagonal}\n")





