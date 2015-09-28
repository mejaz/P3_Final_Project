from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Usernames, Catagory, Items

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# username1 = session.query(Usernames).filter_by(user_id='mejaz', user_pic='yet to come', user_password='hello').one()
# # session.add(username1)
# # session.commit()

# username2 = session.query(Usernames).filter_by(user_id='siddiq', user_pic='yet to come', user_password='hello').one()
# # session.add(username2)
# # session.commit()

catagory1 = Catagory(catagory_name='Soccer')
session.add(catagory1)
session.commit()

# item1 = Items(item_name="Jersey", item_desc="Custom made available.", catagory=catagory1, usernames=username1)
# session.add(item1)
# session.commit()

# item1 = Items(item_name="FootBall", item_desc="Custom made available.", catagory=catagory1, usernames=username1)
# session.add(item1)
# session.commit()

catagory2 = Catagory(catagory_name='Baseketball')
session.add(catagory2)
session.commit()

# item2 = Items(item_name="Basketball Shoes", item_desc="Custom made available.", catagory=catagory2, usernames=username1)
# session.add(item2)
# session.commit()

# item2 = Items(item_name="Basketball Net", item_desc="Custom made available.", catagory=catagory2, usernames=username1)
# session.add(item2)
# session.commit()

catagory3 = Catagory(catagory_name='Baseball')
session.add(catagory3)
session.commit()

# item3 = Items(item_name="Bat", item_desc="Custom made available.", catagory=catagory3, usernames=username1)
# session.add(item3)
# session.commit()

catagory4 = Catagory(catagory_name='Frisbee')
session.add(catagory4)
session.commit()

# item4 = Items(item_name="Frisbee", item_desc="Custom made available.", catagory=catagory4, usernames=username2)
# session.add(item4)
# session.commit()

catagory5 = Catagory(catagory_name='Snowboarding')
session.add(catagory5)
session.commit()

# item5 = Items(item_name="Goggles", item_desc="Custom made available.", catagory=catagory5, usernames=username2)
# session.add(item5)
# session.commit()

catagory6 = Catagory(catagory_name='Rock Climbing')
session.add(catagory6)
session.commit()

# item6 = Items(item_name="Helmet", item_desc="Custom made available.", catagory=catagory6, usernames=username2)
# session.add(item6)
# session.commit()

catagory7 = Catagory(catagory_name='Foosball')
session.add(catagory7)
session.commit()

# item7 = Items(item_name="Fooball Table", item_desc="Custom made available.", catagory=catagory7, usernames=username2)
# session.add(item7)
# session.commit()

# item7 = Items(item_name="Foosball Racket", item_desc="Custom made available.", catagory=catagory7, usernames=username2)
# session.add(item7)
# session.commit()

catagory8 = Catagory(catagory_name='Skating')
session.add(catagory8)
session.commit()

# item8 = Items(item_name="Skates", item_desc="Custom made available.", catagory=catagory8, usernames=username2)
# session.add(item8)
# session.commit()

# item8 = Items(item_name="Helmet", item_desc="Custom made available.", catagory=catagory8, usernames=username2)
# session.add(item8)
# session.commit()


catagory9 = Catagory(catagory_name='Hockey')
session.add(catagory9)
session.commit()

# item9 = Items(item_name="Stick", item_desc="Custom made available.", catagory=catagory9, usernames=username1)
# session.add(item9)
# session.commit()