# Copyright 2021 Arie Bregman
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

from infraform.platforms.container import Container


LOG = logging.getLogger(__name__)


class Podman(Container):

    NAME = PACKAGE = 'podman'
    BINARY = '/bin/podman'
    readiness_check = ["podman -v",
                       "systemctl status podman"]
    installation_commands = ["sudo dnf install -y podman",
                             "sudo systemctl start podman"]

    def __init__(self, scenario):
        super(Podman, self).__init__(scenario, self.BINARY, self.PACKAGE)
