from fastapi import APIRouter, HTTPException
from models.payment_models import CreatePayment, Payment
from database import get_db_connection
from typing import List
from mysql.connector import Error as MySQLError

router = APIRouter()

@router.post("/payments/")
async def create_payment(payments: List[CreatePayment]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO payments (reservation_id, amount, payment_date, payment_method)
        VALUES (%s, %s, %s, %s)
        """
        
        values = [(p.reservation_id, p.amount, p.payment_date, p.payment_method) 
                 for p in payments]
        cursor.executemany(query, values)
        conn.commit()
        
        return {"message": "Payments created successfully"}
        
    except MySQLError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/payments/", response_model=List[Payment])
async def list_payments():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM payments ORDER BY payment_date DESC"
        cursor.execute(query)
        payments = cursor.fetchall()
        return [Payment(**payment) for payment in payments]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 