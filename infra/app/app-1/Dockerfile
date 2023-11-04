FROM alpine:latest

#FROM --platform=linux/amd64 alpine:latest

RUN apk add --no-cache bash

COPY greet_from_01.sh /usr/local/bin/

COPY return.json /usr/local/bin/


RUN chmod +x /usr/local/bin/greet_from_01.sh

CMD ["greet_from_01.sh"]