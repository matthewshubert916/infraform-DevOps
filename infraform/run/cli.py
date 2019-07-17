# Copyright 2019 Infuse Team
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
import importlib

from infraform.exceptions import usage

LOG = logging.getLogger(__name__)


def validate_input(args):
    """Verifies that enough data was passed in order to run successfully."""
    print(args)
    if not args.scenario and not (args.project and args.tester):
        LOG.error(usage.missing_required_args())


def main(args):
    validate_input(args)
    Platform = getattr(importlib.import_module(
        "infraform.platforms.{}".format(args.platform)),
        args.platform.capitalize())
    platform = Platform()
    platform.prepare()
    platform.run()