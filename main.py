#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta

import click
from tabulate import tabulate

from task import TASKS_FILE, Task, TaskState


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
    """Add a new task"""
    if not description:
        raise click.UsageError("Add a description.")

    task = Task(description=" ".join(description))
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    click.echo("Task added.")


@cli.command()
def list():
    """Show all tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks")
        return

    for i, task in enumerate(tasks):
        click.echo(
            f"{i}. [{task.state.value}] {task.description} (Last mod.: {task.last_modified})"
        )


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
    """Update task state"""
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
    """Remove done tasks older than yesterday"""
    tasks = load_tasks()
    yesterday = datetime.now().date() - timedelta(days=1)

    remaining_tasks = []
    removed_count = 0

    for task in tasks:
        mod_date = datetime.fromisoformat(task.last_modified).date()
        if task.state == TaskState.DONE and mod_date < yesterday:
            removed_count += 1
        else:
            remaining_tasks.append(task)

    save_tasks(remaining_tasks)
    click.echo(f"Tasks cleaned: {removed_count}")


@cli.command()
def s():
    """Tasks summary"""
    summary()


def summary():
    tasks = load_tasks()

    click.echo("Tasks summary:\n")

    table = []
    for state in TaskState:
        filtered = [t for t in tasks if t.state == state]
        if not filtered:
            continue

        for task in filtered:
            mod_dt = datetime.fromisoformat(task.last_modified)
            mod_str = mod_dt.strftime("%d-%m-%Y")

            tag = ""
            if mod_dt.date() == datetime.now().date():
                tag = "TODAY"
            elif mod_dt.date() == (datetime.now() - timedelta(days=1)).date():
                tag = "YESTERDAY"

            table.append(
                [task.uid, task.description, tag, state.value.upper(), mod_str]
            )

    click.echo(f"---- {state.value.upper()} ----")
    click.echo(
        tabulate(
            table,
            headers=[
                "ID",
                "Description",
                "Tag",
                "State",
                "Last modified",
            ],
            tablefmt="fancy_grid",
        )
    )


if __name__ == "__main__":
    cli()
