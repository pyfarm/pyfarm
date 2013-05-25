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
from pyfarm.preferences import prefs
from pyfarm.cmdargs import *
from pyfarm.net.functions import openport

parser.description = "Entry point for PyFarm's master."

try:
    port = prefs.get('network.ports.master')

except KeyError:
    port = openport()

parser.set_defaults(port=port)

parser.add_argument(
    '--queue', default=True, type=tobool,
    help='enables or disables queue events'
)
parser.add_argument(
    '--assignment', default=True, type=tobool,
    help='enables or disables the assignment queue'
)