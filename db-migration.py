from sqlalchemy import create_engine, Table, MetaData, orm
import database as db
from worker import Worker

engine = create_engine('sqlite:///database.sqlite', echo=True)
metadata = MetaData()

users_table = Table('users', metadata, autoload=True, autoload_with=engine)
products_table = Table('products', metadata, autoload=True, autoload_with=engine)
category_table = Table('category', metadata, autoload=True, autoload_with=engine)
subcategory_table = Table('subcategory', metadata, autoload=True, autoload_with=engine)
variation_table = Table('variation', metadata, autoload=True, autoload_with=engine)
product_variation_table = Table('product_variation', metadata, autoload=True, autoload_with=engine)
orders_table = Table('orders', metadata, autoload=True, autoload_with=engine)
orderitems_table = Table('orderitems', metadata, autoload=True, autoload_with=engine)
transactions_table = Table('transactions', metadata, autoload=True, autoload_with=engine)
btc_transactions_table = Table('btc_transactions', metadata, autoload=True, autoload_with=engine)

query = btc_transactions_table.select()

result = engine.execute(query)

engine = create_engine("postgresql+psycopg2://eseencemarket:ck7aJt1pgPsq@ep-dark-haze-497404.eu-central-1.aws.neon.tech/neondb")
session = orm.sessionmaker(bind=engine)()

for row in result:
    import datetime
    timestamp_str = row.timestamp
    timestamp_obj = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    unix_timestamp = int(timestamp_obj.timestamp())        
    rec = db.BtcTransaction(
        user_id= row.user_id,
        price= row.price,
        value= row.value,
        currency= row.currency,
        status= row.status,
        timestamp= unix_timestamp,
        address= row.address,
        txid= row.txid)
    # rec = db.OrderItem(
    #     item_id=row.item_id,
    #     product_id=row.product_id,
    #     order_id=row.order_id       
    # )
    # rec = db.Order(user_id=row.user_id,creation_date=row.creation_date,delivery_date=row.delivery_date,refund_date=row.refund_date,refund_reason=row.refund_reason,notes=row.notes)
    # rec = db.OrderItem(product_id=row.product_id,order_id=row.order_id)
    # rec = db.Variation(name=row.name, quantity=row.quantity, price_diff=row.price_diff)
    # rec = db.ProductVariation(product_id=row.product_id, variation_id=row.variation_id)
    # rec = db.User(user_id=row.user_id, 
    # first_name=row.first_name,
    # last_name=row.last_name,
    # username =row.username,
    # language =row.language,
    # credit = row.credit)

    # date_str = row.timestamp
    # print(date_str)
    # timestamp_str = row.timestamp
    # timestamp_obj = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    # unix_timestamp = int(timestamp_obj.timestamp())    
    # timestamp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').timestamp()

    # rec = db.BtcTransaction(transaction_id= row.transaction_id,
    #     user_id= row.user_id,
    #     price= row.price,
    #     value= row.value,
    #     currency= row.currency,
    #     status= row.status,
    #     timestamp= unix_timestamp,
    #     address= row.address,
    #     txid= row.txid)
    # rec = db.OrderItem(
    #     item_id=row.item_id,
    #     product_id=row.product_id,
    #     order_id=row.order_id
    # )
#     rec = db.Transaction(
#     user_id=row.user_id,
#     value=row.value,
#     refunded=row.refunded,
#     notes=row.notes,
#     provider=row.provider,
#     telegram_charge_id=row.telegram_charge_id,
#     provider_charge_id=row.provider_charge_id,
#     payment_name=row.payment_name,
#     payment_phone=row.payment_phone,
#     payment_email=row.payment_email,
#     order_id=row.order_id
# )
    # Add the record to the database
    session.add(rec)    
session.commit()

#Product
# rec = db.Product(name=row.name, description=row.description, price=row.price, image=row.image, sub_category_id=row.sub_category_id, category_id=row.category_id, deleted=row.deleted)

    # rec = db.Variation(id=row.id, name=row.name, description=row.description, price=row.price,
    #                             image=row.image,
    #                              category_id=row.category_id,
    #                              sub_category_id=row.sub_category_id,
    #                              deleted=row.deleted)
    
    