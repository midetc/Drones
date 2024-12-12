from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class DronesType(Base):
    __tablename__ = "drones_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    drones = relationship("Drones", back_populates="drone_type")

class Drones(Base):
    __tablename__ = "drones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    drone_type_id = Column(Integer, ForeignKey("drones_types.id"), nullable=False)
    drone_type = relationship("DronesType", back_populates="drones")
    price = Column(Integer, nullable=True)
