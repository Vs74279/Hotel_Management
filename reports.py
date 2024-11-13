from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import date
from database import get_db
from models import Order, OrderItem, Product
from utils import get_current_admin  # Ensure this function checks admin authentication

# Initialize the router for report endpoints
report_router = APIRouter()


@report_router.get("/report/sales")
def get_sales_report(
    start_date: date,  
    end_date: date,    
    db: Session = Depends(get_db),  # Dependency injection for the database session
    current_admin = Depends(get_current_admin)  # Ensure the user is an admin
):
    # Get total revenue: Sum of product prices multiplied by the quantity sold
    total_revenue = db.query(
        func.sum(Product.price * OrderItem.quantity)  
    ).join(
        OrderItem, Product.id == OrderItem.product_id  
    ).join(
        Order, Order.id == OrderItem.order_id  
    ).filter(
        Order.created_at >= start_date, Order.created_at <= end_date  
    ).scalar() or 0  # Return 0 if no results found

    # Get total number of orders: Count orders in the given date range
    order_count = db.query(Order).filter(
        Order.created_at >= start_date,  
        Order.created_at <= end_date  
    ).count()

    # Get most popular menu items: Top 5 items by total quantity sold
    popular_items = db.query(
        Product.name,  # Product name
        func.sum(OrderItem.quantity).label("total_quantity")  # Total quantity sold
    ).join(
        OrderItem, Product.id == OrderItem.product_id  # Join with OrderItem table
    ).join(
        Order, Order.id == OrderItem.order_id  
    ).filter(
        Order.created_at >= start_date, Order.created_at <= end_date  
    ).group_by(
        Product.name  
    ).order_by(
        func.sum(OrderItem.quantity).desc() 
    ).limit(5).all()  # Limit to top 5 items

    # Format the result into a dictionary to return
    report = {
        "total_revenue": total_revenue,  
        "number_of_orders": order_count,  
        "most_popular_items": [{"name": item[0], "quantity": item[1]} for item in popular_items]  
    }

    return report  