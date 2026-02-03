#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 3mdeb <contact@3mdeb.com>
#
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
import subprocess
import sys

import tqdm

N_REPEATS = 5
LOGS_DIR = "ci_logs"
MANUAL_TESTS_LIST = "scripts/ci/regression-scope/configs/release_tests_suite_list.txt"
DEVICES_LIST = "scripts/ci/regression-scope/configs/release_tests_devices.csv"


def run_command(cmd, env=os.environ.copy()):
    """
    Wrapper for subprocess.run to not repeat decoding the output too much
    """
    out = subprocess.run(cmd, capture_output=True, env=env)
    out = out.stdout.decode("utf-8").splitlines()
    return out


env = os.environ.copy()
env["ALLOW_DIRTY"] = "1"
env["MANUAL_TESTS_LIST"] = MANUAL_TESTS_LIST
env["DEVICES"] = DEVICES_LIST

shutil.rmtree(LOGS_DIR, ignore_errors=True)
os.makedirs(LOGS_DIR)

repeats = tqdm.tqdm(range(N_REPEATS))
for i in repeats:
    logs_dir = f"{LOGS_DIR}/run{i}"
    os.makedirs(logs_dir)
    env["LOGS_DIR"] = logs_dir
    out = run_command(["./scripts/ci/develop_pr_auto_regression.sh"], env=env)
    print(out)
