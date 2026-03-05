"""
Exercise 3: Files and JSON
==========================
Practice: reading/writing files, JSON serialization

Instructions:
- Complete each function where you see TODO
- Run this file to test your solutions
- All tests should print "PASSED"

Run with: python exercise_3_files_json.py
"""

import json
import os


# =============================================================================
# EXERCISE 3.1: Writing to a File
# =============================================================================
"""
Create a function that writes a list of lines to a text file.

Parameters:
    filepath (str): Path to the file to create
    lines (list): List of strings to write (one per line)

The function should:
- Create/overwrite the file
- Write each line followed by a newline character
- Use UTF-8 encoding

Example:
    write_lines("output.txt", ["Hello", "World"])
    # Creates file with:
    # Hello
    # World
"""

def write_lines(filepath: str, lines: list) -> None:
    with open(filepath, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line+ "\n")


# =============================================================================
# EXERCISE 3.2: Reading from a File
# =============================================================================
"""
Create a function that reads a text file and returns its lines.

Parameters:
    filepath (str): Path to the file to read

Returns:
    list: List of lines (with whitespace/newlines stripped)

Example:
    # If file contains:
    # Hello
    # World
    read_lines("output.txt") -> ["Hello", "World"]
"""

def read_lines(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


# =============================================================================
# EXERCISE 3.3: Appending to a File
# =============================================================================
"""
Create a function that appends a single line to an existing file.

Parameters:
    filepath (str): Path to the file
    line (str): Line to append

The function should add the line at the end of the file with a newline.
If the file doesn't exist, it should be created.

Example:
    append_line("log.txt", "Entry 1")
    append_line("log.txt", "Entry 2")
    # File now contains:
    # Entry 1
    # Entry 2
"""

def append_line(filepath: str, line: str) -> None:
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(line + "\n")


# =============================================================================
# EXERCISE 3.4: Count Words in a File
# =============================================================================
"""
Create a function that counts words in a text file.

Parameters:
    filepath (str): Path to the file

Returns:
    int: Total number of words in the file

A word is any sequence of characters separated by whitespace.

Example:
    # If file contains "Hello World\nThis is Python"
    count_words("file.txt") -> 5
"""

def count_words(filepath: str) -> int:
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
        return len(words)



# =============================================================================
# EXERCISE 3.5: Write Dictionary to JSON File
# =============================================================================
"""
Create a function that saves a dictionary to a JSON file.

Parameters:
    filepath (str): Path to the JSON file
    data (dict): Dictionary to save

The function should write formatted JSON (indented with 2 spaces).

Example:
    save_json("data.json", {"name": "Alice", "age": 30})
    # Creates file with:
    # {
    #   "name": "Alice",
    #   "age": 30
    # }
"""

def save_json(filepath: str, data: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


# =============================================================================
# EXERCISE 3.6: Load Dictionary from JSON File
# =============================================================================
"""
Create a function that loads a dictionary from a JSON file.

Parameters:
    filepath (str): Path to the JSON file

Returns:
    dict: The loaded dictionary

Example:
    data = load_json("data.json")
    data["name"] -> "Alice"
"""

def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


# =============================================================================
# EXERCISE 3.7: Update JSON File
# =============================================================================
"""
Create a function that updates specific keys in a JSON file.

Parameters:
    filepath (str): Path to the JSON file
    **updates: Key-value pairs to update

The function should:
1. Load the existing JSON data
2. Update it with the provided key-value pairs
3. Save it back to the file

Example:
    # If file contains {"name": "Alice", "age": 30}
    update_json("data.json", age=31, city="NYC")
    # File now contains {"name": "Alice", "age": 31, "city": "NYC"}
"""

def update_json(filepath: str, **updates) -> None:
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
        data.update(updates)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data,file, indent=2)


# =============================================================================
# EXERCISE 3.8: Todo List Manager
# =============================================================================
"""
Create a TodoList class that persists to a JSON file.

The class should:
- Load existing todos from file on initialization (or start empty if file doesn't exist)
- Save to file after every modification

Attributes:
    filepath (str): Path to the JSON file
    todos (list): List of todo dictionaries

Each todo is a dict: {"id": int, "task": str, "done": bool}

Methods:
    add(task: str) -> int: Add a new todo, return its id
    complete(todo_id: int) -> bool: Mark todo as done, return True if found
    get_pending() -> list: Return list of todos where done=False
    get_all() -> list: Return all todos

Example:
    todo_list = TodoList("todos.json")
    id1 = todo_list.add("Buy groceries")  # Returns 1
    id2 = todo_list.add("Walk the dog")   # Returns 2
    todo_list.complete(1)                  # Returns True
    todo_list.get_pending()                # Returns [{"id": 2, "task": "Walk the dog", "done": False}]
"""

class TodoList:
    def __init__(self, filepath: str):
        self.filepath = filepath
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                self.todos = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.todos = []

    def _save(self) -> None:
        """Helper method to save todos to file."""
        # Save self.todos to self.filepath as JSON
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.todos, file, indent=2)

    def _next_id(self) -> int:
        """Helper method to get the next available ID."""
        if not self.todos:
            return 1
        return max(todo["id"] for todo in self.todos)+1

    def add(self, task: str) -> int:

        todo_id = self._next_id()
        new_todo = {
            "id": todo_id,
            "task": task,
            "done": False
        }
        self.todos.append(new_todo)
        self._save()
        return todo_id

    def complete(self, todo_id: int) -> bool:
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["done"] = True
                self._save()
                return True
            return False

    def get_pending(self) -> list:
        return [todo for todo in self.todos if not todo["done"]]

    def get_all(self) -> list:
        #  Return all todos
        return self.todos


