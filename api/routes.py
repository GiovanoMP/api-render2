from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Numeric
from typing import List, Optional
from . import models, schemas
from .database import get_db
from datetime import date, datetime
from decimal import Decimal

router = APIRouter()

@router.get("/health")
def health_check():
    """Rota de verificação de saúde da API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.get("/transactions/", response_model=List[schemas.TransactionResponse])
def get_transactions(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    pais: Optional[str] = Query(default=None),
    categoria: Optional[str] = Query(default=None),
    data_inicio: date = Query(
        default=date(2011, 1, 4),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    data_fim: date = Query(
        default=date(2011, 12, 31),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna lista de transações com filtros opcionais
    """
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=400,
            detail="Data final deve ser maior ou igual à data inicial"
        )

    query = db.query(models.Transaction)
    
    if pais:
        query = query.filter(models.Transaction.Pais == pais)
    if categoria:
        query = query.filter(models.Transaction.CategoriaProduto == categoria)
    
    query = query.filter(
        models.Transaction.DataFatura >= data_inicio,
        models.Transaction.DataFatura <= data_fim
    )
    
    total = query.count()
    transactions = query.offset(skip).limit(limit).all()
    
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma transação encontrada com os filtros especificados"
        )
    
    return transactions

@router.get("/transactions/summary", response_model=schemas.SummaryResponse)
def get_transactions_summary(
    data_inicio: date = Query(
        default=date(2011, 1, 4),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    data_fim: date = Query(
        default=date(2011, 12, 31),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna resumo agregado das transações
    """
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=400,
            detail="Data final deve ser maior ou igual à data inicial"
        )

    result = db.query(
        func.count(models.Transaction.id).label('total_transactions'),
        func.sum(models.Transaction.ValorTotalFatura).label('total_value'),
        func.count(models.Transaction.IDCliente.distinct()).label('unique_customers'),
        func.sum(models.Transaction.Quantidade).label('total_quantity'),
        func.avg(models.Transaction.PrecoUnitario).label('average_unit_price'),
        func.count(models.Transaction.Pais.distinct()).label('unique_countries'),
        func.count(models.Transaction.CategoriaProduto.distinct()).label('unique_categories')
    ).filter(
        models.Transaction.DataFatura >= data_inicio,
        models.Transaction.DataFatura <= data_fim
    ).first()
    
    if not result.total_transactions:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma transação encontrada no período especificado"
        )
    
    return {
        "total_transactions": result.total_transactions,
        "total_value": result.total_value or Decimal('0'),
        "unique_customers": result.unique_customers,
        "total_quantity": result.total_quantity,
        "average_unit_price": result.average_unit_price or Decimal('0'),
        "unique_countries": result.unique_countries,
        "unique_categories": result.unique_categories
    }

@router.get("/transactions/by-category", response_model=List[schemas.CategorySummary])
def get_transactions_by_category(
    data_inicio: date = Query(
        default=date(2011, 1, 4),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    data_fim: date = Query(
        default=date(2011, 12, 31),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    min_vendas: int = Query(default=1, ge=1),
    db: Session = Depends(get_db)
):
    """
    Retorna análise de vendas por categoria
    """
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=400,
            detail="Data final deve ser maior ou igual à data inicial"
        )

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
    ).group_by(
        models.Transaction.CategoriaProduto
    ).having
