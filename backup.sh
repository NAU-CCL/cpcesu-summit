#!/bin/bash
sudo pg_dump -U postgres --format=c --file=cpcesupm_local_201905090605.sqlc cpcesupm
