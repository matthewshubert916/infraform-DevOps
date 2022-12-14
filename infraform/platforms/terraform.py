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

from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Terraform(Platform):

    NAME = PACKAGE = BINARY = 'terraform'
    readiness_check = ["terraform -v"]
    pre_commands = ['terraform init']
    run_commands = ["terraform apply"]
    post_commands = []
    installation_commands = [
        "wget https://releases.hashico\
rp.com/terraform/1.0.8/terraform_1.0.8_linux_amd64.zip",
        "unzip terraform_1.0.8_linux_amd64.zip",
        "sudo mv terraform /usr/local/bin/"
    ]

    def __init__(self, scenario):
        self.binary = self.BINARY
        self.package = self.PACKAGE
        self.scenario = scenario
        super(Terraform, self).__init__(scenario)
