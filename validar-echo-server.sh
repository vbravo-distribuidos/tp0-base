# Test echo server

MESSAGE='test'
SERVER_IP=server
SERVER_PORT=12345

RESPONSE=$(echo "$MESSAGE" | nc $SERVER_IP $SERVER_PORT)

if [ "$RESPONSE" == "$MESSAGE" ]; then
    echo 'action: test_echo_server | result: success'
else
    echo 'action: test_echo_server | result: fail'
fi
