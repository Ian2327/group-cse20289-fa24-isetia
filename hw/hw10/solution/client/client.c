#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zmq.h>

#define MAX_COMMAND_LEN 256
#define SERVER_ENDPOINT "tcp://localhost:41005"
//#define SERVER_ENDPOINT "tcp://%s:%s"
// Port for testing: "tcp://localhost:41005"
// Makes sure input is not empty
int validate_input(const char *input) {
	if(strlen(input) == 0){
		printf("Error: Command cannot be empty.\n");
		return 0;
	}

	//Add more checks later for command formatting
	return 1;
}

int main(int argc, char *argv[]){
	// if(argc < 7){
	// 	fprintf(stderr, "%s <HOST> <PORT> [-query <FILTER_STRING>] <YEAR> <MONTH> <DAY> <HOUR>", argv[0]);
	// 	return EXIT_FAILURE;
	// }
	// char *host = argv[1];
	// char *port = argv[2];

	// char server_endpoint[MAX_COMMAND_LEN];
	// snprintf(server_endpoint, MAX_COMMAND_LEN, SERVER_ENDPOINT, host, port);
	if(argc == 1){
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
	}else if(argc > 6){
		printf("Starting server/client system with shell script.\n");
		char *host  = argv[1];
		char *port  = argv[2];
		char *year  = argv[3];
		char *month = argv[4];
		char *day   = argv[5];
		char *hour  = argv[6];
		printf("Host: %s\n", host);
		printf("Port: %s\n", port);
		printf("Year: %s\n", year);
		printf("Month: %s\n", month);
		printf("Day: %s\n", day);
		printf("Hour: %s\n", hour);

		char filter_string[MAX_COMMAND_LEN] = "";
		if(argc == 8){
			sprintf(filter_string, argv[7]);
		}
		char server_endpoint[25];
		sprintf(server_endpoint, "tcp://%s:%s", host, port);
		printf("%s\n", server_endpoint);
		printf("%s\n", filter_string);
		char command[MAX_COMMAND_LEN];
		sprintf(command, ", %s-%s-%s, %s, %s", year, month, day, hour, filter_string);

		void *context = zmq_ctx_new();
		void *socket = zmq_socket(context, ZMQ_REQ);
		if(zmq_connect(socket, server_endpoint) != 0){
			perror("Error connecting to server");
			zmq_close(socket);
			zmq_ctx_destroy(context);
			return EXIT_FAILURE;
		}
		printf("Connected to server at %s\n", server_endpoint);
		while(1){
			char command_part[MAX_COMMAND_LEN]; // Holds the first part of the command (list, more, count, etc.)
			printf("Enter command (or 'exit' to quit): ");
			if(fgets(command_part, MAX_COMMAND_LEN, stdin) == NULL){
				printf("Error reading input.\n");
				continue;
			}else{
				//printf("Command_part: %s", command_part);
			}
			size_t len = strlen(command_part);
			if(len > 0 && command_part[len-1] == '\n'){
				command_part[len-1] = '\0';
			}

			if(strcmp(command_part, "exit") == 0){
				zmq_send(socket, command_part, strlen(command_part), 0);
				printf("Exiting...\n");
				break;
			}
			if(strcmp(command_part, "more") == 0){
				zmq_send(socket, command_part, strlen(command_part), 0);
			}else{
				if(!validate_input(command)){
					continue;
				}
				char full_command[MAX_COMMAND_LEN];
				//printf("Partial command: %s\n", command);
				sprintf(full_command, "%s%s", command_part, command);
				//printf("FULL COMMAND: %s\n", full_command);
				if(zmq_send(socket, full_command, strlen(full_command), 0) == -1){
					perror("Error sending command");
					continue;
				}
			}
			char response[MAX_COMMAND_LEN] = {0};
			int received = zmq_recv(socket, response, MAX_COMMAND_LEN - 1, 0);
			if(received == -1){
				perror("Error receiving response");
				continue;
			}
			response[received] = '\0';

			printf("FULL RESPONSE: %s\n", response);

			// Start of reponse formatting instead of writing bbf.sh script

			printf("\n=============================================\n");
        	printf("Server Response:\n");
        	printf("=============================================\n");
    		int count = 0;
    		char *key = NULL;
    		char *value = NULL;
			char *token = strtok(response, ",");
			printf("%-20s: %s\n", "Status", token);
			if(strcmp(token, "failure") == 0){
				token = strtok(NULL, ",");
				printf("%-20s: %s\n", "Reason", token);
				token = strtok(NULL, ",");
			}
			else if(strcmp(command_part, "more") == 0 || strcmp(command_part, "list") == 0){
				token = strtok(NULL, ",");
				printf("%-20s: %s\n", "Number in list", token);
			}
   			// Iterate through each token and format it as key-value pair
			token = strtok(NULL, ",");
   			while (token != NULL) {
		        if (count % 2 == 0) {
		            key = token; // Every even token is a key
		        } else {
		            value = token; // Every odd token is a value
		            printf("%-20s: %s\n", key, value);
		        }
			    count++;
			    token = strtok(NULL, ", ");
			}
	
			// End of the response formatting
			printf("=============================================\n");
		}	
	
		
	}else{
		printf("There are an incorrect number of arguments to client.c script.\n");
	}
}

