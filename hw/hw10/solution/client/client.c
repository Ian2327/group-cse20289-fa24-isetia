#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zmq.h>

#define MAX_COMMAND_LEN 256
#define SERVER_ENDPOINT "tcp://localhost:41005"

// Makes sure input is not empty
int validate_input(const char *input) {
	if(strlen(input) == 0){
		printf("Error: Command cannot be empty.\n");
		return 0;
	}

	//Add more checks later for command formatting
	return 1;
}

int main(){
	void *context = zmq_ctx_new();
	void *socket = zmq_socket(context, ZMQ_REQ);
	if(zmq_connect(socket, SERVER_ENDPOINT) != 0){
		perror("Error connecting to server");
		zmq_close(socket);
		zmq_ctx_destroy(context);
		return EXIT_FAILURE;
	}
	printf("Connected to server at %s\n", SERVER_ENDPOINT);
	char command[MAX_COMMAND_LEN];

	while(1){
		printf("Enter command (or 'exit' to quit): ");
		if(fgets(command, MAX_COMMAND_LEN, stdin) == NULL){
			printf("Error reading input.\n");
			continue;
		}

		size_t len = strlen(command);
		if(len > 0 && command[len-1] == '\n'){
			command[len-1] = '\0';
		}

		if(strcmp(command, "exit") == 0){
			zmq_send(socket, command, strlen(command), 0);
			printf("Exiting...\n");
			break;
		}
		if(!validate_input(command)){
			continue;
		}
		if(zmq_send(socket, command, strlen(command), 0) == -1){
			perror("Error sending command");
			continue;
		}
		char response[MAX_COMMAND_LEN] = {0};
		int received = zmq_recv(socket, response, MAX_COMMAND_LEN - 1, 0);
		if(received == -1){
			perror("Error receiving response");
			continue;
		}
		response[received] = '\0';
		printf("Server response: %s\n", response);
	
	}

	zmq_close(socket);
	zmq_ctx_destroy(context);
	return EXIT_SUCCESS;
}

