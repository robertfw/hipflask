from sqlalchemy import Column, Boolean, Integer, String, Sequence, relationship, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import sys

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    login = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean(), default=False)
    is_suspended = Column(Boolean(), default=False)

    def __repr__(self):
        return '<User %r>' % self.login

    # Flask-Login integration
    def is_authenticated(self):
        return self.id is not None

    def is_active(self):
        return not self.is_suspended

    def is_anonymous(self):
        return self.is_authenticated()

    def get_id(self):
        return self.id


class NodeType(Base):
    __tablename__ = 'nodetypes'

    id = Column(Integer, Sequence('nodetype_id_seq'), primary_key=True)
    name = Column(String(255), unique=True)
    nodes = relationship("Node", backref="type")

    @property
    def clazz(self):
        return getattr(sys.modules[__name__], self.name)


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, Sequence('node_id_seq'), primary_key=True)
    nodetype_id = Column(Integer, ForeignKey('nodetypes.id'))
    object_id = Column(Integer)

    incoming_edges = relationship("Edge", backref="to_nodes", primaryjoin="Node.id == Edge.to_id")
    outgoing_edges = relationship("Edge", backref="from_nodes", primaryjoin="Node.id == Edge.from_id")

    @property
    def object(self):
        return self.db.session.query(self.type.clazz).get(self.object_id)


class Edge(Base):
    __tablename__ = 'edges'

    id = Column(Integer, Sequence('edge_id_seq'), primary_key=True)
    from_id = Column(Integer, ForeignKey('nodes.id'))
    to_id = Column(Integer, ForeignKey('nodes.id'))
    edgetype_id = Column(Integer, ForeignKey('edgetypes.id'))


class EdgeType(Base):
    __tablename__ = 'edgetypes'

    id = Column(Integer, Sequence('edgetype_id_seq'), primary_key=True)
    name = Column(String(255), unique=True)
    edges = relationship("Edge", backref="type")
