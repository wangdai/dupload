
def get_items(session, offset, limit, cat=None):
    if cat is None:
        return session.query(Item)
                .order_by(desc(Item.lastmodified))[offset:offset+limit]
    else:
        return session.query(Item).filter_by(cat=cat)
                .order_by(desc(Item.lastmodified))[offset:offset+limit]
