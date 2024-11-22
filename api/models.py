from sqlalchemy import Column, BigInteger, String, Numeric, Boolean, DateTime, Text
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions_sample"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True))
    NumeroFatura = Column(String)
    CodigoProduto = Column(String)
    Descricao = Column(Text)
    Quantidade = Column(BigInteger)
    DataFatura = Column(DateTime(timezone=True))
    PrecoUnitario = Column(Numeric(precision=10, scale=2))
    IDCliente = Column(String)
    Pais = Column(String)
    CategoriaProduto = Column(String)
    CategoriaPreco = Column(String)
    ValorTotalFatura = Column(Numeric(precision=10, scale=2))
    FaturaUnica = Column(Boolean)
    Ano = Column(BigInteger)
    Mes = Column(BigInteger)
    Dia = Column(BigInteger)
    DiaSemana = Column(BigInteger)
