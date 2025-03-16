docker pull busybox 1> /dev/null 2> /dev/null
docker run -it --rm --network tp0_testing_net busybox sh -c \
"if echo test | nc server 12345 | grep -q test; then \
    echo 'action: test_echo_server | result: success'; \
 else \
    echo 'action: test_echo_server | result: fail' \
; fi"