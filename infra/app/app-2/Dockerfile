FROM alpine:latest

# FROM --platform=linux/amd64 alpine:latest

RUN apk add --no-cache bash

COPY greet_from_02.sh /usr/local/bin/

# TODO - Throws error when comment below : cp: can't stat 'return.json': No such file or directory
COPY return.json /usr/local/bin/

RUN chmod +x /usr/local/bin/greet_from_02.sh

CMD ["greet_from_02.sh"]