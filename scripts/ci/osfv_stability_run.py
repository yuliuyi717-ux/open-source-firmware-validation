#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 3mdeb <contact@3mdeb.com>
#
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
import sys

import develop_pr_auto_regression
import tqdm

N_REPEATS = 2
env = os.environ
if "MANUAL_TESTS_LIST" not in env:
    env["MANUAL_TESTS_LIST"] = (
        "scripts/ci/regression-scope/configs/release_tests_suite_list_minimal.txt"
    )
if "DEVICES" not in env:
    env["DEVICES"] = "scripts/ci/regression-scope/configs/release_tests_devices.csv"
if "RULES_FILE" not in env:
    env["RULES_FILE"] = "scripts/ci/regression-scope/configs/release_tests_rules.json"
if "LOGS_DIR" not in env:
    env["LOGS_DIR"] = "ci_logs"
RULES = "scripts/ci/regression-scope/configs/release_tests_rules.json"
env["ALLOW_DIRTY"] = "1"

shutil.rmtree(env["LOGS_DIR"], ignore_errors=True)
os.makedirs(env["LOGS_DIR"])

repeats = tqdm.tqdm(range(N_REPEATS), colour="green")
for i in repeats:
    logs_dir = f"{env["LOGS_DIR"]}/run{i}"
    os.makedirs(logs_dir)
    env["LOGS_DIR"] = logs_dir

    rc = develop_pr_auto_regression.main(silent=True)
    if rc != 0:
        sys.exit(rc)
