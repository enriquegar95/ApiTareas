from app.db.database import Base

# importa modelos aquí para que Alembic los registre
from app.models.tarea import Tarea  # noqa: F401
from app.models.prioridad import Prioridad  # noqa: F401
from app.models.estado import Estado  # noqa: F401