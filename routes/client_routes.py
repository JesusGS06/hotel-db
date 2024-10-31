from fastapi import APIRouter, HTTPException
from models.client_models import CreateClient, Client
from database import get_db_connection
from typing import List
from mysql.connector import Error as MySQLError

router = APIRouter()

@router.post("/clients/")
async def create_client(clients: List[CreateClient]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO clients (first_name, last_name, email, phone)
        VALUES (%s, %s, %s, %s)
        """
        
        values = [(client.first_name, client.last_name, client.email, client.phone) 
                 for client in clients]
        cursor.executemany(query, values)
        conn.commit()
        
        return {"message": "Clients created successfully"}
        
    except MySQLError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/clients/", response_model=List[Client])
async def list_clients():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM clients ORDER BY client_id DESC"
        cursor.execute(query)
        clients = cursor.fetchall()
        return [Client(**client) for client in clients]
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 