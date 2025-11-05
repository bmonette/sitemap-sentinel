from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.db import get_db
from app.security import get_current_user
from app import models
from app.schemas import ProjectIn, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


def _ensure_owner(project: models.Project, user_id: int):
    if not project or project.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    project = models.Project(
        user_id=user.id,
        name=payload.name.strip(),
        site_url=str(payload.site_url),
        sitemap_url=str(payload.sitemap_url),
    )
    db.add(project)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Project already exists for this sitemap")
    db.refresh(project)
    return project


@router.get("", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Project).filter(models.Project.user_id == user.id).order_by(models.Project.created_at.desc()).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    project = db.get(models.Project, project_id)
    _ensure_owner(project, user.id)
    return project


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    project = db.get(models.Project, project_id)
    _ensure_owner(project, user.id)

    if payload.name is not None:
        project.name = payload.name.strip()
    if payload.site_url is not None:
        project.site_url = str(payload.site_url)
    if payload.sitemap_url is not None:
        project.sitemap_url = str(payload.sitemap_url)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Project already exists for this sitemap")
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    project = db.get(models.Project, project_id)
    _ensure_owner(project, user.id)
    db.delete(project)
    db.commit()
