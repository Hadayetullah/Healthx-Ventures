from sqlalchemy.orm import Session
from app import models, schemas

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# def get_tasks(db: Session):
#     return db.query(models.Task).all()

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_data: schemas.TaskCreate, user_id: int):
    task = get_task(db, task_id)
    if task and task.owner_id == user_id:
        task.title = task_data.title
        task.description = task_data.description
        db.commit()
        db.refresh(task)
        return task
    return None

def patch_task(db: Session, task_id: int, task_data: schemas.TaskCreate, user_id: int):
    task = get_task(db, task_id)
    if task and task.owner_id == user_id:
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        db.commit()
        db.refresh(task)
        return task
    return None

def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id)
    if task and task.owner_id == user_id:
        db.delete(task)
        db.commit()
        return task
    return None