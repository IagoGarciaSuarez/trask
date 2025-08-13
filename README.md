# tasky
Unix CLI tool to manage quick tasks

# How to use

Install requirements (don't use venv)

> pip install -r requirements.txt

Give execution permission

> sudo chmod +x ./main.py

Add a symbolic link to use it from any location

> sudo ln -s <route_to_tasky_root>/main.py /usr/local/bin/trask

Check commands:

> trask
```
add    Adds a new task.
clean  Remove done tasks older than today.
d      Remove a task by index.
r      Creates a repeatable task.
s      Tasks summary - Use 's all' to show all of them.
u      Update task state
```