import "./TodoList.css";

function TodoItem({ todo, onEdit, onDelete }) {
  const priorityLabels = {
    1: "Critical",
    2: "High",
    3: "Medium",
    4: "Low",
    5: "Very Low",
  };

  return (
    <div className={`todo-item ${todo.completed ? "completed" : ""}`}>
      <div className="todo-header-row">
        <h3 className="todo-title">{todo.title}</h3>
        <div className="todo-actions">
          <button className="btn-edit" onClick={() => onEdit(todo)}>
            Edit
          </button>
          <button className="btn-delete" onClick={() => onDelete(todo.id)}>
            Delete
          </button>
        </div>
      </div>

      <p className="todo-description">{todo.description}</p>

      <div className="todo-meta">
        <span className={`priority-badge priority-${todo.priority}`}>
          Priority: {priorityLabels[todo.priority]}
        </span>
        <span
          className={`status-badge ${todo.completed ? "completed" : "pending"}`}
        >
          {todo.completed ? "✓ Completed" : "○ Pending"}
        </span>
      </div>
    </div>
  );
}

export default TodoItem;
