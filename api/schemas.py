from pydantic import BaseModel
from typing import List
from datetime import datetime
from decimal import Decimal

class TransactionBase(BaseModel):
    id: int
    created_at: datetime
    NumeroFatura: str
    CodigoProduto: str
    Descricao: str
    Quantidade: int
    DataFatura: datetime
    PrecoUnitario: Decimal
    IDCliente: str
    Pais: str
    CategoriaProduto: str
    CategoriaPreco: str
    ValorTotalFatura: Decimal
    FaturaUnica: bool
    Ano: int
    Mes: int
    Dia: int
    DiaSemana: int

    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    created_at: datetime
    NumeroFatura: str
    CodigoProduto: str
    Descricao: str
    Quantidade: int
    DataFatura: datetime
    PrecoUnitario: Decimal
    IDCliente: str
    Pais: str
    CategoriaProduto: str
    CategoriaPreco: str
    ValorTotalFatura: Decimal
    FaturaUnica: bool
    Ano: int
    Mes: int
    Dia: int
    DiaSemana: int

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total_transactions: int
    total_value: Decimal
    unique_customers: int
    total_quantity: int
    average_unit_price: Decimal
    unique_countries: int
    unique_categories: int

class CategorySummary(BaseModel):
    categoria: str
    total_vendas: int
    valor_total: Decimal
    quantidade_total: int
    ticket_medio: float

class CountrySummary(BaseModel):
    pais: str
    total_vendas: int
    valor_total: Decimal
    quantidade_clientes: int
    ticket_medio: float
