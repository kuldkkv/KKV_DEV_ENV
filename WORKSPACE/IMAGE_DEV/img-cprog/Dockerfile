# Docker file to create image of basic C program
#

FROM alpine:edge

WORKDIR /usr/opt/c_prog

COPY media/ media/

WORKDIR media

RUN echo ">>> preparing to install media contents:"; \
    ls -lR ../ ; \
    echo ">>> installing gcc"; \
    apk add musl-dev gcc; \
    echo ">>> gcc version:"; \
    gcc --version; \
    date; \
    echo "compiling:"; \
    gcc byte_rep.c -o ../byte_rep; \
    echo "post install:"; \
    ls -lR ../ ; \
    echo "test invoke:"; \
    sh ./test.sh

CMD ["sleep", "10000"]
