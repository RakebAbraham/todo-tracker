from flask import Flask, render_template, request, redirect, url_for
from database import SessionLocal, Todo, Tag
from sqlalchemy import asc, desc
import datetime
import random

app = Flask(__name__)

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

@app.route("/")
def index():
    db = SessionLocal()
    
    # Query parameters
    show_completed = request.args.get('show_completed', 'incomplete')  # Default to showing incomplete
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    tag_filter = request.args.get('tag')
    
    # Base query
    query = db.query(Todo)
    
    # Filter based on completion status
    if show_completed == 'complete':
        query = query.filter(Todo.is_completed == True)
    elif show_completed == 'incomplete':
        query = query.filter(Todo.is_completed == False)
    # If show_completed == 'all', don't apply any completion filter
    
    if tag_filter:
        query = query.join(Todo.tags).filter(Tag.name == tag_filter)
    
    # Sorting
    if sort_by == 'due_date':
        sort_column = Todo.due_date
    else:
        sort_column = Todo.created_at
    
    if order == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    todos = query.all()
    
    # Get all tags for filtering
    all_tags = db.query(Tag).all()
    
    # Add this line to get a random quote
    quote = random.choice(QUOTES)
    
    return render_template(
        'index.html',
        todos=todos,
        all_tags=all_tags,
        current_tag=tag_filter,
        show_completed=show_completed,
        sort_by=sort_by,
        order=order,
        quote=quote
    )

@app.route("/add", methods=["GET", "POST"])
def add_todo():
    if request.method == "POST":
        db = SessionLocal()
        title = request.form.get('title')
        body = request.form.get('body')
        due_date_str = request.form.get('due_date')
        tag_values = request.form.getlist('tags')  # Gets multiple checkbox values
        
        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
        tags = []
        for tag_name in tag_values:
            tag = db.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            tags.append(tag)
        
        new_todo = Todo(
            title=title,
            body=body,
            due_date=due_date,
            tags=tags
        )
        db.add(new_todo)
        db.commit()
        db.close()
        return redirect(url_for('index'))
    
    return render_template('add_todo.html')

@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).filter_by(id=todo_id).first()
    if todo:
        todo.is_completed = not todo.is_completed
        db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).filter_by(id=todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    db.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
