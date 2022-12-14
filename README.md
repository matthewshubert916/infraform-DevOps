# InfraForm

[![Build Status](https://travis-ci.org/bregman-arie/infraform.svg?branch=master)](https://travis-ci.org/bregman-arie/infraform)

Unified interface for automation cross different technologies and platforms. Infraform allows you to:

* Run common built-in operations (aka scenarios) or write/provide your own and let Infraform handle the execution
* Use templated scenarios - one scenario, many ways to render it
* Execute scenarios locally or on remote host(s)
* Make use of different technologies to run the scenarios - Ansible, Python, Terraform, Podman, Docker, ...
* Adjusts the host accordingly it it isn't ready to run the chosen technology (Ansible, Terraform ...)

With Infraform it's really all about ease of use. Infraform not only let's you use the same interface to run all these different technologies but it also supports templating which allows you to re-use the same scenarios for different purposes (e.g. staging and prod environments)

Hope you'll enjoy using it and if not, let us know and open an issue :)

<div align="center"><img src="./images/infraform.png"></div><hr/>

## Requirements

* Linux (developed and tested on Fedora)
* Python>=3.7

## Installation

    git clone https://github.com/bregman-arie/infraform && cd infraform
    virtualenv ~/ifr_venv && source ~/ifr_venv/bin/activate
    pip install .

## Usage Examples

### List Scenarios

    ifr list

## Scenarios

Scenario file is one that ends with `.ifr` or `ifr.j2` suffix. It uses the YAML format with the following directives:

```
description:  # the description of the scenario
platform:     # the platform or tool to use (e.g. terraform, ansible, shell, python, etc.)
files:        # the files to copy to the workspace to be used during the execution of the scenario
 - file1
 - file2
 - directory1
vars:         # variables which will be used for executing the scenario
  x: 2
  y: 'value'
dockerfile: | # used for building an image and running a container using that image
 ...
```

Infraform provides you with a couple of built-in scenarios you can list with `ifr list`<br>
To see the content of scenario, run `infraform show <scenario_name>`

Read more about "Scenarios" [here](docs/scenarios.md)

## Supported platforms and tooling

InfraForm is able to execute using the following technologies

Name | Comments 
:------ |:------:
Terraform | Provision infrastucture using Terraform HCL files
Podman | Run containers using Podman
Docker | Run containers using Docker

### Possibly too detailed workflow

The following is a description of what InfraForm does when you run a scenario

1. Validates the scenario you've specified exists (the .ifr file)
2. If a workspace already exists (.infraform/<SCENARIO_NAME>) it removes it. A new workspace is then created
2. Iterates over the hosts specified (if not specific, then it uses localhost)
  1. Checks if a workspace (.infraform/<SCENARIO_NAME>) directory exists already on the remote host. If it exists, it removes the entire directory
  2. Creates a workspace (.infraform/<SCENARIO_NAME>) directory on the remote host
4. Copies the scenario file (.ifr) and all the related content to the directory on the remote/local host
5. Checks the host is ready for executing the scenario by running chosen platform check command(s)
  1. If check command fails, it will ask the user whether to run commands to fix the check result
    1. If user replied with 'y', it will start executing installation commands based on the chosen platform
    2. If user replied with 'n', it will exit with return code different than 0
6. Runs possible pre-commands. This depends highly on the platform used
   - Terraform -> terraform init
   - Podman -> Possibly build an image before running container
7. Executes the scenario using the platform default run command (e.g. Terraform -> terraform apply)

## Contributions

To contribute to the project, use GitHub pull requests.
