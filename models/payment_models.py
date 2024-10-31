from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    TRANSFER = "Transfer"

class CreatePayment(BaseModel):
    reservation_id: int = Field(..., description="Reservation's ID")
    amount: Decimal = Field(..., description="Payment amount")
    payment_date: date = Field(..., description="Payment date")
    payment_method: PaymentMethod = Field(..., description="Payment method")

class Payment(CreatePayment):
    payment_id: int = Field(..., description="Payment's unique ID") 