# Copyright 2019 Arie Bregman
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
import logging

from infraform.platforms.platform import Platform
from infraform.platforms.vars import docker_compose as dc_vars

LOG = logging.getLogger(__name__)


class Docker_compose(Platform):

    def __init__(self, args):

        super(Docker_compose, self).__init__(
            args, binary=dc_vars.BINARY,
            readiness_check=dc_vars.READINESS_CHECK,
            installation=dc_vars.INSTALLATION,
            name=dc_vars.NAME, run=dc_vars.RUN, rm=dc_vars.REMOVE)
