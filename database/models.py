from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    sector = Column(String)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    headline = Column(String)
    source = Column(String)
    url = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    event_type = Column(String)
    description = Column(String)


class Valuation(Base):
    __tablename__ = "valuations"

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    valuation_billions = Column(Float)


class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer)
    sentiment = Column(String)
    
class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True)
    run_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    articles_processed = Column(Integer)
    events_created = Column(Integer)