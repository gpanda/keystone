# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack Foundation
# Copyright 2012 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uuid

import six

from keystone.common import controller
from keystone.common import dependency
from keystone import exception


INTERFACES = ['public', 'internal', 'admin']


@dependency.requires('catalog_api')
class Service(controller.V2Controller):

    @controller.v2_deprecated
    def get_services(self, context):
        self.assert_admin(context)
        service_list = self.catalog_api.list_services()
        return {'OS-KSADM:services': service_list}

    @controller.v2_deprecated
    def get_service(self, context, service_id):
        self.assert_admin(context)
        service_ref = self.catalog_api.get_service(service_id)
        return {'OS-KSADM:service': service_ref}

    @controller.v2_deprecated
    def delete_service(self, context, service_id):
        self.assert_admin(context)
        self.catalog_api.delete_service(service_id)

    @controller.v2_deprecated
    def create_service(self, context, OS_KSADM_service):
        self.assert_admin(context)
        service_id = uuid.uuid4().hex
        service_ref = OS_KSADM_service.copy()
        service_ref['id'] = service_id
        new_service_ref = self.catalog_api.create_service(
            service_id, service_ref)
        return {'OS-KSADM:service': new_service_ref}


@dependency.requires('catalog_api')
class Endpoint(controller.V2Controller):

    @controller.v2_deprecated
    def get_endpoints(self, context):
        """Merge matching v3 endpoint refs into legacy refs."""
        self.assert_admin(context)
        legacy_endpoints = {}
        for endpoint in self.catalog_api.list_endpoints():
            if not endpoint.get('legacy_endpoint_id'):
                # endpoints created in v3 should not appear on the v2 API
                continue

            # is this is a legacy endpoint we haven't indexed yet?
            if endpoint['legacy_endpoint_id'] not in legacy_endpoints:
                legacy_ep = endpoint.copy()
                legacy_ep['id'] = legacy_ep.pop('legacy_endpoint_id')
                legacy_ep.pop('interface')
                legacy_ep.pop('url')

                legacy_endpoints[endpoint['legacy_endpoint_id']] = legacy_ep
            else:
                legacy_ep = legacy_endpoints[endpoint['legacy_endpoint_id']]

            # add the legacy endpoint with an interface url
            legacy_ep['%surl' % endpoint['interface']] = endpoint['url']
        return {'endpoints': legacy_endpoints.values()}

    @controller.v2_deprecated
    def create_endpoint(self, context, endpoint):
        """Create three v3 endpoint refs based on a legacy ref."""
        self.assert_admin(context)

        # according to the v2 spec publicurl is mandatory
        self._require_attribute(endpoint, 'publicurl')
        # service_id is necessary
        self._require_attribute(endpoint, 'service_id')

        legacy_endpoint_ref = endpoint.copy()

        urls = {}
        for i in INTERFACES:
            # remove all urls so they aren't persisted them more than once
            url = '%surl' % i
            if endpoint.get(url):
                # valid urls need to be persisted
                urls[i] = endpoint.pop(url)
            elif url in endpoint:
                # null or empty urls can be discarded
                endpoint.pop(url)
                legacy_endpoint_ref.pop(url)

        legacy_endpoint_id = uuid.uuid4().hex
        for interface, url in six.iteritems(urls):
            endpoint_ref = endpoint.copy()
            endpoint_ref['id'] = uuid.uuid4().hex
            endpoint_ref['legacy_endpoint_id'] = legacy_endpoint_id
            endpoint_ref['interface'] = interface
            endpoint_ref['url'] = url

            self.catalog_api.create_endpoint(endpoint_ref['id'], endpoint_ref)

        legacy_endpoint_ref['id'] = legacy_endpoint_id
        return {'endpoint': legacy_endpoint_ref}

    @controller.v2_deprecated
    def delete_endpoint(self, context, endpoint_id):
        """Delete up to three v3 endpoint refs based on a legacy ref ID."""
        self.assert_admin(context)

        deleted_at_least_one = False
        for endpoint in self.catalog_api.list_endpoints():
            if endpoint['legacy_endpoint_id'] == endpoint_id:
                self.catalog_api.delete_endpoint(endpoint['id'])
                deleted_at_least_one = True

        if not deleted_at_least_one:
            raise exception.EndpointNotFound(endpoint_id=endpoint_id)


@dependency.requires('catalog_api')
class RegionV3(controller.V3Controller):
    collection_name = 'regions'
    member_name = 'region'

    def __init__(self):
        super(RegionV3, self).__init__()
        self.get_member_from_driver = self.catalog_api.get_region

    @controller.protected()
    def create_region(self, context, region):
        ref = self._assign_unique_id(self._normalize_dict(region))

        ref = self.catalog_api.create_region(ref['id'], ref)
        return RegionV3.wrap_member(context, ref)

    def list_regions(self, context):
        refs = self.catalog_api.list_regions()
        return RegionV3.wrap_collection(context, refs)

    @controller.protected()
    def get_region(self, context, region_id):
        ref = self.catalog_api.get_region(region_id)
        return RegionV3.wrap_member(context, ref)

    @controller.protected()
    def update_region(self, context, region_id, region):
        self._require_matching_id(region_id, region)

        ref = self.catalog_api.update_region(region_id, region)
        return RegionV3.wrap_member(context, ref)

    @controller.protected()
    def delete_region(self, context, region_id):
        return self.catalog_api.delete_region(region_id)


@dependency.requires('catalog_api')
class ServiceV3(controller.V3Controller):
    collection_name = 'services'
    member_name = 'service'

    def __init__(self):
        super(ServiceV3, self).__init__()
        self.get_member_from_driver = self.catalog_api.get_service

    @controller.protected()
    def create_service(self, context, service):
        ref = self._assign_unique_id(self._normalize_dict(service))
        self._require_attribute(ref, 'type')

        ref = self.catalog_api.create_service(ref['id'], ref)
        return ServiceV3.wrap_member(context, ref)

    @controller.filterprotected('type')
    def list_services(self, context, filters):
        hints = ServiceV3.build_driver_hints(context, filters)
        refs = self.catalog_api.list_services(hints=hints)
        return ServiceV3.wrap_collection(context, refs, hints=hints)

    @controller.protected()
    def get_service(self, context, service_id):
        ref = self.catalog_api.get_service(service_id)
        return ServiceV3.wrap_member(context, ref)

    @controller.protected()
    def update_service(self, context, service_id, service):
        self._require_matching_id(service_id, service)

        ref = self.catalog_api.update_service(service_id, service)
        return ServiceV3.wrap_member(context, ref)

    @controller.protected()
    def delete_service(self, context, service_id):
        return self.catalog_api.delete_service(service_id)


@dependency.requires('catalog_api')
class EndpointV3(controller.V3Controller):
    collection_name = 'endpoints'
    member_name = 'endpoint'

    def __init__(self):
        super(EndpointV3, self).__init__()
        self.get_member_from_driver = self.catalog_api.get_endpoint

    @classmethod
    def filter_endpoint(cls, ref):
        if 'legacy_endpoint_id' in ref:
            ref.pop('legacy_endpoint_id')
        return ref

    @classmethod
    def wrap_member(cls, context, ref):
        ref = cls.filter_endpoint(ref)
        return super(EndpointV3, cls).wrap_member(context, ref)

    @controller.protected()
    def create_endpoint(self, context, endpoint):
        ref = self._assign_unique_id(self._normalize_dict(endpoint))
        self._require_attribute(ref, 'service_id')
        self._require_attribute(ref, 'interface')
        self.catalog_api.get_service(ref['service_id'])

        ref = self.catalog_api.create_endpoint(ref['id'], ref)
        return EndpointV3.wrap_member(context, ref)

    @controller.filterprotected('interface', 'service_id')
    def list_endpoints(self, context, filters):
        hints = EndpointV3.build_driver_hints(context, filters)
        refs = self.catalog_api.list_endpoints(hints=hints)
        return EndpointV3.wrap_collection(context, refs, hints=hints)

    @controller.protected()
    def get_endpoint(self, context, endpoint_id):
        ref = self.catalog_api.get_endpoint(endpoint_id)
        return EndpointV3.wrap_member(context, ref)

    @controller.protected()
    def update_endpoint(self, context, endpoint_id, endpoint):
        self._require_matching_id(endpoint_id, endpoint)

        if 'service_id' in endpoint:
            self.catalog_api.get_service(endpoint['service_id'])

        ref = self.catalog_api.update_endpoint(endpoint_id, endpoint)
        return EndpointV3.wrap_member(context, ref)

    @controller.protected()
    def delete_endpoint(self, context, endpoint_id):
        return self.catalog_api.delete_endpoint(endpoint_id)
