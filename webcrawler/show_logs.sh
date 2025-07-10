#!/usr/bin/env bash

# Follow the log, starting 100 lines from the end, and don't add the container prefix.
# If you are running more than one container you might want to remove the --no-log-prefix.
docker-compose logs -f --tail 100 --no-log-prefix
