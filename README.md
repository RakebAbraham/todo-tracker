# Todo Tracker

A minimalist todo tracking application with a sophisticated nude color palette, designed to help manage tasks efficiently while maintaining a clean and calming aesthetic. This project was developed in collaboration with Anthropic's Claude AI, showcasing the potential of human-AI pair programming.

## Features

- 🎯 Simple and intuitive task management
- 🏷️ Four essential tag categories:
  - Urgent
  - Work
  - Personal
  - Other
- ⚡ Quick filtering and sorting options
- 💭 Inspiring quotes for daily motivation
- 🎨 Minimalist design with a soothing color scheme inspired by Claude's aesthetic
- 🤖 AI-assisted development using Claude 3 Sonnet

## Tech Stack

- Backend: Python/FastAPI
- Database: SQLAlchemy with SQLite
- Frontend: HTML/CSS
- Design: Custom minimalist UI developed with Claude's guidance
- Development Partner: Anthropic's Claude AI

## Project Structure

todo_tracker/
├── database.py      # Database models and configuration
├── main.py         # FastAPI application and routes
└── templates/      # HTML templates
    ├── index.html
    └── add_todo.html

## Development Journey

### Timeline & Challenges (Total: ~5 hours)

1. **Initial Approach (1 hour)**
   - Started with a single .py file approach
   - Discovered limitations with task addition functionality
   - Researched project structure options

2. **Framework Switch (1.5 hours)**
   - Initially built with Flask (incorrect framework choice)
   - Had to refactor to FastAPI to meet requirements
   - Learned about async/await patterns
   - Dealt with static file serving issues

3. **Database & Structure (1.5 hours)**
   - Implemented SQLAlchemy models
   - Created proper project structure
   - Fixed persistent database issues
   - Handled tag relationships

4. **UI/UX Development (1 hour)**
   - Implemented minimalist design
   - Added inspiring quotes feature
  
### What Worked Well
- Claude was crucial throughout - helped me figure out bugs and design choices when I was stuck
- SQLAlchemy turned out perfect for the database - I tried other approaches but this one just clicked
- Kept the UI super minimal - didn't want to overcomplicate it and it worked out great
- The tag system (urgent/work/personal/other) made organizing tasks actually make sense
- FastAPI's async handling - once I got it working, it handled everything smoothly

### What Was a Struggle at First
- Tried cramming everything into one .py file - bad idea, had to split it up when nothing was working
- Built it in Flask first because I kept encountering errors with installing FastHtml - had to redo everything in FastAPI
- The static files were a mess - I didn't realize I needed a proper structure for them
- Made the database way more complex than needed - simplified it and everything worked better
- Spent too much time fighting with imports before organizing the project structure properly

### What I Figured Out Along the Way
- FastAPI and Flask are completely different - had to relearn how routes work
- Should've planned the structure first - would've saved hours of redoing everything
- Each framework handles static files differently - learned this the hard way
- Keep database relationships simple - no need to overcomplicate things
- Clean design actually made the app work better - not just look better

## Getting Started
