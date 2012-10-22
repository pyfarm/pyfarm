# No shebang line, this module is meant to be imported
#
# This file is part of PyFarm.
# Copyright (C) 2008-2012 Oliver Palmer
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

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, Integer

from pyfarm.db.tables import Base
from pyfarm.datatypes.enums import ACTIVE_HOSTS_FRAME_STATES


class Host(Base):
    '''base host definition'''
    __tablename__ = "pyfarm_hosts"
    repr_attrs = ("id", "hostname")

    # column definitions
    hostname = Column(String(255), nullable=False, unique=True)

    # relational definitions
    software = relationship('Software', uselist=True, backref="ref_software")
    groups = relationship('Group', uselist=True, backref="ref_groups")
    running_frames = relationship(
        'Frame',
        primaryjoin='(Frame.hostid == Host.id) & '
                    '(Frame.state.in_(%s))' % (ACTIVE_HOSTS_FRAME_STATES, )
    )

    def __init__(self, hostname):
        self.hostname = hostname
    # end __init__
# end Host


class Software(Base):
    '''stores information about what software a host can run'''
    __tablename__ = "pyfarm_host_software"
    repr_attrs = ("host", "name")

    # column definitions
    host = Column(Integer, ForeignKey(Host.id))
    name = Column(String(128), nullable=False)
    hosts = relationship('Host', uselist=True, backref="ref_hosts")

    def __init__(self, host, name):
        self.host = host
        self.name = name
    # end __init__
# end Software


class Group(Base):
    '''stores information about which group or groups a host belongs to'''
    __tablename__ = "pyfarm_host_group"
    repr_attrs = ("host", "name")

    # column definitions
    host = Column(Integer, ForeignKey("pyfarm_hosts.id"), nullable=False)
    name = Column(String(128), nullable=False)

    # relationship setup
    hosts = relationship('Host', uselist=True, backref=__tablename__)

    def __init__(self, host, name):
        self.host = host
        self.name = name
    # end __init__
# end Group