
from sqlalchemy import text
from db.db import engine
from sqlalchemy import text



def get_all_users_raw():
    print("applications_repo get_all_users_raw called ")

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                t.*,     
                a.*      
            FROM trainees t
            LEFT JOIN applications a ON t.trainee_id = a.trainee_id
            ORDER BY t.full_name;
        """))
        print("Query executed, fetching results...")

        rows = result.mappings().all()  # ✅ Sonuçları mapping formatında aldık
        data = [dict(row) for row in rows]  # ✅ Dict'e çevirdik
        print("Data fetched successfully:", data)

        return data



def searchText(search_text):
    with engine.connect() as conn:
        query = text("""
            SELECT 
                t.full_name,
                a.application_period,
                a.*
            FROM applications a
            INNER JOIN trainees t ON a.trainee_id = t.trainee_id
            WHERE t.full_name ILIKE :search_pattern
        """)
        
        # Parametreyi güvenli şekilde gönderiyoruz
        result = conn.execute(query, {"search_pattern": f"%{search_text}%"})
        print("Query executed, fetching results...")

        rows = result.mappings().all()  # Mapping formatında sonuç
        data = [dict(row) for row in rows]  # Dict'e çeviriyoruz
        print("Data fetched successfully:", data)

        return data
    
from sqlalchemy import text

def getAll():
    with engine.connect() as conn:
        query = text("""
            SELECT 
                t.*,     -- trainees tablosundaki tüm sütunlar önce gelir
                a.*      -- ardından applications tablosundaki tüm sütunlar
            FROM trainees t
            LEFT JOIN applications a ON t.trainee_id = a.trainee_id
            ORDER BY t.full_name;
        """)

        # Sorguyu çalıştırıyoruz
        result = conn.execute(query)
        print("Query executed, fetching results...")

        # Sonuçları dict formatına dönüştürüyoruz
        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        print(f"Data fetched successfully: {len(data)} rows")

        return data



def showmentor():
    with engine.connect() as conn:
        query = text("""
            SELECT 
                t.full_name,
                t.email,
                t.phone_number,
                a.mentor_interview,
                a.*
            FROM applications a
            INNER JOIN trainees t 
                ON a.trainee_id = t.trainee_id
            WHERE a.mentor_interview = true
        """)

        result = conn.execute(query)
        rows = result.mappings().all()

        data = [dict(row) for row in rows]

        if not data:
            print("No mentor interview results found")
            return []

        print("Data fetched successfully:", data)
        return data
        
def ushowmentor():
    with engine.connect() as conn:
        query = text("""
            SELECT 
                t.full_name,
                t.email,
                t.phone_number,
                a.mentor_interview,
                a.*
            FROM applications a
            INNER JOIN trainees t 
                ON a.trainee_id = t.trainee_id
            WHERE a.mentor_interview = false
        """)

        result = conn.execute(query)
        rows = result.mappings().all()

        data = [dict(row) for row in rows]

        if not data:
            print("No mentor interview results found")
            return []

        print("Data fetched successfully:", data)
        return data
        
def dublicate():
    with engine.connect() as conn:
        query = text("""
            SELECT 
                t.full_name,
                t.email,
                t.phone_number,
                a.application_period,
                a.*
            FROM trainees t
            INNER JOIN applications a 
                ON a.trainee_id = t.trainee_id
            WHERE t.full_name IN (
                SELECT full_name
                FROM trainees
                GROUP BY full_name
                HAVING COUNT(*) > 1
            )
            ORDER BY t.full_name, a.application_period, a.application_id;
        """)

        result = conn.execute(query)
        print("Query executed, fetching results...")

        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        print("Data fetched successfully:", data)

        return data


        


def fltered():
    with engine.connect() as conn:
        query = text("""
            SELECT DISTINCT ON (t.full_name, t.email)
                t.full_name,
                t.email,
                t.phone_number,
                a.application_period,
                a.*
            FROM trainees t
            INNER JOIN applications a 
                ON a.trainee_id = t.trainee_id
            WHERE a.application_period = 'VIT3'
            ORDER BY t.full_name, t.email, a.application_id;
        """)

        result = conn.execute(query)
        print("Query executed, fetching results...")

        rows = result.mappings().all()  # Mapping formatında sonuç
        data = [dict(row) for row in rows]  # Dict'e çeviriyoruz
        print("Data fetched successfully:", data)

        return data



def prevvitcheck():
    with engine.connect() as conn:
        query = text("""
            SELECT
                t.full_name,
                t.email,
                a.application_period,
                MIN(a.application_id) AS example_application_id
            FROM applications a
            INNER JOIN trainees t ON a.trainee_id = t.trainee_id
            WHERE a.application_period IN ('VIT1', 'VIT2', 'VIT3')
            GROUP BY t.full_name, t.email, a.application_period
            HAVING COUNT(DISTINCT a.application_period) > 0
            AND t.email IN (
                SELECT t2.email
                FROM applications a2
                INNER JOIN trainees t2 ON a2.trainee_id = t2.trainee_id
                WHERE a2.application_period IN ('VIT1', 'VIT2', 'VIT3')
                GROUP BY t2.email
                HAVING COUNT(DISTINCT a2.application_period) > 1
            )
            ORDER BY t.full_name, a.application_period;
        """)

        result = conn.execute(query)
        print("Query executed, fetching results...")

        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        print(f"Data fetched successfully: {len(data)} rows")

        return data

        
def differenreg():
    with engine.connect() as conn:
        query = text("""
            WITH ranked AS (
                SELECT 
                    t.*,
                    a.*,
                    ROW_NUMBER() OVER (PARTITION BY t.full_name ORDER BY a.application_id) AS rn
                FROM applications a
                INNER JOIN trainees t ON a.trainee_id = t.trainee_id
                WHERE a.application_period = 'VIT3'
                  AND t.email NOT IN (
                      SELECT t2.email
                      FROM applications a2
                      INNER JOIN trainees t2 ON a2.trainee_id = t2.trainee_id
                      WHERE a2.application_period IN ('VIT1', 'VIT2')
                  )
            )
            SELECT *
            FROM ranked
            WHERE rn = 1
        """)

        # Parametreyi güvenli şekilde gönderiyoruz
        result = conn.execute(query)
        print("Query executed, fetching results...")

        rows = result.mappings().all()  # Mapping formatında sonuç
        data = [dict(row) for row in rows]  # Dict'e çeviriyoruz
        print("Data fetched successfully:", data)

        return data