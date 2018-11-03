#!/bin/bash

docker rm postgres-citibike

docker run --name postgres-citibike -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:10.5
