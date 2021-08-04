# Word Sudoku Solver

Word Sudoku Solver using genetic algorithms

### Setup
1. Install python 3
2. Install [pip](https://pypi.org/project/pip/)

OR alternatively, you can use [PyCharm Community](https://www.jetbrains.com/pycharm/download/), which comes prepacked with Python and will auto-setup with the project
   
### Run
cd "project-folder"

1. `pip install -r requirements.txt`
2. `python3 main_demo.py`

### Directory Structure
Assuming root directory => (cd "project-folder")

Main program file => `main_demo.py`

1. `ga_component` - Module for Genetic Algorithm operators and solver resides here
2. `model` - All data types and sample word sudoku problems resides here
3. `util` - Common utility classes for matrices, populating random data, etc.
   
----
4. tests - !! Not relevant to GA implementation !! To individually test smaller parts - like GA operators
5. extras - !! Not relevant to GA implementation !! Module for grid visualisation (for generating report) and to generate statistics by multiple trials

### Notes
All Python code - syntax, naming, conventions follow [PEP8](https://www.python.org/dev/peps/pep-0008/) guidelines

