from .client_routes import router as client_router
from .room_routes import router as room_router
from .reservation_routes import router as reservation_router
from .service_routes import router as service_router
from .payment_routes import router as payment_router
from .maintenance_routes import router as maintenance_router
from .reports_routes import router as reports_router

__all__ = [
    'client_router',
    'room_router',
    'reservation_router',
    'service_router',
    'payment_router',
    'maintenance_router',
    'reports_router'
] 