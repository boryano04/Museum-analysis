from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/assignment/10-11")
def get_assignment():
    conn = sqlite3.connect("museum.db")
    cursor = conn.cursor()

    # задание 10
    query_10 = """
    SELECT t.name, COUNT(w.id)
    FROM types t
    LEFT JOIN wings w ON w.type_id = t.id
    GROUP BY t.id;
    """
    cursor.execute(query_10)
    res10 = cursor.fetchall()

    # задание 11
    query_11 = """
    SELECT 
        t.name,
        ROUND(
            (SUM(m.price * w.profit * p.scale) - SUM(m.price)) 
            / SUM(m.price) * 100, 2
        ) as roi
    FROM moves m
    JOIN wings w ON m.wing_id = w.id
    JOIN types t ON w.type_id = t.id
    JOIN places p ON m.place_id = p.id
    GROUP BY t.id;
    """
    cursor.execute(query_11)
    res11 = cursor.fetchall()

    conn.close()

    return {
        "task10": res10,
        "task11": res11
    }
