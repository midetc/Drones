from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Any, Union, List
from models import Drone, Client, Operator, Operation, Contract

def create_record(session: Session, model: Any, **kwargs) -> str:
    """
    Створює запис для будь-якої моделі.
    """
    try:
        new_record = model(**kwargs)
        session.add(new_record)
        session.commit()
        return f"Record in {model.__name__} created successfully!"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Error: {str(e)}"

def get_record(session: Session, model: Any, record_id: int) -> Union[Any, None]:
    """
    Отримує запис за його ID.
    """
    return session.get(model, record_id)

def update_record(session: Session, model: Any, record_id: int, **kwargs) -> str:
    """
    Оновлює запис за його ID.
    """
    try:
        record = session.get(model, record_id)
        if not record:
            return f"Record with ID {record_id} in {model.__name__} not found."
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        return f"Record with ID {record_id} in {model.__name__} updated successfully!"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Error: {str(e)}"

def delete_record(session: Session, model: Any, record_id: int) -> str:
    """
    Видаляє запис за його ID.
    """
    try:
        record = session.get(model, record_id)
        if not record:
            return f"Record with ID {record_id} in {model.__name__} not found."
        session.delete(record)
        session.commit()
        return f"Record with ID {record_id} in {model.__name__} deleted successfully!"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Error: {str(e)}"

def list_drones_by_operator(session: Session, operator_id: int) -> Union[str, List[Drone]]:
    """
    Повертає список дронів оператора.
    """
    operator = session.query(Operator).filter_by(id=operator_id).first()
    if not operator:
        return f"Operator with ID {operator_id} not found."
    return operator.drones

def list_operations_by_drone(session: Session, drone_id: int) -> Union[str, List[Operation]]:
    """
    Повертає список операцій для дрона.
    """
    drone = session.query(Drone).filter_by(id=drone_id).first()
    if not drone:
        return f"Drone with ID {drone_id} not found."
    return drone.operations

def list_contracts_by_client(session: Session, client_id: int) -> Union[str, List[Contract]]:
    """
    Повертає список контрактів клієнта.
    """
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        return f"Client with ID {client_id} not found."
    return client.contracts

def count_operations_by_period(session: Session, start_date, end_date) -> int:
    """
    Повертає кількість операцій за вказаний період.
    """
    return session.query(Operation).filter(Operation.date.between(start_date, end_date)).count()

def drone_load_report(session: Session) -> dict:
    """
    Генерує звіт про завантаженість дронів.
    """
    drones = session.query(Drone).all()
    report = {}
    for drone in drones:
        report[drone.name] = len(drone.operations)
    return report

def add_operation_to_drone(session: Session, drone_id: int, operation_id: int) -> str:
    """
    Додає операцію до дрона, перевіряючи, чи існує така асоціація.
    """
    drone = session.query(Drone).filter_by(id=drone_id).first()
    operation = session.query(Operation).filter_by(id=operation_id).first()

    if not drone:
        return f"Drone with ID {drone_id} not found."
    if not operation:
        return f"Operation with ID {operation_id} not found."

    if operation not in drone.operations:
        drone.operations.append(operation)
        try:
            session.commit()
            return f"Operation {operation_id} successfully added to drone {drone_id}."
        except SQLAlchemyError as e:
            session.rollback()
            return f"Error: {str(e)}"
    else:
        return f"Operation {operation_id} is already assigned to drone {drone_id}."
