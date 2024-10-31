from fastapi import APIRouter, HTTPException
from models.reservation_models import CreateReservation, Reservation
from database import get_db_connection
from typing import List
from mysql.connector import Error as MySQLError

router = APIRouter()

@router.post("/reservations/")
async def create_reservation(reservations: List[CreateReservation]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO reservations (client_id, room_id, start_date, end_date)
        VALUES (%s, %s, %s, %s)
        """
        
        values = [(r.client_id, r.room_id, r.start_date, r.end_date) 
                 for r in reservations]
        cursor.executemany(query, values)
        conn.commit()
        
        return {"message": "Reservations created successfully"}
        
    except MySQLError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/reservations/", response_model=List[Reservation])
async def list_reservations():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM reservations ORDER BY reservation_id DESC"
        cursor.execute(query)
        reservations = cursor.fetchall()
        return [Reservation(**reservation) for reservation in reservations]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/reservations/client/{client_id}", response_model=List[Reservation])
async def get_client_reservations(client_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM reservations WHERE client_id = %s ORDER BY start_date DESC"
        cursor.execute(query, (client_id,))
        reservations = cursor.fetchall()
        return [Reservation(**reservation) for reservation in reservations]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 