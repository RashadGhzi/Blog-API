from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@postgresserver/blog-app"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:2gb*-*cB-A4*4dE1EDgG34-A-D3E3cbd@monorail.proxy.rlwy.net:58473/railway"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
