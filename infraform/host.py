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
import crayons
import logging
import sys

from infraform.utils import process
from infraform.workspace import Workspace

LOG = logging.getLogger(__name__)


class Host(object):

    def __init__(self, address, workspace_dir=None,
                 scenario_fpath=None, platform_name=None):
        self.address = address
        if workspace_dir:
            self.workspace = Workspace(host=self.address,
                                       subdir=workspace_dir)

    def check_host_platform_readiness(self, platform):
        LOG.info("{}: {}".format(
            crayons.yellow("host platform check started"),
            crayons.cyan(self.address)))
        result = process.execute_cmd(
            commands=platform.readiness_check,
            host=self.address, hide_output=True, warn_on_fail=True)
        if result.return_code != 0:
            LOG.info("host platform check result: {}".format(
                crayons.red("FAILED")))
            if result.stderr:
                LOG.info("host: {} isn't ready.\nstderr: {}".format(
                    crayons.cyan(self.address), crayons.red(result.stderr)))
            try:
                LOG.info("Run the following on {}:\n{}".format(
                    crayons.cyan(self.address), crayons.yellow(
                        "\n".join(platform.installation_commands))))
            except AttributeError:
                LOG.info("I have no idea how to fix this...bye :'(")
                sys.exit(2)
            ans = input("Should I run it for you?[yY/Nn]: ")
            if ans.lower() == "y":
                LOG.info(
                    "Running installation commands on {}".format(
                        crayons.cyan(self.address)))
                process.execute_cmd(
                    commands=platform.installation_commands,
                    host=self.address)
            else:
                LOG.info("Goodbye")
                sys.exit(2)
        LOG.info(crayons.green("host verification result: PASSED"))
