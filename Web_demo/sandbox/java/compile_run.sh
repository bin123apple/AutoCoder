#!/bin/bash

set -e

cd /app

mkdir -p src/main/java

mv script.java src/main/java/

mvn clean package

java -jar target/test-1.0-SNAPSHOT.jar
