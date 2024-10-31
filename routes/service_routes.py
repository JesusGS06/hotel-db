from fastapi import APIRouter, HTTPException
from models.service_models import CreateService, Service, CreateReservationService, ReservationService
from database import get_db_connection
from typing import List
from mysql.connector import Error as MySQLError

router = APIRouter()

@router.post("/services/")
async def create_service(services: List[CreateService]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO services (name, description, cost)
        VALUES (%s, %s, %s)
        """
        
        values = [(s.name, s.description, s.cost) for s in services]
        cursor.executemany(query, values)
        conn.commit()
        
        return {"message": "Services created successfully"}
        
    except MySQLError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/services/", response_model=List[Service])
async def list_services():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM services ORDER BY service_id DESC"
        cursor.execute(query)
        services = cursor.fetchall()
        return [Service(**service) for service in services]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.post("/reservation-services/")
async def add_services_to_reservation(reservation_services: List[CreateReservationService]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO reservation_services (reservation_id, service_id, quantity)
        VALUES (%s, %s, %s)
        """
        
        values = [(rs.reservation_id, rs.service_id, rs.quantity) 
                 for rs in reservation_services]
        cursor.executemany(query, values)
        conn.commit()
        
        return {"message": "Services added to reservation successfully"}
        
    except MySQLError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/reservation-services/{reservation_id}", response_model=List[ReservationService])
async def get_reservation_services(reservation_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT * FROM reservation_services 
        WHERE reservation_id = %s
        """
        cursor.execute(query, (reservation_id,))
        services = cursor.fetchall()
        return [ReservationService(**service) for service in services]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 