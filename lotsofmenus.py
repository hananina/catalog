from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Shop, Base, Item
 
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


#Items for Benefit
shop1 = Shop(name = "Benefit")

session.add(shop1)
session.commit()

item1 = Item(name = "roller lash curling mascara", description = "It is a roller for lashes! The eye-opening Hook n Roll brush grabs, separates, lifts and curls... while the instant curve-setting formula holds for 12 hours. Contains provitamin B5 and serin.", category = "eyes", shop_id = "shop1")

session.add(item1)
session.commit()

item2 = Item(name = "posiebalm", description = "posiebalm conditions & hydrates with mango butter and sodium hyaluronate. This kiss of sheer color gives you the prettiest lips.",
             category = "lips", shop = shop1)

session.add(item2)
session.commit()

item3 = Item(name = "the POREfessional face primer", description = "Quickly minimize the appearance of pores & fine lines for smoother-than-smooth skin! Apply this silky, lightweight balm alone, under or over makeup. The translucent formula contains a vitamin E derivative known to protect skin from free radicals.",
             category = "face", shop = shop1)

session.add(item3)
session.commit()

item4 = Item(name = "total moisture facial cream", description = "This facial cream provides concentrated hydration for a radiantly refreshed complexion. Our exclusive tri-radiance complex helps develop the skin's water reserves and reinforces the moisture barrier. Contains mango butter, a natural plant-based emollient known to provide moisture.",
           category = "skincare", shop = shop1)

session.add(item4)
session.commit()


#Items for Stila
shop2 = Shop(name = "Stila")

session.add(shop1)
session.commit()

item1 = Item(name = "Smudge Stick Waterproof Eye Liner", description = "Our bestselling Smudge Sticks are available in an array of matte and shimmer formulas",
             category = "eyes", shop = shop2)

session.add(item1)
session.commit()

item2 = Item(name = "Convertible Color", description = "Our ingenious two in one lipstick and blush is loaded with creamy",
             category = "lips", shop = shop2)

session.add(item2)
session.commit()

item3 = Item(name = "Correct & Perfect All-in-One Color Correcting Palette", description = "Create Complexion Perfection! Under-eye circles, redness, uneven or dull skin?  Not anymore with this all-in-one customizable color correcting palette.  Five velvety smooth cream color correctors and two tinted setting powders are all you need to help neutralize imperfections and brighten dull skin tones.  ", 
            category = "face", shop = shop2)

session.add(item3)
session.commit()

item4 = Item(name = "Shape & Shade Custom Contour Duo", description = "This ultra-creamy, super-soft contour and high-light duo, uniquely, in three shades, is the perfect contouring solution for all skin tones. ", 
            category = "face", shop = shop2)

session.add(item4)
session.commit()

print "added menu items!"
