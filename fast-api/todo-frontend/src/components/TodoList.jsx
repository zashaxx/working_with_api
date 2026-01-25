import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { todoAPI } from "../services/api";
import TodoItem from "./TodoItem";
import TodoForm from "./TodoForm";
import "./TodoList.css";

function TodoList() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingTodo, setEditingTodo] = useState(null);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data = await todoAPI.getAllTodos();
      setTodos(data);
      setError("");
    } catch (err) {
      setError("Failed to fetch todos");
      if (err.response?.status === 401) {
        logout();
        navigate("/login");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (todoData) => {
    try {
      await todoAPI.createTodo(todoData);
      fetchTodos();
      setShowForm(false);
    } catch (err) {
      setError("Failed to create todo");
    }
  };

  const handleUpdateTodo = async (id, todoData) => {
    try {
      await todoAPI.updateTodo(id, todoData);
      fetchTodos();
      setEditingTodo(null);
    } catch (err) {
      setError("Failed to update todo");
    }
  };

  const handleDeleteTodo = async (id) => {
    if (window.confirm("Are you sure you want to delete this todo?")) {
      try {
        await todoAPI.deleteTodo(id);
        fetchTodos();
      } catch (err) {
        setError("Failed to delete todo");
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading todos...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <nav className="navbar">
        <h1>📝 My Todos</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}!</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      {error && <div className="error-message">{error}</div>}

      <div className="todo-container">
        <div className="todo-header">
          <h2>Your Tasks</h2>
          <button
            className="btn-add"
            onClick={() => {
              setShowForm(!showForm);
              setEditingTodo(null);
            }}
          >
            {showForm ? "Cancel" : "+ Add New Todo"}
          </button>
        </div>

        {(showForm || editingTodo) && (
          <TodoForm
            onSubmit={
              editingTodo
                ? (data) => handleUpdateTodo(editingTodo.id, data)
                : handleAddTodo
            }
            initialData={editingTodo}
            onCancel={() => {
              setShowForm(false);
              setEditingTodo(null);
            }}
          />
        )}

        <div className="todos-list">
          {todos.length === 0 ? (
            <div className="no-todos">
              <p>No todos yet! Click "Add New Todo" to create one.</p>
            </div>
          ) : (
            todos.map((todo) => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onEdit={() => {
                  setEditingTodo(todo);
                  setShowForm(false);
                }}
                onDelete={handleDeleteTodo}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default TodoList;
