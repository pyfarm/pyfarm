# No shebang line, this module is meant to be imported
#
# Copyright 2013 Oliver Palmer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyfarm.models import Agent, AgentTags, AgentSoftware
from pyfarm.admin.tables.core import CoreTableModelView


class AgentTagsModelView(CoreTableModelView):
    def __init__(self):
        super(AgentTagsModelView, self).__init__(AgentTags)


class AgentSoftwareModelView(CoreTableModelView):
    def __init__(self):
        super(AgentSoftwareModelView, self).__init__(AgentSoftware)


# TODO: editor widgets in view
# TODO: add action for batch edits
# TODO: if action + form (above) is not possible, create some 'general' actions
class AgentModelView(CoreTableModelView):
    # TODO: add form for creation that includes **tagging**
    # form = None
    def __init__(self):
        super(AgentModelView, self).__init__(Agent)