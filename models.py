from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enums for predefined fields
class DroneType(enum.Enum):
    RECONNAISSANCE = "Розвідувальний"
    BOMBER = "Бомбер"
    KAMIKAZE = "Камікадзе"
    MULTIFUNCTIONAL = "Багатофункціональний"


class CharacteristicKey(enum.Enum):
    MAX_FLIGHT_ALT = "Максимальна висота польоту"
    FLIGHT_RANGE = "Дальність польоту"
    AUTONOMY_TIME = "Час автономної роботи"
    MAX_PAYLOAD = "Максимальне навантаження"
    WEAPON_TYPE = "Тип озброєння"
    CONTROL_SYSTEM = "Система управління"

# Models
class Drone(Base):
    __tablename__ = "drones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(DroneType, name="drone_type"), nullable=False)  # Используем Enum
    cost = Column(Float, nullable=False)
    production_date = Column(Date, nullable=False)
    characteristics = relationship("DroneCharacteristic",
                                   back_populates="drone",
                                   cascade="all, delete-orphan"
                                   )


class DroneCharacteristic(Base):
    __tablename__ = "drone_characteristics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(Enum(CharacteristicKey, name="characteristic_key"), nullable=False)  # Используем Enum
    value = Column(String, nullable=True)
    drone_id = Column(Integer, ForeignKey("drones.id"))
    drone = relationship("Drone", back_populates="characteristics")
