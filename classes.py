import logging
from dataclasses import dataclass

import utils

# Base period of time in μs
timeBase = 1

printTime = lambda value: utils.printTime(value, timeBase)


class Task:
    def __init__(self, name, wcet, period, deadline, offset=0, priority=0):
        self.name = name
        self.wcet = wcet
        self.period = period
        self.deadline = deadline
        self.offset = offset
        self.priority = priority
        logging.debug(f"Task created: {self}")

    def __repr__(self) -> str:
        "Return a string representation of the task for debugging"
        return f"Task({self.name}, period={self.period}, wcet={self.wcet}, deadline={self.deadline}, offset={self.offset}, priority={self.priority})"

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.wcet,
                self.period,
                self.deadline,
                self.offset,
                self.priority,
            )
        )


class Job:
    def __init__(self, parent_task: Task, id: int):
        self.task = parent_task
        self.id = id
        self.release = ((self.id - 1) * self.task.period) + self.task.offset
        self.deadline = self.release + self.task.deadline

        self.read_interval = [self.release, self.deadline - self.task.wcet]
        self.data_intervval = [
            self.release + self.task.wcet,
            self.deadline + self.task.period,
        ]

        # JLD attributes
        self.JLD_successors = []
        self.JLD_predecessors = []
        logging.debug(f"Job created: {self}")

    def __str__(self) -> str:
        """String representation of the job"""
        str_job = f"Job({self.task.name}, {self.id}): r = {printTime(self.release)}, d = {printTime(self.deadline)}"

        return str_job

    def __repr__(self) -> str:
        return f"Job({self.task.name}, {self.id})"

    def __hash__(self) -> int:
        return hash((self.task, self.id))


@dataclass(frozen=True)
class JLD:
    """Class to represent a job-level dependency"""

    pred_task: Task
    pred_job_id: int
    succ_task: Task
    succ_job_id: int

    def __str__(self):
        return f"JLD: {self.pred_task.name}#{self.pred_job_id} -> {self.succ_task.name}#{self.succ_job_id}"


class TreeNode:
    def __init__(self, job: Job):
        self.job = job
        self.children = []
        self.parent = None

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def __str__(self, level=0):
        prefix = "   " * level + "|--- " if level > 0 else ""
        ret = f"{prefix}{repr(self.job)}\n"

        for child in self.children:
            ret += child.__str__(level + 1)

        return ret

    def __repr__(self):
        return f"TreeNode({self.job})"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Example Tasks
    task1 = Task("Task1", wcet=5, period=20, deadline=15, offset=0, priority=1)
    task2 = Task("Task2", wcet=3, period=10, deadline=10, offset=0, priority=2)
    task3 = Task("Task3", wcet=4, period=25, deadline=20, offset=5, priority=3)
    task4 = Task("Task4", wcet=2, period=15, deadline=12, offset=2, priority=4)

    # Jobs for each task
    job1 = Job(task1, id=1)
    job2 = Job(task1, id=2)
    job3 = Job(task2, id=1)
    job4 = Job(task2, id=2)
    job5 = Job(task3, id=1)
    job6 = Job(task3, id=2)
    job7 = Job(task4, id=1)
    job8 = Job(task4, id=2)

    # Root of the tree
    root = TreeNode(job1)

    # First level children
    child1 = TreeNode(job2)
    child2 = TreeNode(job3)
    child3 = TreeNode(job5)

    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)

    # Second level (children of child1)
    subchild1 = TreeNode(job4)
    subchild2 = TreeNode(job6)
    child1.add_child(subchild1)
    child1.add_child(subchild2)

    # Third level (children of child2)
    subchild3 = TreeNode(job7)
    child2.add_child(subchild3)

    # Fourth level (deep nested dependency)
    subsubchild = TreeNode(job8)
    subchild3.add_child(subsubchild)

    # Print the entire tree
    print(root)
