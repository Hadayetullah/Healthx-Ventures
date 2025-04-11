from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import schemas, crud
from app.routes.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.create_task(db, task, user.id)

@router.get("/", response_model=list[schemas.Task])
def list_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_tasks(db, user.id)

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_task_by_id(db, task_id, user.id)

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = crud.update_task(db, task_id, task, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return updated

@router.patch("/{task_id}", response_model=schemas.Task)
def patch_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    patched = crud.patch_task(db, task_id, task, user.id)
    if not patched:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return patched

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    deleted = crud.delete_task(db, task_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return {"message": "Task deleted successfully"}
