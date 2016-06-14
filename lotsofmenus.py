from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Category, Item
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#Items for Eyes
category1 = Category(name = "Eyes")

session.add(category1)
session.commit()

item1 = Item(name = "roller lash mascara", description = "A mascara inspired by hair rollers", 
            category_id = category1.id)

session.add(item1)
session.commit()

item2 = Item(name = "Smudge Stick Waterproof Eye Liner", description = "Our bestselling Smudge Sticks are available in an array of matte and shimmer formulas",
             category_id = category1.id)

session.add(item2)
session.commit()

item3 = Item(name = "Naked Eye Color Palette", description = "brown and dark brown",
            category_id = category1.id)

session.add(item3)
session.commit()

item4 = Item(name = "Eye Cream", description = "This Eye cream provides concentrated hydration for a radiantly refreshed complexion. Our exclusive tri-radiance complex helps develop the skin's water reserves and reinforces the moisture barrier. Contains mango butter, a natural plant-based emollient known to provide moisture.",
          category_id = category1.id)

session.add(item4)
session.commit()


#Items for Lips
category2 = Category(name = "Lips")

session.add(category2)
session.commit()

item1 = Item(name = "Fresh Sugar Lip Treatment Sunscreen SPF 15", description = "A bestselling lip treatment and a cult favorite among all who try it, including Hollywoods elite that moisturizes, protects, and smooths the lips.",
              category_id = category2.id)

session.add(item1)
session.commit()

item2 = Item(name = "Smashbox Always On Matte Liquid Lipstick", description = "An eight-hour wear, liquid-matte lipstick with a featherweight, comfortable formula that stays put and keeps color looking as fresh and flawless as the first swipe. ",
              category_id = category2.id)

session.add(item2)
session.commit()

item3 = Item(name = "Dior Dior Addict Lip Glow", description = "A sheer balm that enhances your natural lip color while moisturizing and protecting lips. ", 
            category_id = category2.id)

session.add(item3)
session.commit()

item4 = Item(name = "Bite Beauty Amuse Bouche Lipstick", description = "A collection of high-impact lipsticks in dimensional shades that have been handcrafted to deliver extreme moisture, soft texture, and creamy wear. ", 
             category_id = category2.id)

session.add(item4)
session.commit()

print "added menu items!"
