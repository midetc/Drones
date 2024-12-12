from database import Session, engine
from models import Base, Drones, DronesType

def main():
    session = Session()

    try:
        drone_type = DronesType(name="Quadcopter")
        session.add(drone_type)
        session.commit()

        drone = Drones(name="DJI Phantom", drone_type_id=drone_type.id, price=1200)
        session.add(drone)
        session.commit()

        drones = session.query(Drones).all()
        for drone in drones:
            print(f"Drone: {drone.name}, Type: {drone.drone_type.name}, Price: {drone.price}")

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    main()
