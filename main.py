from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database import SessionLocal, Todo, Tag
from sqlalchemy import asc, desc
import datetime
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add this list of quotes
QUOTES = [
    "Small progress is still progress",
    "One task at a time",
    "Today's efforts shape tomorrow's success",
    "Start where you are",
    "Simple steps lead to great achievements",
    "Focus on progress, not perfection",
    "Each task completed is a step forward",
    "Mindful productivity brings peace",
    "Your future self will thank you",
    "Clarity comes from taking action"
]

@app.get("/")
async def index(request: Request, show_completed: str = 'incomplete', sort_by: str = 'created_at', 
                order: str = 'desc', tag: str = None):
    db = SessionLocal()
    
    query = db.query(Todo)
    
    if show_completed == 'complete':
        query = query.filter(Todo.is_completed == True)
    elif show_completed == 'incomplete':
        query = query.filter(Todo.is_completed == False)
    
    if tag:
        query = query.join(Todo.tags).filter(Tag.name == tag)
    
    if sort_by == 'due_date':
        sort_column = Todo.due_date
    else:
        sort_column = Todo.created_at
    
    if order == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    todos = query.all()
    all_tags = db.query(Tag).all()
    
    quote = random.choice(QUOTES)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "todos": todos,
            "all_tags": all_tags,
            "current_tag": tag,
            "show_completed": show_completed,
            "sort_by": sort_by,
            "order": order,
            "quote": quote
        }
    )

@app.get("/add")
async def add_todo_form(request: Request):
    return templates.TemplateResponse("add_todo.html", {"request": request})

@app.post("/add")
async def add_todo(
    title: str = Form(...),
    body: str = Form(None),
    due_date: str = Form(None),
    tags: list = Form([])
):
    db = SessionLocal()
    
    due_date_obj = datetime.datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
    tag_objects = []
    
    for tag_name in tags:
        tag = db.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        tag_objects.append(tag)
    
    new_todo = Todo(
        title=title,
        body=body,
        due_date=due_date_obj,
        tags=tag_objects
    )
    
    db.add(new_todo)
    db.commit()
    db.close()
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle/{todo_id}")
async def toggle_todo(todo_id: int):
    db = SessionLocal()
    todo = db.query(Todo).filter_by(id=todo_id).first()
    if todo:
        todo.is_completed = not todo.is_completed
        db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    db = SessionLocal()
    todo = db.query(Todo).filter_by(id=todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
