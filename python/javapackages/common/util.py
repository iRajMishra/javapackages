#!/usr/bin/python
# Copyright (c) 2014, Red Hat, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the Red Hat nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:  Michal Srb <msrb@redhat.com>

import os
import signal
import sys
import six
import subprocess


def kill_parent_process():
    os.kill(os.getppid(), signal.SIGTERM)


def get_cachedir(path, create_if_not_exists=True):
    cachedir_path = os.path.join(path, ".javapackages_cache")
    if not os.path.exists(cachedir_path) and create_if_not_exists:
        os.makedirs(cachedir_path)
    return cachedir_path


def args_to_unicode(args):
    if six.PY2:
        for index, arg in enumerate(args):
            args[index] = arg.decode(sys.getfilesystemencoding())
    return args


def execute_command(binpath, args=[], env=None, input=None, shell=False,
                    enable_scl=None):
    scl_cmd = "scl enable {scl}"
    command = ""
    if enable_scl:
        scl_cmd = scl_cmd.format(scl=enable_scl)
        command = scl_cmd + " && "
        shell = True
    command = [command + binpath]
    command.extend(args)

    proc = subprocess.Popen(command, shell=shell,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE, universal_newlines=True,
                            env=env)
    stdout, stderr = proc.communicate(input=None)
    proc.wait()
    return proc.returncode, stdout, stderr
