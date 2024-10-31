from fastapi import APIRouter, HTTPException
from models.maintenance_models import CreateMaintenance, Maintenance
from database import get_db_connection
from typing import List
from mysql.connector import Error as MySQLError

router = APIRouter()

@router.post("/maintenance/")
async def create_maintenance(maintenance_records: List[CreateMaintenance]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO maintenance (room_id, maintenance_date, description)
        VALUES (%s, %s, %s)
        """
        
        values = [(m.room_id, m.maintenance_date, m.description) 
                 for m in maintenance_records]
        cursor.executemany(query, values)
        conn.commit()
        
        return {"message": "Maintenance records created successfully"}
        
    except MySQLError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/maintenance/", response_model=List[Maintenance])
async def list_maintenance():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM maintenance ORDER BY maintenance_date DESC"
        cursor.execute(query)
        records = cursor.fetchall()
        return [Maintenance(**record) for record in records]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/maintenance/room/{room_id}", response_model=List[Maintenance])
async def get_room_maintenance(room_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM maintenance WHERE room_id = %s ORDER BY maintenance_date DESC"
        cursor.execute(query, (room_id,))
        records = cursor.fetchall()
        return [Maintenance(**record) for record in records]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 