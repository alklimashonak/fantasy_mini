from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.database import Base


association_table = Table('association', Base.metadata,
                          Column('team_id', ForeignKey('team.id'), primary_key=True),
                          Column('driver_id', ForeignKey('driver.id'), primary_key=True)
                          )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(24), nullable=False, index=True)
    email = Column(String(48), nullable=True)
    password = Column(String(24), nullable=False)

    teams = relationship('Team', back_populates='owner')


class Driver(Base):
    __tablename__ = 'driver'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(24), nullable=False, index=True)
    last_name = Column(String(24), nullable=False, index=True)
    number = Column(Integer, nullable=False)

    teams = relationship('Team', secondary=association_table, back_populates='drivers')


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(48), nullable=False, index=True)

    owner_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship('User', back_populates='teams')
    drivers = relationship('Driver', secondary=association_table, back_populates='teams')
