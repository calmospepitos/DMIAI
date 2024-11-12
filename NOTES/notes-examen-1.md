### Python, Numpy, and KNN Notes for AI Exam

---

### Numpy Basics
- **Core Use**: Numpy is the main library for numerical and matrix computations in Python, essential for data manipulation in AI.
- **Array Creation**:
  - `np.array([1, 2, 3])` – Creates a 1D array.
  - `np.zeros((2, 2))`, `np.ones((2, 2))` – Creates 2x2 arrays of zeros or ones.
  - `np.arange(start, stop, step)` – Array with a range of values.
  - `np.linspace(start, stop, num)` – Array with `num` evenly spaced values.

---

### Array Manipulation

#### Adding Elements
- **`np.append`**: Adds values to the end of an array.
  ```python
  arr = np.array([1, 2, 3])
  new_arr = np.append(arr, [4, 5])  # [1, 2, 3, 4, 5]
  ```
- **`np.insert`**: Inserts values at a specified index.
  ```python
  arr = np.array([1, 2, 3])
  new_arr = np.insert(arr, 1, 10)  # [1, 10, 2, 3]
  ```

#### Removing Elements
- **`np.delete`**: Removes elements at specified indices.
  ```python
  arr = np.array([1, 2, 3, 4, 5])
  new_arr = np.delete(arr, 2)  # [1, 2, 4, 5]
  ```

#### Concatenation and Stacking
- **Concatenate**: Joins arrays along an axis.
  ```python
  new_arr = np.concatenate((arr1, arr2))  # [1, 2, 3, 4]
  ```
- **Stacking**:
  - **Vertical**: `np.vstack((arr1, arr2))` – [[1, 2], [3, 4]]
  - **Horizontal**: `np.hstack((arr1, arr2))` – [1, 2, 3, 4]

#### Splitting Arrays
- **`np.split`**: Divides an array into sub-arrays.
  ```python
  arr1, arr2, arr3 = np.split(arr, [2, 4])  # [1, 2], [3, 4], [5, 6]
  ```

#### Modifying Elements
- **Direct Assignment**:
  ```python
  arr[1] = 10  # [1, 10, 3]
  ```
- **Slices**: Update sections of an array.
  ```python
  arr[1:4] = [10, 20, 30]  # [1, 10, 20, 30, 5]
  ```

#### Reshaping and Transposing
- **`reshape`**: Changes the array’s dimensions.
  ```python
  new_arr = arr.reshape(2, 3)  # [[1, 2, 3], [4, 5, 6]]
  ```
- **`transpose`**: Flips the array's axes.
  ```python
  new_arr = np.transpose(arr)  # [[1, 4], [2, 5], [3, 6]]
  ```

#### Mathematical Operations
- **Element-wise**: Operations like `+`, `-`, `*`, `/` are element-wise.
  ```python
  new_arr = arr * 2  # [2, 4, 6]
  ```
- **Aggregation**: `np.sum(arr)`, `np.mean(arr)`, `np.max(arr)`, `np.min(arr)`.

---

### Array Attributes

### `ndarray` Attributes
- **Key Attributes of `ndarray`**:
  - `.dtype`: Data type of elements (e.g., `int32`, `float64`).
  - `.ndim`: Number of dimensions.
  - `.shape`: Shape of the array as a tuple (rows, columns, etc.).
  - `.size`: Total number of elements in the array.

---

### Data Normalization

- **What is Data Normalization**:
  - Data normalization is the process of scaling features so that they have comparable ranges.
  - Normalization often scales each feature to a standard range (e.g., 0 to 1) or to a distribution with a mean of 0 and a standard deviation of 1.
  - **Normalization Formula** (Standardization with z-score):  
    \[
    \text{normalized\_data} = \frac{\text{data} - \text{mean}}{\text{std\_dev}}
    \]
    ```python
    normalized_data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
    ```

- **When to Use Normalization**:
  - **Distance-Based Algorithms**: Normalization is crucial for algorithms like KNN, where distance metrics are used, as features on different scales can disproportionately affect the distance.
  - **Improving Model Performance**: Ensures all features contribute equally, which can enhance model accuracy.
  - **Data Ranges Differ Significantly**: If one feature’s range is much larger than others, it could dominate the distance metric (e.g., age vs. income).
  - **When Outliers Are Present**: Normalization can sometimes mitigate the impact of outliers.

---

### Distance Calculations for KNN
- **Euclidean Distance**: `np.sqrt(np.sum((point1 - point2)**2))`
- **Efficient Distance Calculation with Broadcasting**:
  ```python
  np.sqrt(np.sum((data_points - query_point)**2, axis=1))
  ```

#### Sorting for Nearest Neighbors
- `np.argsort(arr)` – Returns indices that would sort `arr`.
  ```python
  distances = np.sqrt(np.sum((data_points - query_point)**2, axis=1))
  nearest_neighbors = np.argsort(distances)[:K]
  ```

---

### K-Nearest Neighbors (KNN)

#### Concept
- **What it Does**: KNN is a simple, non-parametric algorithm for classification and regression.
- **Steps**:
  1. **Select K**: Choose the number of neighbors, `K`. Low K → sensitive to noise, High K → general.
  2. **Calculate Distances**:
    - **Euclidean Distance**:  
  $$d(p, q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$$
    - **Manhattan Distance**:  
  $$d(p, q) = \sum_{i=1}^{n} |p_i - q_i|$$
    - **Cosine Similarity**:  
  $$\text{cosine\_similarity}(p, q) = \frac{p \cdot q}{\|p\| \|q\|}$$
  3. **Sort and Select Neighbors**: Find K closest points.
  4. **Predict**:
     - **Classification**: Majority vote among K neighbors.
     - **Regression**: Average value of K neighbors.

#### Sorting for Nearest Neighbors
- `np.argsort(arr)` – Returns indices that would sort `arr`.
  ```python
  distances = np.sqrt(np.sum((data_points - query_point)**2, axis=1))
  nearest_neighbors = np.argsort(distances)[:K]
  ```

---

#### Parameters
- **Number of Neighbors (K)**:
  - Low K → high variance (overfitting).
  - High K → high bias (underfitting).
- **Distance Metric**: Determines "closeness."
  - Euclidean (good for continuous, equally scaled data).
  - Manhattan (grid-like or high-dimensional data).
  - Cosine Similarity (for high-dimensional/text data).
- **Feature Scaling**: Use normalization or standardization.

#### Example Workflow
1. **Standardize Features**:
   ```python
   normalized_data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
   ```
2. **Compute Euclidean Distance**:
   ```python
   distances = np.sqrt(np.sum((data_points - query_point)**2, axis=1))
   ```
3. **Sort Distances**:
   ```python
   nearest_neighbors = np.argsort(distances)[:K]
   ```
4. **Predict Class Label** (Classification):
   ```python
   labels, counts = np.unique(nearest_neighbor_labels, return_counts=True)
   most_common_label = labels[np.argmax(counts)]
   ```

---

### Qt Basics (Python with PyQt or PySide)

#### What is Qt
- **GUI Framework**: Qt is used for building GUI applications. It provides widgets (buttons, labels, etc.) and layouts (organizing widgets).
- **Widgets**: Basic building blocks, e.g., `QPushButton`, `QLabel`, `QLineEdit`.
- **Layouts**: Organize widgets in a window, e.g., `QVBoxLayout`, `QHBoxLayout`.
- **Signals and Slots**: Event handling in Qt. E.g., clicking a button can trigger a function.

#### Basic Code Structure
```python
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication([])
window = QWidget()
window.setWindowTitle('My Application')
window.show()
app.exec_()
```

#### QMainWindow
- Provides more complex window structures, with menu bars, toolbars, and status bars.