const API_URL = import.meta.env.VITE_API_URL;

export async function obtenerTareas() {
  const res = await fetch(`${API_URL}/api/v1/tareas`);

  if (!res.ok) {
    throw new Error("Error al obtener tareas");
  }

  return res.json();
}

export async function crearTarea(data) {
  const res = await fetch(`${API_URL}/api/v1/tareas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Error al crear tarea");
  }

  return res.json();
}