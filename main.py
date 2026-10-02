from fastapi import FastAPI, HTTPException, status
from dataclasses import asdict
from schemas import TaskCreate, TaskUpdate, TaskResponse
from models import Task

app = FastAPI(title="Task Manager")

tasks_db: dict[int, Task] = {}

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def tasks_create_endpoint(task_in: TaskCreate):
    new_id = len(tasks_db) + 1
    task_data = task_in.model_dump()
    new_task = Task(task_id=new_id, **task_data)
    tasks_db[new_id] = new_task
    task_dict = asdict(new_task)
    return TaskResponse(**task_dict)

@app.get("/tasks", response_model=list[TaskResponse])
def get_task_endpoint():
    response_list = []
    for task in tasks_db.values():
        task_dict = asdict(task)
        response_list.append(TaskResponse(**task_dict))
    return response_list

#https://codesignal.com/learn/courses/http-methods-and-request-handling-with-fastapi/lessons/removing-items-with-delete-requests was used to understand the delete function in fastapi
@app.delete("/tasks/{task_id}")
def delete_task_endpoint(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist")
    del tasks_db[task_id]
    return {"message": f"Task {task_id} deleted successfully"}

#https://www.linkedin.com/pulse/understanding-patch-method-fastapi-manikandan-parasuraman-powzc/ was used to understand the patch method in fastapi
#PATCH is used to partially to update resources
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task_endpoint(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    task_dict = asdict(tasks_db[task_id])
    task_dict.update(update_data)
    updated_task = Task(**task_dict)
    tasks_db[task_id] = updated_task
    return TaskResponse(**asdict(updated_task))
