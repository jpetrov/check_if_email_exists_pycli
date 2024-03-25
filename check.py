#!/bin/bash
./check_if_email_exists $1 | grep "is_reachable"
