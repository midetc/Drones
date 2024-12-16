from database import Session, engine
from models import Base, Drone, Operator, Client, Contract, Operation
from crud import (
    create_record,
    get_record,
    update_record,
    delete_record,
    list_drones_by_operator,
    list_operations_by_drone,
    list_contracts_by_client,
    count_operations_by_period,
    drone_load_report,
    add_operation_to_drone
)
from datetime import datetime

def main() -> None:
    """
    Головна функція для тестування CRUD-операцій та інших функцій.
    """
    # Створюємо таблиці
    Base.metadata.create_all(engine)

    with Session() as session:
        try:
            # ТЕСТ 1: Створення записів (Operator, Client)
            print("\n=== TEST 1: CREATE RECORDS ===")
            operator_result = create_record(session, Operator, name="John Doe", experience_level="Expert")
            print(operator_result)

            client_result = create_record(session, Client, name="Client A", contact_info="clienta@example.com")
            print(client_result)

            # ТЕСТ 2: Отримання створених записів
            print("\n=== TEST 2: GET CREATED RECORDS ===")
            operator = session.query(Operator).filter_by(name="John Doe").first()
            client = session.query(Client).filter_by(name="Client A").first()

            if operator:
                print(f"Operator found: {operator.name}, Experience: {operator.experience_level}")
            else:
                print("Operator not found after creation.")

            if client:
                print(f"Client found: {client.name}, Contact Info: {client.contact_info}")
            else:
                print("Client not found after creation.")

            # ТЕСТ 3: Створення контракту
            print("\n=== TEST 3: CREATE CONTRACT ===")
            contract_result = create_record(
                session,
                Contract,
                client_id=client.id,
                start_date=datetime(2023, 1, 1),
                end_date=datetime(2023, 12, 31)
            )
            print(contract_result)

            # ТЕСТ 4: Створення дрона
            print("\n=== TEST 4: CREATE DRONE ===")
            drone_result = create_record(
                session,
                Drone,
                name="Drone Alpha",
                type="Recon",
                status="Active",
                operator_id=operator.id
            )
            print(drone_result)

            # ТЕСТ 5: Створення операції
            print("\n=== TEST 5: CREATE OPERATION ===")
            contract = session.query(Contract).filter_by(client_id=client.id).first()
            if not contract:
                print("Contract not found. Aborting operation creation.")
                return

            operation_result = create_record(
                session,
                Operation,
                name="Operation Recon",
                date=datetime(2023, 7, 15),
                description="Recon mission",
                contract_id=contract.id
            )
            print(operation_result)

            # ТЕСТ 6: Отримання запису (get_record)
            print("\n=== TEST 6: GET RECORD ===")
            operator_from_db = get_record(session, Operator, operator.id)
            if operator_from_db:
                print(f"Operator: {operator_from_db.name}, Experience: {operator_from_db.experience_level}")
            else:
                print("Operator not found.")

            # ТЕСТ 7: Оновлення запису (update_record)
            print("\n=== TEST 7: UPDATE RECORD ===")
            update_result = update_record(session, Operator, operator.id, experience_level="Master")
            print(update_result)
            updated_operator = get_record(session, Operator, operator.id)
            if updated_operator:
                print(f"Updated Operator: {updated_operator.name}, Experience: {updated_operator.experience_level}")
            else:
                print("Updated Operator not found.")

            # ТЕСТ 8: Видалення запису (delete_record)
            print("\n=== TEST 8: DELETE RECORD ===")
            delete_result = delete_record(session, Operation, 1)  # Спроба видалити операцію з ID 1
            print(delete_result)
            deleted_operation = get_record(session, Operation, 1)
            print(f"Operation after delete: {deleted_operation}")

            # ТЕСТ 9: Список дронів за оператором (list_drones_by_operator)
            print("\n=== TEST 9: LIST DRONES BY OPERATOR ===")
            drones = list_drones_by_operator(session, operator.id)
            if isinstance(drones, list):
                print(f"Drones for Operator {operator.id}: {[drone.name for drone in drones]}")
            else:
                print(drones)

            # ТЕСТ 10: Список операцій за дроном (list_operations_by_drone)
            print("\n=== TEST 10: LIST OPERATIONS BY DRONE ===")
            drone = session.query(Drone).filter_by(name="Drone Alpha").first()
            operation = session.query(Operation).filter_by(name="Operation Recon").first()
            if drone and operation:
                # Перше додавання
                print(add_operation_to_drone(session, drone.id, operation.id))
                # Спроба додати знову ту ж операцію
                print(add_operation_to_drone(session, drone.id, operation.id))

            operations = list_operations_by_drone(session, drone.id)
            if isinstance(operations, list) and operations:
                print(f"Operations for Drone {drone.id}: {[op.name for op in operations]}")
            else:
                print("No valid operations found for this Drone.")

            # ТЕСТ 11: Список контрактів за клієнтом (list_contracts_by_client)
            print("\n=== TEST 11: LIST CONTRACTS BY CLIENT ===")
            contracts = list_contracts_by_client(session, client.id)
            if isinstance(contracts, list) and contracts:
                print(f"Contracts for Client {client.id}: {[contract.id for contract in contracts]}")
            else:
                print("No contracts found for Client.")

            # ТЕСТ 12: Підрахунок операцій за період (count_operations_by_period)
            print("\n=== TEST 12: COUNT OPERATIONS BY PERIOD ===")
            operation_count = count_operations_by_period(session, datetime(2023, 1, 1), datetime(2023, 12, 31))
            print(f"Operations in 2023: {operation_count}")

            # ТЕСТ 13: Звіт по завантаженості дронів (drone_load_report)
            print("\n=== TEST 13: DRONE LOAD REPORT ===")
            report = drone_load_report(session)
            print("Drone Load Report:", report)

        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()

if __name__ == "__main__":
    main()
