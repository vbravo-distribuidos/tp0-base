docker pull --quiet busybox
docker run --rm --network tp0_testing_net busybox sh -c \
"if [[ \"\$(echo test | nc server 12345)\" == \"test\" ]] ; then \
    echo 'action: test_echo_server | result: success'; \
 else \
    echo 'action: test_echo_server | result: fail' \
; fi"