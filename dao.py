import database as db


def get_products(session, category = None, sub_category = None):
    if category:
        products = session.query(db.Product).filter_by(category=category, deleted=False).all()
    elif sub_category:
        products = session.query(db.Product).filter_by(sub_category=sub_category, deleted=False).all()
    else:
        products = session.query(db.Product).filter_by(deleted=False).all()
    
    return products