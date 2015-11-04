# Copyright 2015 vanderliang@gmail.com
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

from koala.tests.api import base
from koala.tests.db import utils


class TestRouterEvent(base.FunctionalTest):

    def setUp(self):
        super(TestRouterEvent, self).setUp()
        self.create_router_price()

    def tearDown(self):
        super(TestRouterEvent, self).tearDown()

    def create_router_price(self):
        self.post_json('/prices', utils.get_router_price()).json

    def test_post_create_event_success(self):
        router_event = utils.get_router_event()
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + router_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_exists_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + router_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_delete_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_type'] = 'delete'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        self.get_json(url, expect_errors=True)

        url = '/records/' + router_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_create_delete_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', router_event)

        router_event['event_time'] = '2015-10-11T01:00:00.000000'
        router_event['event_type'] = 'delete'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 240)

        url = '/records/' + router_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 240)

    def test_create_exists_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', router_event)

        router_event['event_time'] = '2015-10-11T01:00:00.000000'
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 240)

        url = '/records/' + router_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 240)

    def test_exists_delete_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_type'] = 'exists'
        router_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', router_event)

        router_event['event_time'] = '2015-10-11T01:00:00.000000'
        router_event['event_type'] = 'delete'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 240)

        url = '/records/' + router_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 240)

    def test_exists_exists_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_type'] = 'exists'
        router_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', router_event)

        router_event['event_time'] = '2015-10-11T01:00:00.000000'
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 240)

        url = '/records/' + router_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 240)

    def test_create_exists_delete_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', router_event)

        router_event['event_time'] = '2015-10-11T01:00:00.000000'
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 240)

        router_event['event_time'] = '2015-10-21T01:00:00.000000'
        router_event['event_type'] = 'delete'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 480)

        url = '/records/' + router_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 240)
        self.assertEqual(int(records[1]['consumption']), 240)

    def test_exists_exists_delete_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_time'] = '2015-10-01T01:00:00.000000'
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event)

        router_event['event_time'] = '2015-10-11T01:00:00.000000'
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 240)

        router_event['event_time'] = '2015-10-21T01:00:00.000000'
        router_event['event_type'] = 'delete'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 480)

        url = '/records/' + router_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)

    def test_create_delete_exists_event_success(self):
        router_event = utils.get_router_event()
        router_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', router_event)

        router_event['event_time'] = '2015-10-11T01:00:00.000000'
        router_event['event_type'] = 'delete'
        self.post_json('/events', router_event)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 240)

        router_event['event_time'] = '2015-10-21T01:00:00.000000'
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event, expect_errors=True)

        url = '/resources/' + router_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 240)

        url = '/records/' + router_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

    def test_without_resource_id(self):
        router_event = utils.get_router_event()
        router_event.pop('resource_id')
        self.post_json('/events', router_event, expect_errors=True)

    def test_without_content(self):
        router_event = utils.get_router_event()
        router_event.pop('content')
        self.post_json('/events', router_event, expect_errors=True)

    def test_with_wrong_content(self):
        router_event = utils.get_router_event()
        router_event['content'] = 'wrong_content'
        self.post_json('/events', router_event, expect_errors=True)

    def test_with_wrong_event_type(self):
        router_event = utils.get_router_event()
        router_event['event_type'] = 'resize'
        self.post_json('/events', router_event, expect_errors=True)

    def test_with_wrong_event_time(self):
        router_event = utils.get_router_event()
        router_event['event_time'] = '2015-10-21T01:00:00.000000'
        self.post_json('/events', router_event)

        router_event = utils.get_router_event()
        router_event['event_time'] = '2015-09-21T01:00:00.000000'
        router_event['event_type'] = 'exists'
        self.post_json('/events', router_event, expect_errors=True)
