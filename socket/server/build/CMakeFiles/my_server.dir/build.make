# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sofia/src/socket/server

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sofia/src/socket/server/build

# Include any dependencies generated for this target.
include CMakeFiles/my_server.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/my_server.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/my_server.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/my_server.dir/flags.make

CMakeFiles/my_server.dir/server.c.o: CMakeFiles/my_server.dir/flags.make
CMakeFiles/my_server.dir/server.c.o: ../server.c
CMakeFiles/my_server.dir/server.c.o: CMakeFiles/my_server.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sofia/src/socket/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/my_server.dir/server.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/my_server.dir/server.c.o -MF CMakeFiles/my_server.dir/server.c.o.d -o CMakeFiles/my_server.dir/server.c.o -c /home/sofia/src/socket/server/server.c

CMakeFiles/my_server.dir/server.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/my_server.dir/server.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sofia/src/socket/server/server.c > CMakeFiles/my_server.dir/server.c.i

CMakeFiles/my_server.dir/server.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/my_server.dir/server.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sofia/src/socket/server/server.c -o CMakeFiles/my_server.dir/server.c.s

# Object files for target my_server
my_server_OBJECTS = \
"CMakeFiles/my_server.dir/server.c.o"

# External object files for target my_server
my_server_EXTERNAL_OBJECTS =

my_server: CMakeFiles/my_server.dir/server.c.o
my_server: CMakeFiles/my_server.dir/build.make
my_server: CMakeFiles/my_server.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sofia/src/socket/server/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable my_server"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/my_server.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/my_server.dir/build: my_server
.PHONY : CMakeFiles/my_server.dir/build

CMakeFiles/my_server.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/my_server.dir/cmake_clean.cmake
.PHONY : CMakeFiles/my_server.dir/clean

CMakeFiles/my_server.dir/depend:
	cd /home/sofia/src/socket/server/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sofia/src/socket/server /home/sofia/src/socket/server /home/sofia/src/socket/server/build /home/sofia/src/socket/server/build /home/sofia/src/socket/server/build/CMakeFiles/my_server.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/my_server.dir/depend

