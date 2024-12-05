#!/bin/bash

# Test script for the C client program
# Demonstrates connection to the server, sending commands, and handling responses.

EXECUTABLE="./client"  # Replace with the actual compiled binary path if different.
SERVER_ENDPOINT="tcp://localhost:41005"

# Function to test commands
run_commands() {
    echo "Testing valid commands..."
    $EXECUTABLE <<EOF
list, *-*-*, *, 
more
invalidcommand
exit
EOF
    echo "----------------------------------------"
}

# Function to test argument handling
run_argument_tests() {
    echo "Testing argument handling..."

    echo "Testing with insufficient arguments:"
    $EXECUTABLE arg1 arg2 arg3
    echo "----------------------------------------"

    echo "Testing with valid arguments:"
    $EXECUTABLE "localhost" "41005" "2024" "12" "05" "10" &
	CLIENT_PID=$!
    echo "----------------------------------------"
	kill -SIGINT $CLIENT_PID
}


# Script execution starts here
if ! [ -x "$EXECUTABLE" ]; then
    echo "Error: Client executable not found or not executable. Please compile it."
    exit 1
fi

echo "========================================"
echo "Running argument handling tests..."
run_argument_tests
echo "========================================"

echo "Running command tests..."
run_commands
echo "========================================"

echo "All tests completed."

