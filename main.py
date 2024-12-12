from database import Session, engine
from models import Base, Drone, DroneCharacteristic, DroneType
from datetime import datetime


def main():
    session = Session()

    try:
        # drones = [
        #     Drone(
        #         name="Kolyada",
        #         type=DroneType.BOMBER,
        #         cost=15000.0,
        #         production_date=datetime(2023, 11, 21),
        #         characteristics=[
        #             DroneCharacteristic(key="Speed", value="70"),
        #             DroneCharacteristic(key="Range", value="300 km")
        #         ]
        #     ),
        #     Drone(
        #         name="Phantom",
        #         type=DroneType.BOMBER,
        #         cost=500.0,
        #         production_date=datetime(2022, 3, 22),
        #         characteristics=[
        #             DroneCharacteristic(key="Speed", value="50"),
        #             DroneCharacteristic(key="Battery", value="5 hours")
        #         ]
        #     ),
        # ]

        # session.add_all(drones)
        # session.commit()

        drones = session.query(Drone).all.filter(Drone)
        for drone in drones:
            print(f"Drone: {drone.name}, Type: {drone.type.value}, Cost: {drone.cost}")
            print("Characteristics:")
            for char in drone.characteristics:
                print(f"  - {char.key}: {char.value}")

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    main()
