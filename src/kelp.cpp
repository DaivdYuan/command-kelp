// this file invokes the helper functions by calling python scripts through system calls    
#include <iostream>
#include <string>

const std::string command = "python3 /usr/local/lib/command_helper/helper.py";

int main(int argc, char *argv[]) {
    // put all the arguments into a string
    std::string command_to_run = command;
    for (int i = 1; i < argc; i++) {
        command_to_run += " " + std::string(argv[i]);
    }
    system(command_to_run.c_str());
    return 0;
}
