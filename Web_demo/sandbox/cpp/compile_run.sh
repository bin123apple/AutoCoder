#!/bin/bash

set -e

# echo "Starting compilation and execution..."

# compile
g++ -fopenmp /app/script.cpp -L/usr/local/lib -lgtest -lgtest_main -pthread -o /app/test

# run
/app/test --gtest_print_time=0 --gtest_brief=1

# echo "Execution completed."

# exit_code=$?
# exit $exit_code