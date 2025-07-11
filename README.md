# Proyecto con SQLAlchemy + Alembic + PostgreSQL

Este proyecto usa **SQLAlchemy** como ORM y **Alembic** para las migraciones, conectando a una base de datos **PostgreSQL**.

---

## 🔧 Configuración rápida

1. **Copia y edita la configuración**

```bash
cp sample.env .env
````

Edita `.env` y cambia `DATABASE_URI` con tu conexión PostgreSQL:

```
DATABASE_URI=postgresql://usuario:password@localhost:5432/mi_base
```

---

2. **(Opcional recomendado)** Crea entorno virtual

```bash
python -m venv env
source env/bin/activate  # en Windows: .\env\Scripts\activate
```

---

3. **Instala dependencias**

```bash
pip install -r requirements.txt
```

---

4. **Crea y aplica migraciones**

```bash
alembic revision --autogenerate -m "primer modelo"
alembic upgrade head
```

---

5. **Hostear de forma local**

```bash
fastapi dev main.py
```
---
---
## 🎖️ Integrantes
1. Matias Rocha
2. Cristofer Leiva
3. Tomas Serrudo
4. Miguel Rocha
---
