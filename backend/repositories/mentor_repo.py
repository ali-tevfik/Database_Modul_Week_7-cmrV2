from sqlalchemy import text
from db.db import engine


# İsme göre mentor arama
def find_mentor_by_name(name: str): 
    print("mentor_repo find_mentor_by_name called with name:", name)
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT                                 
                    trainees.full_name as trainee_full_name,
                    mentors.*
                FROM mentors
                INNER JOIN trainees
                    ON mentors.trainee_id = trainees.trainee_id
                WHERE LOWER(mentors.full_name) LIKE :name
            """),
            {"name": f"%{name.lower()}%"}  # parametre burada düzgün geçiyor
        )
        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        return data


       
   # Tüm mentorları getirme     
def get_all_mentors():
    print("mentors_repo get_all_mentors called")  
    with engine.connect() as conn:
        result = conn.execute(text("""
           SELECT 
      trainees.full_name as trainee_full_name,
	    mentors.*
FROM mentors
INNER JOIN trainees
    ON mentors.trainee_id = trainees.trainee_id;
        """))
        print("Query executed, fetching results..."),

        # ✅ Row'ları sözlük (dict) haline getiriyoruz
        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        return data



def find_mentor_by_comboBox(opinion_value: str):
    """Seçilen comboBox değerine göre mentorları getirir"""
    with engine.connect() as conn:
        stmt = text("""
            SELECT trainees.full_name as trainee_full_name,
                   mentors.*
            FROM mentors
            INNER JOIN trainees
                ON mentors.trainee_id = trainees.trainee_id
            WHERE mentors.opinion = :opinion
        """)
        result = conn.execute(stmt, {"opinion": opinion_value})
        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        return data