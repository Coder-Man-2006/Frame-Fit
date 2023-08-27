import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the CSV data
data = pd.read_csv("measurements.csv")

# Separate features (X) and target (y)
X = data[["Length of Face", "Temple to Temple", "Cheekbone to Cheekbone", "Jawline"]]
y_face_length = data["Length of Face"]
y_temple_to_temple = data["Temple to Temple"]
y_cheekbone_to_cheekbone = data["Cheekbone to Cheekbone"]
y_jawline = data["Jawline"]

# Create a linear regression model
model = LinearRegression()

# Fit the model for each measurement
model.fit(X, y_face_length)
slope_face_length = model.coef_[0]
intercept_face_length = model.intercept_

model.fit(X, y_temple_to_temple)
slope_temple_to_temple = model.coef_[0]
intercept_temple_to_temple = model.intercept_

model.fit(X, y_cheekbone_to_cheekbone)
slope_cheekbone_to_cheekbone = model.coef_[0]
intercept_cheekbone_to_cheekbone = model.intercept_

model.fit(X, y_jawline)
slope_jawline = model.coef_[0]
intercept_jawline = model.intercept_

# Print equations
print(f"Equation Face Length: y = {slope_face_length:.2f}x + {intercept_face_length:.2f}")
print(f"Equation Temple to Temple: y = {slope_temple_to_temple:.2f}x + {intercept_temple_to_temple:.2f}")
print(f"Equation Cheekbone to Cheekbone: y = {slope_cheekbone_to_cheekbone:.2f}x + {intercept_cheekbone_to_cheekbone:.2f}")
print(f"Equation Jawline: y = {slope_jawline:.2f}x + {intercept_jawline:.2f}")

# Scatter plots
plt.figure(figsize=(10, 6))
plt.scatter(X.iloc[:, 0], y_face_length, color=(245/255, 245/255, 220/255), label="Face Length")
plt.scatter(X.iloc[:, 1], y_temple_to_temple, color=(255/255, 0, 0), label="Temple to Temple")
plt.scatter(X.iloc[:, 2], y_cheekbone_to_cheekbone, color=(176/255, 224/255, 230/255), label="Cheekbone to Cheekbone")
plt.scatter(X.iloc[:, 3], y_jawline, color=(128/255, 0, 128/255), label="Jawline")

plt.xlabel("Measurement")
plt.ylabel("Value")
plt.title("Linear Regression Scatter Plots")
plt.legend()
plt.grid(True)
plt.show()

