#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta
import shutil
import textwrap

import click
from tabulate import tabulate

from task import TASKS_FILE, Task, TaskState

term_width = shutil.get_terminal_size((80, 20)).columns
MAX_WIDTH = int(term_width * 0.25)


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        tasks = [Task.from_dict(item) for item in json.load(f)]
        tasks.sort(key=lambda t: datetime.fromisoformat(t.last_modified), reverse=True)
        for idx, task in enumerate(tasks):
            task.uid = idx

        save_tasks(tasks)

        return tasks


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("description", nargs=-1)
def add(description: str):
    add_task(0, description)


@cli.command()
@click.argument("description", nargs=-1)
def r(description: str):
    add_task(1, description)


def add_task(repeat: int, description: str):
    """Add a new task"""
    if not description:
        raise click.UsageError("Add a description.")

    task = Task(description=" ".join(description), repeat=(repeat == 1))
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    click.echo("Task added.")


@cli.command()
@click.argument("index", type=int)
def d(index):
    """Remove a task by index"""
    tasks = load_tasks()
    try:
        task = tasks.pop(index)
        save_tasks(tasks)
        click.echo(f"Task removed: {task.description}")
    except IndexError:
        click.echo("Index not valid")


@cli.command()
@click.argument("index", type=int)
@click.argument("state")
def u(index, state):
    """Update task state - States: pending | started | hold | pr | pre | done"""
    tasks = load_tasks()
    try:
        new_state = TaskState.from_str(state)
        task = next((t for t in tasks if t.uid == index), None)
        task.update_state(new_state)
        save_tasks(tasks)
        click.echo(f"State updated: [{new_state.value}] {task.description}")
    except IndexError:
        click.echo("Index not valid")
    except click.UsageError as e:
        click.echo(f"Error: {e}")


@cli.command()
def clean():
    """Remove done tasks older than today"""
    tasks = load_tasks()
    today = datetime.now().date()
    remaining_tasks = []
    removed_count = 0

    for task in tasks:
        mod_date = datetime.fromisoformat(task.last_modified).date()

        if task.state == TaskState.DONE and task.repeat and mod_date == today:
            task.update_state(TaskState.PENDING)

        if task.state == TaskState.DONE and mod_date < today:
            removed_count += 1
        else:
            remaining_tasks.append(task)

    save_tasks(remaining_tasks)
    click.echo(f"Tasks cleaned: {removed_count}")


@cli.command()
@click.argument("modo", required=False, default="")
def s(modo):
    """Tasks summary - Use 's all' to show also 'done'"""
    mostrar_todo = modo.lower() == "all"
    summary(mostrar_todo)


def summary(mostrar_todo: bool):
    tasks = load_tasks()

    click.echo("Tasks summary:\n")

    table = []

    for state in TaskState:
        if not mostrar_todo and state in [TaskState.DONE, TaskState.HOLD]:
            continue

        filtered = [t for t in tasks if t.state == state]
        if not filtered:
            continue

        for task in filtered:
            mod_dt = datetime.fromisoformat(task.last_modified)
            mod_str = mod_dt.strftime("%d/%m/%Y")

            tag = ""
            if mod_dt.date() == datetime.now().date():
                tag = "TODAY"
            elif mod_dt.date() == (datetime.now() - timedelta(days=1)).date():
                tag = "YESTERDAY"

            wrapped_desc = "\n".join(textwrap.wrap(task.description, width=MAX_WIDTH))
            state_text = state.value.upper()
            if task.repeat:
                state_text += "*"

            table.append(
                [
                    task.uid,
                    wrapped_desc,
                    state_text,
                    tag,
                    mod_str,
                ]
            )

    click.echo(
        tabulate(
            table,
            headers=["ID", "Description", "State", "Tag", "Last modified"],
            tablefmt="fancy_grid",
        )
    )


if __name__ == "__main__":
    cli()
