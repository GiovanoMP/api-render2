from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Numeric
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from . import models, schemas
from .database import get_db

router = APIRouter()

@router.get("/transactions/", response_model=List[schemas.TransactionResponse])
def get_transactions(
    skip: int = 0, 
    limit: int = 100, 
    pais: Optional[str] = None,
    categoria: Optional[str] = None,
    data_inicio: date = Query(default=date(2011, 1, 4)),
    data_fim: date = Query(default=date(2011, 12, 31)),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Transaction)
        
        if pais:
            query = query.filter(models.Transaction.Pais == pais)
        if categoria:
            query = query.filter(models.Transaction.CategoriaProduto == categoria)
        if data_inicio:
            query = query.filter(models.Transaction.DataFatura >= data_inicio)
        if data_fim:
            query = query.filter(models.Transaction.DataFatura <= data_fim)
        
        transactions = query.offset(skip).limit(limit).all()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/summary", response_model=schemas.SummaryResponse)
def get_transactions_summary(
    data_inicio: date = Query(default=date(2011, 1, 4)),
    data_fim: date = Query(default=date(2011, 12, 31)),
    db: Session = Depends(get_db)
):
    try:
        result = db.query(
            func.count(models.Transaction.id).label('total_transactions'),
            func.sum(cast(models.Transaction.ValorTotalFatura, Numeric)).label('total_value'),
            func.count(models.Transaction.IDCliente.distinct()).label('unique_customers'),
            func.sum(models.Transaction.Quantidade).label('total_quantity'),
            func.avg(cast(models.Transaction.PrecoUnitario, Numeric)).label('average_unit_price'),
            func.count(models.Transaction.Pais.distinct()).label('unique_countries'),
            func.count(models.Transaction.CategoriaProduto.distinct()).label('unique_categories')
        ).filter(
            models.Transaction.DataFatura >= data_inicio,
            models.Transaction.DataFatura <= data_fim
        ).first()

        if not result:
            raise HTTPException(status_code=404, detail="No data found for the specified period")

        return {
            "total_transactions": result.total_transactions or 0,
            "total_value": result.total_value or Decimal('0'),
            "unique_customers": result.unique_customers or 0,
            "total_quantity": result.total_quantity or 0,
            "average_unit_price": result.average_unit_price or Decimal('0'),
            "unique_countries": result.unique_countries or 0,
            "unique_categories": result.unique_categories or 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/by-category", response_model=List[schemas.CategorySummary])
def get_transactions_by_category(
    data_inicio: date = Query(default=date(2011, 1, 4)),
    data_fim: date = Query(default=date(2011, 12, 31)),
    db: Session = Depends(get_db)
):
    try:
        categories = db.query(
            models.Transaction.CategoriaProduto.label('categoria'),
            func.count(models.Transaction.id).label('total_vendas'),
            func.sum(models.Transaction.ValorTotalFatura).label('valor_total'),
            func.sum(models.Transaction.Quantidade).label('quantidade_total'),
            (func.sum(models.Transaction.ValorTotalFatura) / 
             func.cast(func.count(models.Transaction.id), Numeric)).label('ticket_medio')
        ).filter(
            models.Transaction.DataFatura >= data_inicio,
            models.Transaction.DataFatura <= data_fim
        ).group_by(models.Transaction.CategoriaProduto).all()
        
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/by-country", response_model=List[schemas.CountrySummary])
def get_transactions_by_country(
    data_inicio: date = Query(default=date(2011, 1, 4)),
    data_fim: date = Query(default=date(2011, 12, 31)),
    db: Session = Depends(get_db)
):
    try:
        countries = db.query(
            models.Transaction.Pais.label('pais'),
            func.count(models.Transaction.id).label('total_vendas'),
            func.sum(models.Transaction.ValorTotalFatura).label('valor_total'),
            func.count(models.Transaction.IDCliente.distinct()).label('quantidade_clientes'),
            (func.sum(models.Transaction.ValorTotalFatura) / 
             func.cast(func.count(models.Transaction.id), Numeric)).label('ticket_medio')
        ).filter(
            models.Transaction.DataFatura >= data_inicio,
            models.Transaction.DataFatura <= data_fim
        ).group_by(models.Transaction.Pais).all()
        
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
