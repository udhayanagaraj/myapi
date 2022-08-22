
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


sqlalchemy_database_url=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine=create_engine(sqlalchemy_database_url)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()


#dependices
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


#raw sql connection


# while True:
#     try:
#         connection=psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="2001",cursor_factory=RealDictCursor)
#         cursor=connection.cursor()
#         print("Database connection was sucessful")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("error:",error)
#         time.sleep(2)