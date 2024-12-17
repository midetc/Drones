from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

drone_operations = Table(
    'drone_operations',
    Base.metadata,
    Column('drone_id', Integer, ForeignKey('drones.id'), primary_key=True),
    Column('operation_id', Integer, ForeignKey('operations.id'), primary_key=True)
)

class MaintenanceLog(Base):
    __tablename__ = 'maintenance_logs'
    id = Column(Integer, primary_key=True)
    drone_id = Column(Integer, ForeignKey('drones.id'))
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)

    drone = relationship("Drone", back_populates="maintenance_logs")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)

    contracts = relationship("Contract", back_populates="client")

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)

    client = relationship("Client", back_populates="contracts")
    operations = relationship("Operation", back_populates="contract")

class Operator(Base):
    __tablename__ = 'operators'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)

    drones = relationship("Drone", back_populates="operator")

class Drone(Base):
    __tablename__ = 'drones'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    operator_id = Column(Integer, ForeignKey('operators.id'))

    operator = relationship("Operator", back_populates="drones")
    operations = relationship("Operation", secondary=drone_operations, back_populates="drones")
    maintenance_logs = relationship("MaintenanceLog", back_populates="drone")

class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    contract_id = Column(Integer, ForeignKey('contracts.id'))

    contract = relationship("Contract", back_populates="operations")
    drones = relationship("Drone", secondary=drone_operations, back_populates="operations")
