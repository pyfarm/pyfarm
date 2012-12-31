# No shebang line, this module is meant to be imported
#
# This file is part of PyFarm.
# Copyright (C) 2008-2013 Oliver Palmer
#
# PyFarm is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyFarm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PyFarm.  If not, see <http://www.gnu.org/licenses/>.

'''
storage class for frame-to-frame, frame-job and job-job
dependencies
'''

from sqlalchemy import Column, ForeignKey, select
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship

from pyfarm.db.tables import Base
from pyfarm.db.tables._constants import TABLE_F2_DEPENDENCIES, \
    TABLE_J2J_DEPENDENCIES, TABLE_FRAME, TABLE_JOB

__all__ = ['F2FDependency', 'J2JDependency']

class Dependency(object):
    @classmethod
    def children(cls, parentid, session):
        '''returns a list of child id objects for the given dependency'''
        ids = []

        # get the immediate children of the provided parent and
        # use this to populate the initial parent ids
        select_statement = select(
            columns=[cls._child],
            whereclause=cls._parent == parentid,
            distinct=True
        )
        query_ids = list(
            entry[0]
            for entry in session.query(select_statement)
        )

        # while we have ids to query pop an item
        # off of the list and
        while query_ids:
            query_id = query_ids.pop()
            if query_id != parentid and query_id not in ids:
                ids.append(query_id)

                # select all rows that
                select_statement = select(
                    columns=[cls._child],
                    whereclause=cls._parent == query_id,
                    distinct=True
                )
                child_ids = list(
                    entry[0]
                    for entry in session.query(select_statement)
                )
                query_ids.extend(child_ids)

        return ids
    # end select_children

    @classmethod
    def ids(cls, session=None):
        from sqlalchemy.orm import object_session
        object_session(cls)
#        from pyfarm.db.engine import engine
#        Session = sessionmaker(bind=engine)
#        session = Session()
#        print id(session)
    # end ids
# end Dependency


class F2FDependency(Base):
    '''defines frame to frame dependencies'''
    __tablename__ = TABLE_F2_DEPENDENCIES
    repr_attrs = ("_parent", "_child")

    # column definitions
    _parent = Column(Integer, ForeignKey('%s.id' % TABLE_FRAME))
    _child = Column(Integer, ForeignKey('%s.id' % TABLE_FRAME))

    # relationship definitions
    parent = relationship(
        'Frame',
        primaryjoin='(Frame.id == F2FDependency._parent)',
        backref='ref_dependencyf2f_parent'
    )
    child = relationship(
        'Frame',
        primaryjoin='(Frame.id == F2FDependency._child)',
        backref='ref_dependencyf2f_child'
    )

    def __init__(self, parent, child):
        self._parent = parent.id if hasattr(parent, 'id') else parent
        self._child = child.id if hasattr(child, 'id') else child

        if self._parent == self._child:
            raise ValueError("a frame cannot be dependent on itself")
    # end __init__
# end F2FDependency


class J2JDependency(Base, Dependency):
    '''defines job to job dependencies'''
    __tablename__ = TABLE_J2J_DEPENDENCIES
    repr_attrs = ("_parent", "_child")

    # column definitions
    _parent = Column(Integer, ForeignKey('%s.id' % TABLE_JOB))
    _child = Column(Integer, ForeignKey('%s.id' % TABLE_JOB))

    # relationship definitions
    parent = relationship(
        'Job',
        primaryjoin='(Job.id == J2JDependency._parent)',
        backref='ref_dependencyj2j_parent'
    )
    child = relationship(
        'Job',
        primaryjoin='(Job.id == J2JDependency._child)',
        backref='ref_dependencyj2j_child'
    )

    def __init__(self, parent, child):
        self._parent = parent.id if hasattr(parent, 'id') else parent
        self._child = child.id if hasattr(child, 'id') else child

        if self._parent == self._child:
            raise ValueError("a job cannot be dependent on itself")
    # end __init__
# end J2JDependency

if __name__ == '__main__':
    pass