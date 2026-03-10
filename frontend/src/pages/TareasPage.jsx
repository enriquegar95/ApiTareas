import { useEffect, useState } from "react";
import { obtenerTareas } from "../api/tareasApi";

export default function TareasPage() {
  const [tareas, setTareas] = useState([]);

  useEffect(() => {
    cargarTareas();
  }, []);

  async function cargarTareas() {
    try {
      const data = await obtenerTareas();
      setTareas(data);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Lista de tareas</h1>

      <ul>
        {tareas.map((t) => (
          <li key={t.id}>
            {t.titulo}
          </li>
        ))}
      </ul>
    </div>
  );
}