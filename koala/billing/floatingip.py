# Copyright 2015 vanderliang@gmail.com.
# All Rights Reserved.
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

from koala.billing import base
from koala.openstack.common.gettextutils import _


class FloatingIP(base.Resource):
    def __init__(self, value):
        super(FloatingIP, self).__init__(value)
        msg = _("Floating IP billing system has not been implemented.")
        raise NotImplementedError(msg)
