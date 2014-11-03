from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy import PrimaryKeyConstraint
import os


engine = create_engine(os.environ["APP_DATABASE_URL"], convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String())
    clicks = db.Column(db.Integer)
    buys = db.Column(db.Integer)
    cart_adds = db.Column(db.Integer)
    glances = db.Column(db.Integer)

    def __init__(self, sku, clicks, buys, cart_adds, glances):
        self.sku = sku
        self.clicks = clicks
        self.buys = buys
        self.cart_adds = cart_adds
        self.glances = glances

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Order(Base):
    __table__ = Base.metadata.tables['orders']
    #line_items = relationship("LineItem", backref="order")


class LineItem(Base):
    __table__ = Base.metadata.tables['line_items']
    #parent_id = Column(Integer, ForeignKey('orders.id'))
    #variants = relationship("Variant", backref="line_item")


class Variant(Base):
    __table__ = Base.metadata.tables['variants']
    #option_values = relationship("OptionValue", backref="variant")


class OptionValue(Base):
    __table__ = Base.metadata.tables['option_values']


class OptionValueVariant(Base):
    __table__ = Base.metadata.tables['option_values_variants']
    __mapper_args__ = {
        'primary_key':[Base.metadata.tables['option_values_variants'].c.variant_id, Base.metadata.tables['option_values_variants'].c.option_value_id]
    }
    #__table_args__ = {PrimaryKeyConstraint:("variant_id", "option_value_id")}
    #__table_args__ = {'autoload':True, "primary_key":("variant_id", "option_value_id")}