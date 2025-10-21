from sqlalchemy import text
from db import engine


def get_all_users_raw():
    print("interviews_repo get_all_users_raw called ")  
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                t.full_name,
                pt.project_submission_date,
                pt.project_progress_date
            FROM project_tracking pt
            INNER JOIN trainees t ON pt.trainee_id = t.trainee_id
        """))
        print("Query executed, fetching results...")

        # ✅ Row'ları sözlük (dict) haline getiriyoruz
        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        print("Data fetched successfully:", data)
        return data
