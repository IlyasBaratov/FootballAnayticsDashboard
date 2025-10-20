from sqlalchemy import create_engine

# Database URL format:
# 'dialect+driver://username:password@host:port/database_name'
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/footballdb"

engine = create_engine(DATABASE_URL)