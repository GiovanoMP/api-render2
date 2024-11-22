from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
from .config import get_settings

settings = get_settings()

def get_db_url():
    url = settings.DATABASE_URL
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    # Trata caracteres especiais na senha
    parsed = urllib.parse.urlparse(url)
    if parsed.password:
        safe_password = urllib.parse.quote_plus(parsed.password)
        url = f"postgresql://{parsed.username}:{safe_password}@{parsed.hostname}:{parsed.port}{parsed.path}"
    
    return url

engine = create_engine(
    get_db_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
