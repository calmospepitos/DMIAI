## Numpy Basics

### Traversing Arrays - Fundamentals
- **Iterating Through 1D Arrays**:
  Use a `for` loop to access each element in a 1D array.
  ```python
  arr = np.array([1, 2, 3, 4, 5])
  for element in arr:
      print(element)
  ```
- **Iterating Through 2D Arrays**:
  By default, iterating over a 2D array accesses rows.
  ```python
  arr = np.array([[1, 2], [3, 4], [5, 6]])
  for row in arr:
      print(row)
  ```
- **Accessing Columns in a 2D Array**:
  Use slicing or transposition to iterate through columns.
  ```python
  arr = np.array([[1, 2], [3, 4], [5, 6]])
  for col in arr.T:
      print(col)
  ```
- **Iterating Over Specific Rows or Columns**:
  Use slicing to access specific rows or columns.
  ```python
  arr = np.array([[1, 2], [3, 4], [5, 6]])
  # Access first row
  print(arr[0, :])  # [1, 2]
  # Access second column
  print(arr[:, 1])  # [2, 4, 6]
  ```
- **Iterating With Index**:
  Use `enumerate` for both index and value.
  ```python
  arr = np.array([10, 20, 30])
  for idx, val in enumerate(arr):
      print(f'Index {idx}: Value {val}')
  ```
- **Using `np.nditer` for General Iteration**:
  This function provides a unified way to iterate through arrays of any dimension.
  ```python
  arr = np.array([[1, 2], [3, 4]])
  for element in np.nditer(arr):
      print(element)
  ```
- **Iterating With Conditions**:
  Combine iteration with boolean conditions.
  ```python
  arr = np.array([1, 2, 3, 4, 5])
  for val in arr:
      if val > 3:
          print(val)  # Prints values greater than 3
  ''' Slicing: Extract parts of an array using indices in Python. '''
  arr = np.array([1, 2, 3, 4, 5])
  sliced = arr[1:4]  # [2, 3, 4]
  ```
- **Boolean Indexing**: Filter arrays based on conditions.
  ```python
  arr = np.array([1, 2, 3, 4, 5])
  filtered = arr[arr > 3]  # [4, 5]
  ```


## Array Manipulation

- **Array Creation**:
  - `np.array([1, 2, 3])` – Creates a 1D array.
  - `np.zeros((2, 2))`, `np.ones((2, 2))` – Creates 2x2 arrays of zeros or ones.
  - `np.arange(start, stop, step)` – Array with a range of values.
  - `np.linspace(start, stop, num)` – Array with `num` evenly spaced values.
- **Reshaping**: Change the shape of an array without altering data.
  ```python
  arr = np.arange(1, 10)
  reshaped = arr.reshape(3, 3)
  ```
- **`transpose`**: Flips the array's axes.
  ```python
  new_arr = np.transpose(arr)  # [[1, 4], [2, 5], [3, 6]]
  ```
- **Concatenate**: Joins arrays along an axis.
  ```python
  new_arr = np.concatenate((arr1, arr2))  # [1, 2, 3, 4]
  ```
- **Stacking**: Combine multiple arrays into one.
  ```python
  arr1 = np.array([1, 2])
  arr2 = np.array([3, 4])
  stacked = np.vstack((arr1, arr2))  # Vertical stacking
  ```
  - **Vertical**: `np.vstack((arr1, arr2))` – [[1, 2], [3, 4]]
  - **Horizontal**: `np.hstack((arr1, arr2))` – [1, 2, 3, 4]
- **Splitting**: Divide arrays into multiple sub-arrays.
  ```python
  arr = np.arange(1, 10)
  split = np.array_split(arr, 3)
  ```

### Adding Elements
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

### Removing Elements
- **`np.delete`**: Removes elements at specified indices.
  ```python
  arr = np.array([1, 2, 3, 4, 5])
  new_arr = np.delete(arr, 2)  # [1, 2, 4, 5]
  ```

### Modifying Elements
- **Direct Assignment**:
  ```python
  arr[1] = 10  # [1, 10, 3]
  ```
- **Slices**: Update sections of an array.
  ```python
  arr[1:4] = [10, 20, 30]  # [1, 10, 20, 30, 5]
  ```

### Mathematical Operations
- **Broadcasting**: Perform operations on arrays of different shapes.
  ```python
  arr = np.array([1, 2, 3])
  broadcasted = arr + 10  # [11, 12, 13]
  ```
- **Mathematical Operations**: Perform operations across arrays.
  ```python
  arr = np.array([1, 2, 3])
  summed = arr + arr  # [2, 4, 6]
  ```
- **Element-wise**: Operations like `+`, `-`, `*`, `/` are element-wise.
- **Aggregation**: `np.sum(arr)`, `np.mean(arr)`, `np.max(arr)`, `np.min(arr)`.

## Array Attributes

### `ndarray` Attributes
- **Key Attributes of `ndarray`**:
  - `.dtype`: Data type of elements (e.g., `int32`, `float64`).
  - `.ndim`: Number of dimensions.
  - `.shape`: Shape of the array as a tuple (rows, columns, etc.).
  - `.size`: Total number of elements in the array.


## Data Normalization

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


## Qt Basics (Python with PyQt or PySide)

### What is Qt
- **GUI Framework**: Qt is used for building GUI applications. It provides widgets (buttons, labels, etc.) and layouts (organizing widgets).
- **Widgets**: Basic building blocks, e.g., `QPushButton`, `QLabel`, `QLineEdit`.
- **Layouts**: Organize widgets in a window, e.g., `QVBoxLayout`, `QHBoxLayout`.
- **Signals and Slots**: Event handling in Qt. E.g., clicking a button can trigger a function.

### Basic Code Structure
```python
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication([])
window = QWidget()
window.setWindowTitle('My Application')
window.show()
app.exec_()
```

### QMainWindow
- Provides more complex window structures, with menu bars, toolbars, and status bars.

## Genetic Algorithms (GA)

- **Definition**: Genetic Algorithms are optimization techniques inspired by the natural selection process in biology. They simulate evolution to find optimal or near-optimal solutions for complex problems.

### Biological Background

- **Natural Selection**: Individuals with favorable traits are more likely to survive and reproduce, passing their traits to the next generation. In GAs, individuals with higher fitness scores are selected for reproduction.
- **Genes, Crossover, and Mutation**:  
   - **Chromosomes** represent potential solutions, composed of 'genes.'
   - **Crossover** combines genes from two parents to create offspring.
   - **Mutation** introduces random changes to maintain diversity and explore new solution spaces.

### Components of a Genetic Algorithm
1. **Population**: A set of candidate solutions (chromosomes) for the problem.
   - Example: Chromosomes represent truck delivery routes.
2. **Fitness Function**: Evaluates how well a solution meets the     objective. Higher fitness indicates better solutions.
3. **Selection Function**: Chooses individuals for reproduction based on fitness.
4. **Crossover Function**: Combines information from parents to produce offspring.
5. **Mutation Function**: Introduces randomness by altering genes, ensuring diversity and avoiding local optima.

### Selection Methods
- **Roulette Wheel Selection**: Individuals are selected based on their fitness proportions, like spinning a roulette wheel where fitter individuals occupy larger segments.
- **Tournament Selection**: Randomly choose a subset of individuals and select the fittest among them.
- **Rank-Based Selection**: Individuals are ranked based on fitness, and selection probability is assigned according to rank rather than absolute fitness.

### Crossover Techniques
- **Single-point Crossover**: Choose one point in the parent chromosomes and swap the segments after that point.
- **Multi-point Crossover**: Select multiple points for segment swapping.
- **Uniform Crossover**: For each gene, randomly choose which parent to inherit from.

### The Process
1. **Initialization**: Generate an initial random population.
2. **Evaluation**: Calculate fitness scores for the population.
3. **Selection**: Choose individuals for reproduction.
4. **Crossover**: Combine parent genes to create new individuals.
5. **Mutation**: Introduce random changes in offspring.
6. **Replacement**: Form a new population with offspring.
7. **Repeat**: Iterate until reaching the termination condition.

### Termination Conditions
GAs typically terminate when one of these conditions is met:
- A satisfactory solution is found.
- A maximum number of generations is reached.
- The population converges (diversity is lost).
- Computational budget (time or resources) is exhausted.

### The Applications
- **Optimization**: Scheduling, resource allocation, and layout design.
- **Machine Learning**: Feature selection and hyperparameter tuning.
- **AI**: Strategy development in games.

### The Challenges and Tips
- **Parameter Tuning**:  
   - Population size, mutation rate, and crossover rate significantly affect performance.
   - Larger populations offer better solutions but require more resources.
- **Encoding**: Transform problem-specific solutions into a chromosome format, e.g., routes as sequences.
- **Premature Convergence**:  
   - Occurs when the population lacks diversity.
   - Solutions: Increase mutation rate or start with a diverse initial population.
- **Elitism**:  
   - Retains the best solutions for the next generation.
   - Must balance elitism with diversity to prevent premature convergence.

### Example of a Simple GA
  ```python
  import numpy as np

  def tsp_fitness(route, distances):
      return -sum(distances[route[i], route[i+1]] for i in range(len(route)-1))

  def order_crossover(parent1, parent2):
      size = len(parent1)
      start, end = sorted(np.random.randint(0, size, 2))
      child = [-1] * size
      child[start:end] = parent1[start:end]
      remaining = [item for item in parent2 if item not in child]
      child[:start] = remaining[:start]
      child[end:] = remaining[start:]
      return child

  def swap_mutation(route, mutation_rate=0.1):
      for i in range(len(route)):
          if np.random.rand() < mutation_rate:
              j = np.random.randint(0, len(route))
              route[i], route[j] = route[j], route[i]
      return route
  ```
