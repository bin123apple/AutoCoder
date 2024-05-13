#!/bin/bash
# compile
gfortran -fopenmp -J /app/ -o /app/test /app/script.f90
# run
/app/test
