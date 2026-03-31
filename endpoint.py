from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/assignment/10-11")
def get_assignment():
    conn = sqlite3.connect("museum.db")
    cursor = conn.cursor()

    query_10_1 = """
    SELECT *
    FROM types
    WHERE name LIKE '%изделие%';
    """
    cursor.execute(query_10_1)
    res10_1 = cursor.fetchall()

    query_10_2 = """
    SELECT 
        t.id AS type_id,
        t.name AS type_name,
        COUNT(w.id) AS items_count
    FROM types t
    LEFT JOIN wings w ON w.type_id = t.id
    GROUP BY t.id, t.name
    ORDER BY items_count DESC, t.name;
    """
    cursor.execute(query_10_2)
    res10_2 = cursor.fetchall()

    query_11 = """
    SELECT 
        t.id AS type_id,
        t.name AS type_name,
        ROUND(SUM(m.price * w.profit * p.scale), 2) AS total_revenue,
        ROUND(SUM(m.price), 2) AS marketing_cost,
        ROUND(AVG(w.profit), 2) AS avg_profit,
        ROUND(
            ((SUM(m.price * w.profit * p.scale) - SUM(m.price)) / SUM(m.price)) * 100,
            2
        ) AS roi_percent
    FROM moves m
    JOIN wings w ON m.wing_id = w.id
    JOIN types t ON w.type_id = t.id
    JOIN places p ON m.place_id = p.id
    GROUP BY t.id, t.name
    HAVING SUM(m.price) > 0
    ORDER BY roi_percent DESC, total_revenue DESC;
    """
    cursor.execute(query_11)
    res11 = cursor.fetchall()

    conn.close()

    return {
        "task10_1": res10_1,
        "task10_2": res10_2,
        "task11": res11
    }
