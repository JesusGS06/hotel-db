from fastapi import APIRouter, HTTPException
from database import get_db_connection
from typing import List
from mysql.connector import Error as MySQLError
from datetime import date

router = APIRouter()

@router.get("/reports/rooms/occupancy-rate")
async def get_room_occupancy_rate():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            r.room_id,
            r.room_number,
            COUNT(res.reservation_id) as total_reservations,
            (COUNT(res.reservation_id) * 100.0 / 
                (SELECT COUNT(*) FROM reservations)) as occupancy_rate
        FROM rooms r
        LEFT JOIN reservations res ON r.room_id = res.room_id
        GROUP BY r.room_id, r.room_number
        ORDER BY occupancy_rate DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/clients/top-spenders")
async def get_top_spending_clients():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            c.client_id,
            c.first_name,
            c.last_name,
            COUNT(DISTINCT r.reservation_id) as total_reservations,
            SUM(p.amount) as total_spent
        FROM clients c
        JOIN reservations r ON c.client_id = r.client_id
        JOIN payments p ON r.reservation_id = p.reservation_id
        GROUP BY c.client_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
        LIMIT 10
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/services/most-requested")
async def get_most_requested_services():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            s.service_id,
            s.name,
            COUNT(rs.reservation_service_id) as times_requested,
            SUM(rs.quantity) as total_quantity,
            SUM(s.cost * rs.quantity) as total_revenue
        FROM services s
        LEFT JOIN reservation_services rs ON s.service_id = rs.service_id
        GROUP BY s.service_id, s.name
        ORDER BY times_requested DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/rooms/maintenance-frequency")
async def get_room_maintenance_frequency():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            r.room_id,
            r.room_number,
            COUNT(m.maintenance_id) as maintenance_count,
            MIN(m.maintenance_date) as first_maintenance,
            MAX(m.maintenance_date) as last_maintenance
        FROM rooms r
        LEFT JOIN maintenance m ON r.room_id = m.room_id
        GROUP BY r.room_id, r.room_number
        ORDER BY maintenance_count DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/revenue/monthly")
async def get_monthly_revenue():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            YEAR(p.payment_date) as year,
            MONTH(p.payment_date) as month,
            COUNT(DISTINCT r.reservation_id) as total_reservations,
            SUM(p.amount) as total_revenue,
            AVG(p.amount) as average_payment
        FROM payments p
        JOIN reservations r ON p.reservation_id = r.reservation_id
        GROUP BY YEAR(p.payment_date), MONTH(p.payment_date)
        ORDER BY year DESC, month DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/clients/reservation-history/{client_id}")
async def get_client_reservation_history(client_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            r.reservation_id,
            r.start_date,
            r.end_date,
            rm.room_number,
            rm.type,
            COALESCE(SUM(p.amount), 0) as total_paid,
            COUNT(rs.service_id) as services_used
        FROM reservations r
        JOIN rooms rm ON r.room_id = rm.room_id
        LEFT JOIN payments p ON r.reservation_id = p.reservation_id
        LEFT JOIN reservation_services rs ON r.reservation_id = rs.reservation_id
        WHERE r.client_id = %s
        GROUP BY r.reservation_id, r.start_date, r.end_date, rm.room_number, rm.type
        ORDER BY r.start_date DESC
        """
        cursor.execute(query, (client_id,))
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/rooms/revenue")
async def get_room_revenue():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            r.room_id,
            r.room_number,
            r.type,
            COUNT(res.reservation_id) as total_reservations,
            COALESCE(SUM(p.amount), 0) as total_revenue,
            COALESCE(AVG(p.amount), 0) as average_revenue_per_reservation
        FROM rooms r
        LEFT JOIN reservations res ON r.room_id = res.room_id
        LEFT JOIN payments p ON res.reservation_id = p.reservation_id
        GROUP BY r.room_id, r.room_number, r.type
        ORDER BY total_revenue DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/reservations/duration-analysis")
async def get_reservation_duration_analysis():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            YEAR(start_date) as year,
            MONTH(start_date) as month,
            COUNT(*) as total_reservations,
            AVG(DATEDIFF(end_date, start_date)) as avg_stay_duration,
            MIN(DATEDIFF(end_date, start_date)) as min_stay_duration,
            MAX(DATEDIFF(end_date, start_date)) as max_stay_duration
        FROM reservations
        GROUP BY YEAR(start_date), MONTH(start_date)
        ORDER BY year DESC, month DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/payments/method-analysis")
async def get_payment_method_analysis():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            payment_method,
            COUNT(*) as total_payments,
            SUM(amount) as total_amount,
            AVG(amount) as average_amount,
            MIN(amount) as min_amount,
            MAX(amount) as max_amount
        FROM payments
        GROUP BY payment_method
        ORDER BY total_amount DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/rooms/available-now")
async def get_available_rooms_now():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT room_id, room_number, type, price
        FROM rooms
        WHERE status = 'Available'
        AND room_id NOT IN (
            SELECT room_id FROM reservations
            WHERE CURDATE() BETWEEN start_date AND end_date
        )
        ORDER BY room_number
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/clients/active")
async def get_active_clients():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT DISTINCT c.client_id, c.first_name, c.last_name, c.email
        FROM clients c
        JOIN reservations r ON c.client_id = r.client_id
        WHERE r.end_date >= CURDATE()
        ORDER BY c.last_name, c.first_name
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/rooms/maintenance-today")
async def get_rooms_in_maintenance_today():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT r.room_number, m.description, m.maintenance_date
        FROM maintenance m
        JOIN rooms r ON m.room_id = r.room_id
        WHERE DATE(m.maintenance_date) = CURDATE()
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/reservations/today")
async def get_todays_reservations():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT r.reservation_id, c.first_name, c.last_name, rm.room_number
        FROM reservations r
        JOIN clients c ON r.client_id = c.client_id
        JOIN rooms rm ON r.room_id = rm.room_id
        WHERE DATE(r.start_date) = CURDATE()
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/payments/today")
async def get_todays_payments():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT payment_id, amount, payment_method
        FROM payments
        WHERE DATE(payment_date) = CURDATE()
        ORDER BY payment_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@router.get("/reports/services/basic")
async def get_basic_services():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT service_id, name, cost
        FROM services
        ORDER BY cost
        """
        cursor.execute(query)
        return cursor.fetchall()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()