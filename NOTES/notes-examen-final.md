## Numpy Fundamentals

### Traversing Arrays
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
  - **Start**: Index to start slicing (inclusive).
  - **Stop**: Index to stop slicing (exclusive).
  - **Step**: Step size (default is 1).
  ```python
  # arr[start:stop:step]
  
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
- **Using** `np.nditer` **for General Iteration**:
  This function provides a unified way to iterate through arrays of any dimension.
  ```python
  arr = np.array([[1, 2], [3, 4]])
  for element in np.nditer(arr):
      print(element) # 1, 2, 3, 4
  ```
- **Iterating With Conditions**:
  Combine iteration with boolean conditions.
  ```python
  arr = np.array([1, 2, 3, 4, 5])
  for val in arr:
      if val > 3:
          print(val)  # Prints values greater than 3
  ''' Slicing: Extract parts of an array using indices in Python. In Python, slicing follows the rule of inclusive start and exclusive stop.'''
  arr = np.array([1, 2, 3, 4, 5])
  sliced = arr[1:4]  # [2, 3, 4]
  ```
- **Boolean Indexing**: Filter arrays based on conditions.
  ```python
  arr = np.array([1, 2, 3, 4, 5])
  filtered = arr[arr > 3]  # [4, 5]
  ''' Not comparing indexes, but the value of the items inside the array. Here we're checking if each item is greater than 3.'''
  ```

### Array Manipulation

- **Array Creation**:
  - `np.array([1, 2, 3])` – Creates a 1D array.
  - `np.zeros((2, 2))`, `np.ones((2, 2))` – Creates 2x2 arrays of zeros or ones.
  - `np.arange(start, stop, step)` – Array with a range of values.
  - `np.linspace(start, stop, num)` – Array with `num` evenly spaced values.
- **Reshaping**: Change the shape of an array without altering data.
  ```python
  arr = np.arange(1, 10)
  # arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  reshaped = arr.reshape(3, 3)
  # reshaped = [[1, 2, 3],
  #             [4, 5, 6],
  #             [7, 8, 9]]
  ```
- **Transposing**: Flips the array's axes.
  ```python
  arr = np.array([[1, 2, 3], [4, 5, 6]])
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
- **GUI Framework**: Qt is used for building GUI (Graphical User Interface) applications. It provides widgets (buttons, labels, etc.) and layouts (organizing widgets).
- **Widgets**: Basic building blocks, e.g., `QPushButton`, `QLabel`, `QLineEdit`.
- **Layouts**: Organize widgets in a window, e.g., `QVBoxLayout`, `QHBoxLayout`.
- **Signals and Slots**: Event handling in Qt. E.g., clicking a button can trigger a function.

### Signals and Slots
- Qt uses a **signal and slot** mechanism for event handling.
- **Signal**: Emitted when an event occurs (e.g., button click).
- **Slot**: A function that is executed in response to a signal.

```python
button = QPushButton("Click Me")
button.clicked.connect(lambda: print("Button clicked!"))
```

### Layouts
- Used to arrange widgets in the window.
- Types of layouts:
  - `QHBoxLayout`: Horizontal layout.
  - `QVBoxLayout`: Vertical layout.
  - `QGridLayout`: Grid layout.

- Key methods for QGridLayout:
  - `setSpacing(spacing)`: Space between cells.
  - `setRowStretch(row, factor)`: Adjust row resizing behavior.

```python
layout = QGridLayout()
layout.addWidget(QLabel("Label 1"), 0, 0)
layout.addWidget(QPushButton("Button"), 1, 1)
window.setLayout(layout)
```

### Widgets
#### **Labels (`QLabel`)**
- Displays static or dynamic text/images.

```python
Qlabel = QLabel("Hello, World!")
label.setAlignment(Qt.AlignCenter)
label.setText("Updated Text")
```

#### **Buttons (`QPushButton`)**
- Used for user interaction.

```python
button = QPushButton("Click Me")
button.clicked.connect(lambda: print("Button clicked!"))
```

#### **Text Boxes**
- **Single-Line Input (`QLineEdit`)**:
  ```python
  line_edit = QLineEdit()
  line_edit.setPlaceholderText("Enter your name")
  ```

- **Multi-Line Input (`QTextEdit`)**:
  ```python
  text_edit = QTextEdit()
  text_edit.setText("This is a multi-line text box.")
  ```

#### **Combo Boxes (`QComboBox`)**
- Dropdown menu for selecting items.

```python
combo_box = QComboBox()
combo_box.addItem("Option 1")
combo_box.addItem("Option 2")
combo_box.setCurrentIndex(0)  # Set default selection
```

#### **Checkboxes (`QCheckBox`)**
- Allows selection of multiple options.

```python
check_box = QCheckBox("I agree to the terms")
```

#### **Radio Buttons (`QRadioButton`)**
- Allows selection of one option from a group.

```python
radio1 = QRadioButton("Option 1")
radio2 = QRadioButton("Option 2")
```

### QMainWindow
Use a central widget with layouts to add your widgets.

```python
app = QApplication([])

# Main Window
window = QMainWindow()
central_widget = QWidget()
layout = QVBoxLayout()

# Add widgets
label = QLabel("Welcome!")
button = QPushButton("Start")
layout.addWidget(label)
layout.addWidget(button)

# Set the central widget and layout
central_widget.setLayout(layout)
window.setCentralWidget(central_widget)

window.show()
app.exec_()
```

## Genetic Algorithms (GA)

- **Definition**: A Genetic Algorithm is a search heuristic that mimics the process of natural selection, drawing inspiration from biological evolution. It is a type of evolutionary algorithm that generates solutions to optimization and search problems. The idea is to evolve a population of candidate solutions (individuals) over several generations to find the best solution(s).

### The Applications
- **Optimization**: Scheduling, resource allocation, and layout design.
- **Machine Learning**: Feature selection and hyperparameter tuning.
- **AI**: Strategy development in games.

### Biological Background

- **Natural Selection**: Individuals with favorable traits are more likely to survive and reproduce, passing their traits to the next generation. In GAs, individuals with higher fitness scores are selected for reproduction.
- **Genes, Crossover, and Mutation**:  
   - **Chromosomes** represent potential solutions, composed of genes.
   - **Crossover** combines genes from two parents to create offspring.
   - **Mutation** introduces random changes to maintain diversity and explore new solution spaces.

### Components of a Genetic Algorithm
1. **Population**: A set of candidate solutions (chromosomes) for the problem.
   - **Example**: Chromosomes represent truck delivery routes.
   - *High*: Finds diverse solutions and avoids getting stuck in bad spots (local optima), but slower and needs more computation.
   - *Low*: Runs faster, but less variety and more likely to get stuck in bad solutions.
2. **Fitness Function**: Evaluates how well a solution meets the     objective. Higher fitness indicates better solutions.
   - **Fitness Function**: $$\text{Fitness Score} = \frac{1}{Total Distance}$$
   - *High (low-distance)*: Good solution.
   - *Low (high-distance)*: Bad solution.
3. **Selection Function**: Chooses individuals for reproduction based on fitness.
   - *High*: Keeps picking the same strong solutions, leading to less variety.
   - *Low*: Wastes time on bad solutions.
4. **Crossover Function**: Combines information from parents to produce offspring.
   - *High*: Mixes good traits, helping find better solutions, but can ruin good solutions by over-mixing.
   - *Low*: Keeps good solutions intact, but slow to find new, better solutions.
5. **Mutation Function**: Introduces randomness by altering genes, ensuring diversity and avoiding local optima.
   - *High*: Keeps the algorithm from getting stuck by trying new things, but can make the algorithm too random, slowing progress.
   - *Low*: Focuses on refining good solutions, but risks getting stuck with no improvements.

### Selection Methods
- **Roulette Wheel Selection**: Individuals are selected based on their fitness proportions, like spinning a roulette wheel where fitter individuals occupy larger segments.
- **Tournament Selection**: Randomly choose a subset of individuals and select the fittest among them.
- **Rank-Based Selection**: Individuals are ranked based on fitness, and selection probability is assigned according to rank rather than absolute fitness.

### Crossover Techniques
- **Single-point Crossover**: Choose one point in the parent chromosomes and swap the segments after that point.
- **Multi-point Crossover**: Select multiple points for segment swapping.
- **Uniform Crossover**: For each gene, randomly choose which parent to inherit from.

### Termination Conditions
GAs typically terminate when one of these conditions is met:
- A satisfactory solution is found.
- A maximum number of generations is reached.
- The population converges (diversity is lost).
- Computational budget (time or resources) is exhausted.

### The Process
1. **Initialization**: Generate an initial random population.
2. **Evaluation**: Calculate fitness scores for the population.
3. **Selection**: Choose individuals for reproduction.
4. **Crossover**: Combine parent genes to create new individuals.
5. **Mutation**: Introduce random changes in offspring.
6. **Replacement**: Form a new population with offspring.
7. **Repeat**: Iterate until reaching the termination condition.

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