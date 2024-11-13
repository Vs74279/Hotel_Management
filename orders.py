from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database import get_db
from models import Order, OrderStatus, OrderItem, User
from schemas import OrderCreate, OrderUpdate, OrderResponse

order_router = APIRouter()

@order_router.post("/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    
    db_order = Order(customer_id=order.customer_id, status=OrderStatus.pending)
    for item in order.items:
        db_order_item = OrderItem(product_id=item['product_id'], quantity=item['quantity'])
        db_order.items.append(db_order_item)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@order_router.get("/orders")
async def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@order_router.put("/orders/{order_id}")
async def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update only the status field
    if order_update.status:
        db_order.status = order_update.status

    db.commit()
    db.refresh(db_order)
    return db_order


@order_router.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}