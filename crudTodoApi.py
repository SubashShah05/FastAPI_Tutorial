from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos=[]

class Todo(BaseModel):
    id: int
    title: str  
    completed: bool

    @app.post("/create-todo")
    def create_todo(todo: Todo):
        todos.append(todo)
        return {
            "message": "Todo created successfully",
            "data": todo
        } 
    
    @app.get("/get-todos")
    def get_todos():
        return {
            "message": "Todos retrieved successfully",
            "data": todos
        }
    
    @app.get("/get-todo/{todo_id}")
    def get_todo(todo_id: int):
        for todo in todos:
            if todo.id == todo_id:
                return {
                    "message": "Todo retrieved successfully",
                    "data": todo
                }
        return {
            "error": "Todo not found"
        }  


    @app.put("/update-todo/{todo_id}")
    def update_todo(todo_id: int, updated_todo: Todo):
        for index, todo in enumerate(todos):
            if todo.id == todo_id:
                todos[index] = updated_todo
                return {
                    "message": "Todo updated successfully",
                    "data": updated_todo
                }
        return {
            "error": "Todo not found"
        }   
    
    @app.delete("/delete-todo/{todo_id}")
    def delete_todo(todo_id: int):
        for index, todo in enumerate(todos):
            if todo.id == todo_id:
                deleted_todo = todos.pop(index)
                return {
                    "message": "Todo deleted successfully",
                    "data": deleted_todo
                }
        return {
            "error": "Todo not found"
        }