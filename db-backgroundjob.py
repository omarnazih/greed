from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import sqlalchemy

import database as db

engine = sqlalchemy.create_engine(user_cfg["Database"]["engine"])
session = sqlalchemy.orm.sessionmaker(bind=engine)()

# create a function to delete old data from the table
def delete_old_data():
    # create a SQL query to delete rows older than 1 day
    old_product=session.query(db.Product).filter(db.Product.deleted == True).all()    
    print(old_product)
    for product in old_product:
        print(product)
        session.delete(product)

    session.commit()

delete_old_data()
# create a scheduler that runs the delete_old_data function every day
scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_data, 'interval', days=1)
scheduler.start()