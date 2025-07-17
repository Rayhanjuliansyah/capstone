from sqlalchemy import Column, Integer, Date
from database import Base

class Prediction(Base):
    __tablename__ = "prediksi"

    id = Column(Integer, primary_key=True, index=True)
    tanggal = Column(Date)
    dbd = Column(Integer)
    ispa = Column(Integer)
    influenza = Column(Integer)
