from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql+psycopg2://postgres:oyeleye1608@localhost:5432/fastapi_demo"
engine = create_engine(db_url)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
