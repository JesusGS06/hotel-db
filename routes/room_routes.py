from fastapi import APIRouter, HTTPException
from models.room_models import CreateRoom, Room, RoomStatus
from database import get_db_connection
from typing import List
from mysql.connector import Error as MySQLError

router = APIRouter()

@router.post("/rooms/")
async def create_room(rooms: List[CreateRoom]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO rooms (room_number, type, price, status)
        VALUES (%s, %s, %s, %s)
        """
        
        values = [(room.room_number, room.type, room.price, room.status) 
                 for room in rooms]
        cursor.executemany(query, values)
        conn.commit()
        
        return {"message": "Rooms created successfully"}
        
    except MySQLError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/rooms/", response_model=List[Room])
async def list_rooms():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM rooms ORDER BY room_id DESC"
        cursor.execute(query)
        rooms = cursor.fetchall()
        return [Room(**room) for room in rooms]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()