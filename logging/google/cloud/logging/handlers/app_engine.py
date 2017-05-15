# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logging handler for App Engine Flexible

Send logs to Stackdriver Logging API.
"""

import os

from google.cloud.logging.handlers.handlers import CloudLoggingHandler
from google.cloud.logging.handlers.handlers import EXCLUDED_LOGGER_DEFAULTS
from google.cloud.logging.handlers.transports import BackgroundThreadTransport
from google.cloud.logging.resource import Resource

GAE_PROJECT_ENV = 'GCLOUD_PROJECT'

DEFAULT_LOGGER_NAME = 'projects/{}/logs/app'.format(os.environ.get(GAE_PROJECT_ENV))

GAE_RESOURCE = Resource(
    type='gae_app',
    labels={
        'project_id': os.environ.get(GAE_PROJECT_ENV),
        'module_id': os.environ.get('GAE_SERVICE'),
        'version_id': os.environ.get('GAE_VERSION'),
    },
)


class AppEngineHandler(CloudLoggingHandler):
    """A handler that directly makes Stackdriver logging API calls.

    This handler can be used to route Python standard logging messages directly
    to the Stackdriver Logging API.

    This handler supports both an asynchronous and synchronous transport.

    :type client: :class:`google.cloud.logging.client`
    :param client: the authenticated Google Cloud Logging client for this
                   handler to use

    :type name: str
    :param name: the name of the custom log in Stackdriver Logging. Defaults
                 to 'python'. The name of the Python logger will be represented
                 in the ``python_logger`` field.

    :type transport: type
    :param transport: Class for creating new transport objects. It should
                      extend from the base :class:`.Transport` type and
                      implement :meth`.Transport.send`. Defaults to
                      :class:`.BackgroundThreadTransport`. The other
                      option is :class:`.SyncTransport`.

    :type resource: :class:`~google.cloud.logging.resource.Resource`
    :param resource: Monitored resource of the entry, defaults
                     to the global resource type.
    """

    def __init__(self, client,
                 name=EXCLUDED_LOGGER_DEFAULTS,
                 transport=BackgroundThreadTransport):
        super(AppEngineHandler, self).__init__(client, name, transport, resource=GAE_RESOURCE)
