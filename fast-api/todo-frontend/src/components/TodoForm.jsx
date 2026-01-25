import { useState, useEffect } from "react";
import "./TodoForm.css";

function TodoForm({ onSubmit, initialData, onCancel }) {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    priority: 3,
    completed: false,
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title,
        description: initialData.description,
        priority: initialData.priority,
        completed: initialData.completed,
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const value =
      e.target.type === "checkbox"
        ? e.target.checked
        : e.target.type === "number"
          ? parseInt(e.target.value)
          : e.target.value;

    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    if (!initialData) {
      setFormData({
        title: "",
        description: "",
        priority: 3,
        completed: false,
      });
    }
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <h3>{initialData ? "Edit Todo" : "Add New Todo"}</h3>

      <div className="form-group">
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          maxLength={50}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          maxLength={250}
          rows={4}
          required
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="priority">Priority (1-5)</label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            required
          >
            <option value={1}>1 - Critical</option>
            <option value={2}>2 - High</option>
            <option value={3}>3 - Medium</option>
            <option value={4}>4 - Low</option>
            <option value={5}>5 - Very Low</option>
          </select>
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="completed"
              checked={formData.completed}
              onChange={handleChange}
            />
            <span>Mark as completed</span>
          </label>
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn-submit">
          {initialData ? "Update Todo" : "Add Todo"}
        </button>
        <button type="button" className="btn-cancel" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}

export default TodoForm;
