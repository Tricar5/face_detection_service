""""""
import json
from redis import Redis

__all__ = [
    "get_all_tasks"
]


def get_all_tasks(r: Redis, st, end) -> list[str]:
    """Function to get all tasks"""

    tasks = []
    # iterate a list in batches of size n

    for i, key in enumerate(r.scan_iter()):

        if i in range(st, end + 1):
            k = key.decode("utf-8")
            task_body = json.loads(r.get(k).decode("utf-8"))
            tasks.append({"id": k.replace("celery-task-meta-", ""),
                          "status": task_body.get("status"),
                          "result": task_body.get("result").get("result")})

    return tasks
