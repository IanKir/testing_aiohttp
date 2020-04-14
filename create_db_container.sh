#!/bin/bash
docker run --name dbserver -p 5432:5432 -e POSTGRES_PASSWORD=testuser -d postgres