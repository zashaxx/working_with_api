from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://postgres:test1234!@localhost:5432/TodoApplicationServer"
# )

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://root:test1234!@localhost:3306/TodoApplicationServer"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
