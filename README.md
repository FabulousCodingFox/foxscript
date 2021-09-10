# FoxScript
A Python-based language compiled to MC Commands (Datapacks)

# How to use it
FoxScript syntax is pretty close to Python.

### Decorators
```python
#Set the author name
@author: FabulousFox
#Set the MC Version
@mc-version: 1.16.5
#Set the project name(Name of the folder in the datapacks folder)
@project-name: FoxScript_Test
#Set the project description
@project-description: This is a test!
```

### Making a Function
First, we need to create the namespace:
```python
class Namespace:
```
To add a function, simply add a python-like codeline:
```python
class Namespace:
    def function():
        say("Hi!")
```
To make a function executed every tick or reload, name them "__tick__" and "__load__".
```python
class Namespace:
    def __tick__():
        say("Executed 20 times a second")
    def __load__():
        say("Executed on reload")
```
