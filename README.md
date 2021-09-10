# FoxScript
A Python-based language compiled to MC Commands (Datapacks)

# Progress
- [ ] Loops
- [X] If statements
- [X] Namespaces
- [X] Functions
- [X] Tick
- [X] Load
- [X] Scoreboards

# How to use it
FoxScript syntax is pretty close to Python.

### Decorators
```python
#Minecraft Version
__project__["mc-version"]  = "1.16.5"
#Name
__project__["name"]        = "Fox"
#Description
__project__["description"] = "FoxScriptTest"
#Author
__project__["author"]      = "FabulousFox"
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

# List of all syntax:
```python
#say
say("text")

#scoreboard objectives add scoreboardname scoreboardtype, the type is by default dummy
scoreboard("scoreboardname","scoreboardtype")

#@a[name=Steve,x=0,dx=0,...], when only one argument is given, the player with that name will be targeted, the standard type is @a
Player(type="@a",name="Steve")

#scoreboard player set Steve DemoBoard 0
Player("Steve").DemoBoard = 0

#If-statements
if Player("Steve").DemoBoard == Player("Alex").DemoBoard:
    say("Identical")
if Player("Steve").DemoBoard == 2:
    say("2")
```
