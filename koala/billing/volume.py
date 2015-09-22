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
from koala.common import exception
from koala.openstack.common.gettextutils import _
from koala.openstack.common import jsonutils

VOLUME_EVENT_TYPES = ('create', 'delete', 'resize', 'exists')


class Volume(base.Resource):
    """Volume billing resource."""
    # NOTE(fandeliang) How to implement to support multi volumes, such as both
    # ssd and sata.

    def __init__(self, value):
        super(Volume, self).__init__(value)

        self.size = self.content.get('size', None)
        self.check_event_type()
        self.check_content()

    def check_event_type(self):
        if self.event_type not in VOLUME_EVENT_TYPES:
            msg = _("Volume event type must be in %s") % str(VOLUME_EVENT_TYPES)
            raise exception.EventTypeInvalid(msg)

    def check_content(self):
        self.size = self.content.get('size', None)

        if self.size is None:
            msg = _("Volume size not specified in the content.")
            raise exception.VolumeContentInvalid(msg)

        if self.size < 1:
            msg = _("Volume size must be positive integer.")
            raise exception.VolumeSizeInvalid(msg)

    def billing_resource(self):
        """Billing resource

           This is the mainly function for billing a resource. When the new
           event comes, we check whether the resource is a new or not. If
           it's a new resource, we need to generate a resource corresponding,
           otherwise, we just to calculate the consumption and update the
           billing records.
        """
        if self.get_resource():
            self.calculate_consumption()
        else:
            # NOTE(fandeliang) we still need to check the event type. if the
            # event type is not create, it means that some messages ahead
            # have lost.
            if self.event_type == 'create':
                self.create_resource()
            elif self.event_type == 'delete':
                # If we recieve a delete event with not resource records, just
                # ignore it.
                # TBD(fandeliang) Log.warning(_("Messaging missing"))
                pass
            else:
                # If we recieve a resize or exists event, create the new
                # resource and treat it as the create time.
                # TBD(fandeliang) Log.warning(_("Messaging missing"))
                self.create_resource()

    def calculate_consumption(self):
        """Calculate the consumption by deta time and price."""
        resource = self.get_resource()
        unit_price = self.get_price()
        start_at = self.get_start_at()
        deta_time = (self.event_time - start_at).seconds / 3600.0
        record_description = self.resource_type + ' ' + self.event_type
        record = {}
        updated_resource = {}

        if self.event_type == 'create':
            msg = _("Duplicate event.")
            raise exception.EventDuplicate(msg)

        elif self.event_type == 'resize':
            # We get the previous size information from the resource content
            # for a resize event.
            pre_content = jsonutils.loads(resource.content)
            pre_size = pre_content.get('size', 0)
            consumption = unit_price * deta_time * self.size
            updated_resource['updated_at'] = self.event_time
            updated_resource['content'] = jsonutils.dumps(self.content)

        elif self.event_type == 'exists':
            consumption = unit_price * deta_time * self.size
            record_description = "Audit billing"

        elif self.event_type == 'delete':
            consumption = unit_price * deta_time * self.size
            updated_resource['deleted'] = 1
            updated_resource['deleted_at'] = self.event_time
            updated_resource['status'] = 'delete'
            updated_resource['description'] = "Resource has been deleted"

        # Format record information and store it to database.
        record['resource_id'] = self.resource_id
        record['start_at'] = start_at
        record['end_at'] = self.event_time
        record['unit_price'] = unit_price
        record['consumption'] = consumption
        record['description'] = record_description
        self.create_record(record)

        # Format resource information and update it to database.
        updated_resource['consumption'] = resource.consumption + consumption
        self.update_resource(updated_resource)