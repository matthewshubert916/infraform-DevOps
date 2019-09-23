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
import jinja2 as j2
import logging
import os
import re
import subprocess
import sys

from infraform.exceptions import usage
from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Container(Platform):

    PACKAGE = 'podman'
    BINARY = '/bin/podman'
    DOCKERFILE_TEMPLATE = (os.path.dirname(__file__) +
                           '/templates/Dockerfile.j2')

    def __init__(self, args, binary, package):
        self.binary = binary
        self.package = package
        super(Container, self).__init__(args)
        self.adjust_args()
        try:
            self.image = "{}-{}-{}".format(self.args['project'],
                                           self.args['tester'],
                                           self.args['release'])
        except KeyError as e:
            LOG.error(usage.missing_arg(e))
            LOG.error(usage.run_usage())
            sys.exit(2)

    def adjust_args(self):
        """Adjust args to allow comfortable and simple invocation."""
        if 'gerrit' in self.args:
            if not self.args['gerrit'].startswith('https://'):
                self.args['gerrit'] = 'https://' + self.args['gerrit'] + '/gerrit'
            else:
                self.args['gerrit'] = self.args['gerrit'] + '/gerrit'
        if 'git' in self.args:
            if not self.args['git'].startswith('https://'):
                self.args['git'] = 'https://' + self.args['git']
        self.args['local'] = os.path.exists(self.args['project'])
        self.args['project_name'] = os.path.basename(self.args['project'])
        self.args['project_path'] = os.path.expanduser(self.args['project'])

    def prepare(self):
        if self.image_not_exists():
            LOG.warning("Couldn't find image: {}. Switching to image building".format(self.image))
            dockerfile_path = self.write_dockerfile(self.generate_dockerfile())
            self.build_image(dockerfile_path)

    def run(self):
        # try:
        #    subprocess.run("{} run {}".format(self.binary, self.image),
        #                   shell=True)
        # except ConnectionError as exception:  # noqa
        #    LOG.error(exception)
        #    LOG.error(self.raise_service_down())
        pass

    def image_not_exists(self):
        """Returns true if image exists."""
        res = subprocess.run("{} inspect {}".format(self.binary, self.image),
                             shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL)
        return res.returncode

    def get_template(self, name):
        """Returns jinja2 Dockerfile template."""
        with open(name, 'r+') as open_f:
            template_content = open_f.read()
        return template_content

    def generate_dockerfile(self):
        j2_env = j2.Environment(loader=j2.FunctionLoader(
            self.get_template), trim_blocks=True, undefined=j2.StrictUndefined)
        template = j2_env.get_template(self.DOCKERFILE_TEMPLATE)
        try:
            rendered_file = template.render(args=self.args)
        except j2.exceptions.UndefinedError as e:
            missing_arg = re.findall(r"'([^']*)'", e.message)[1]
            if missing_arg == 'git':
                missing_arg = (
                    missing_arg + ' or provide a local path of the project')
            LOG.error(usage.missing_arg(missing_arg))
            LOG.error(usage.run_usage())
            sys.exit(2)
        return rendered_file

    def write_dockerfile(self, df_content, df_path="Dockerfile"):
        with open(df_path, 'w+') as f:
            f.write(df_content)
        return df_path

    def destroy(self):
        """Removes the container from the system."""
        res = subprocess.run("{} rm {}".format(self.binary,
                                               self.args['name']))
        if res.returncode != 0:
            sys.exit(2)
        return res

    def build_image(self, df_path):
        """Builds image given df path."""
        res = subprocess.run("{} build -f {} -t test {}".format(self.binary, df_path,
                                                                self.args['project_path']),
                             shell=True)
        print(res)
        if res.returncode != 0:
            sys.exit(2)
        return res
