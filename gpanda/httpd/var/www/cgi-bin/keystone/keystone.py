# Copyright 2013 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# gpanda debug >>
from __future__ import print_function
# gpanda debug <<

import os

from keystone.server import wsgi as wsgi_server


name = os.path.basename(__file__)

import sys
print("gpanda debug >>", sys.stderr)
print(name, file=sys.stderr)
print(__file__, file=sys.stderr)
print("gpanda debug <<", sys.stderr)
# print(name, file=sys.stdout)
# print(__file__, file=sys.stdout)

# NOTE(ldbragst): 'application' is required in this context by WSGI spec.
# The following is a reference to Python Paste Deploy documentation
# http://pythonpaste.org/deploy/

# import pdb
# pdb.set_trace()
application = wsgi_server.initialize_application(name)


class Debugger:

    def __init__(self, object):
        self.__object = object

    def __call__(self, *args, **kwargs):
        import pdb
        import sys
        debugger = pdb.Pdb()
        debugger.use_rawinput = 0
        debugger.reset()
        sys.settrace(debugger.trace_dispatch)

        try:
            return self.__object(*args, **kwargs)
        finally:
            debugger.quitting = 1
            sys.settrace(None)

# from paste.exceptions.errormiddleware import ErrorMiddleware
# application = Debugger(application)
# application = ErrorMiddleware(application, debug=True)
