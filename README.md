# Operating System Simulation

This program is designed to simulate some fundemental operating system operations. These include:
- Process creation, suspension and termination
- Thread creation, suspension and termination
- Inter-process Communication (IPC) for both threads and processes
- Message passing
- Shared memory allocation 

# User Manual 
This OS supports a few commands with subcommands and arguments. Generally it follows the following structure:

### Command Syntax
<command> <sub-command> <argument>
or
<command> <sub-command> 

Bellow is a list of all possible commands and their outputs: 
```
positional arguments:
  {os,process,thread}
    os                 Invoke general CLI commands
    process            Manage Processes
    thread             Manage threads

optional arguments:
  -h, --help           show this help message and exit
```

**os commands**
```
positional arguments:
  {list,help,apps}
    list            Displays a list of all currently running processes
    help            Displays a list of all commands
    apps            Displays a list of all available applications

optional arguments:
  -h, --help        show this help message and exit
```

**process commands**
```
positional arguments:
  {start,kill,suspend,resume}
    start               Start a new process
    kill                Terminate a process that is currently running
    suspend             Pause the execution of a process
    resume              Resume a currently running process

optional arguments:
  -h, --help            show this help message and exit
```

**thread commands**
```
positional arguments:
  {start,kill,suspend,resume}
    start               Start a new thread
    kill                Terminate a thread that is currently running
    suspend             Pause the execution of a thread
    resume              Resume a currently running thread

optional arguments:
  -h, --help            show this help message and exit
```

### Examples
```python
# view a list of functions runnable by a process or thread
os apps
```
**Output**
```
Name          Function
------------  --------------
test_process  test_process()
test_thread   test_thread()
count         process_file()
```

```
# view a table of currently running processes and threads
os list
```
**Output**
```
		- Processes -
  pid  name          is_suspended
-----  ------------  --------------
41388  test_process  False

	 ** No Running Threads **
```

Below is an outline of the file structure and the general function of each file:

# Project Structure 

# `main.py` 
the entry-point for the program. This initializes objects from all other files that are needed to support this projects functionalities. The next crucial component of the `main()` function within is the initialization of the commands available to the user. Using the `argparse` library, we are able to quickly create a CLI for the user complete with help guidance and parsing of their input. 

### `argparse`
After all required resources have been initialized, we enter a loop function that asks for user input and passes that input to argparse. Argparse then parses the input into its consituent components to be used for dispatching procsses and threads with their arguments. with argparse we define commands in the following way: 

first we set some base command. For example, if the user wishes to interact with a process he or she will type 'process' after which will be one of the following possible choices start, create, suspend, resume. This allows us to define functions that handle the specifics of these tasks and argparse abstracts the process of extracting these details. 

```python
# PARSERS FOR PROCESSES
    process_parser = subparsers.add_parser('process', help='Manage Processes')
    process_subparsers = process_parser.add_subparsers(dest='process_command', required=True)

    # starting processes
    process_start = process_subparsers.add_parser('start', help='Start a new process')
    process_start.add_argument('process_name', help='Name of the process')

    # killing processes
    process_kill = process_subparsers.add_parser('kill', help='Terminate a process that is currently running')
    process_kill.add_argument('pid', help='PID of the process')
   # process_kill.add_argument('--f', action='store_true', help='Force kill the process')

    # suspending processes
    process_suspend = process_subparsers.add_parser('suspend', help='Pause the execution of a process')
    process_suspend.add_argument('pid', help='PID of the process')

    # resuming processes
    process_resume = process_subparsers.add_parser('resume', help='Resume a currently running process')
    process_resume.add_argument('pid', help='PID of the process')
```
each sub command pertains to a process and likewise, users can perform the same operations on threads.

# `command_handler.py` 
this function is essentially a router. It is sent an argument object called `arg` from argparse after the user's input has been confirmed valid. Command handler then essentially breaks down the command and invokes all things required to execute that command. This is done with the `handle_command()` function:
```python 
    def handle_command(self, args):
        if args.command == 'os':
            if args.os_command == 'list':
                self.os_list()

            if args.os_command == 'apps':
                self.show_user_apps()

        elif args.command == 'process':
            if args.process_command == 'start':
                app = self.app_manager.get_app(args.process_name)
                if app is not None:
                    self.start_process(name=args.process_name, function_to_execute=app)
                else:
                    print(f"\t** Unknown App `{args.process_name}` **")

        # ...
```

For example if the user wishes to start a process called `my_process`, he or she will type: 'process start my_processs'. The "process" tells command handler that we will be working with a process so to use the functions of the `process_manager`. The second keyword "start" maps to the `start_process()` function of the process manager. Lastly, the third keyword "my_process" is the target function that the process will run. Beyond this, command handler is responsible for displaying some basic OS functions such as the list of user application names and their function mappings, as well as a list of currently executing processes and threads. 

# `process_manager` 
this file holds the `ProcessManager` class which is responsible for doing the following for processes:
- creation (start_process())
- suspension (suspend_process())
- resuming (resume_process())
- termination (kill_process())

the process manager also maintains a list of active processes and through a (slightly) complicated method, continously updates the statuses of each process and ensures that if a process is no longer active it is removed from the list. This is what allows the OS to dynamically display the currently active processes and threads to the user. 

# `thread_manager`
much in the same way `process_manager` handles processes. `thread_manager` deals with threads in a similar fashion. The difference here is that threads represent the most atomic units of operations supported by the OS, we therefore make use of an Idea called an event. An event object from `threading.Event` is used to allow a process to listen for signals that are sent from the OS to it. One limitation of python is its global-interpreter lock (GIL) so we must define logic within each thread to listen for these signals while the thread runs. These signals are defined below:
- `pause_event` - triggers a thread to pause termination and is invoked with the suspend subcommand
- `resume_event` - triggers a thread to continue its execution and is invoked with the resume subcommand
- `stop_event` - termination of a thread. Invoked by the kill subcommand

# `app_manager` 
the app manager allows us to quickly map process names to the functions that they represent. That way, the user can request from the OS a list of application and create processes or threads which run those functions by referenceing the function alias stored in the `name_table` of the `app_manager`. 
For any kind of parallel processing to work in python, it is a requirement that the method being called is static - essentially a class method. Since threads require all 3 signals to be defined, each function thats intended to be run by a thread must support these parameters even if it does not use them as they are automatically passed from the thread_manager when the thread is created (likewise for the process_manager if the function is being run by a process). 

# Logging 
most outputs and commands were logged in a file called `USER_SESSION.log`. This made it possible to quickly save the session history as well as circumvent issues with processes and threads printing to the console when we were blocking to await user input. Below is a snippet of code showing how the log tracks a user session: 
```
2024-03-13 01:02:16,573 - INFO - main - [[ STARTUP SUCCESFUL ]]
2024-03-13 01:02:23,234 - INFO - main - USER_INPUT: process start test_process
2024-03-13 01:02:23,235 - INFO - main - [[ USER INPUT : Namespace(command='process', process_command='start', process_name='test_process')
2024-03-13 01:02:23,245 - INFO - process_manager - [[ Started process 'test_process' | PID: 42992 ]]
```

# Demonstration
below are the demonstrations of the project requirements for the following
- processes
- threads
- IPC
- file processing task

## Processes
```
process start test_process
[[ Started process 'test_process' | PID: 36096 ]]
os list

		- Processes -
  pid  name          is_suspended
-----  ------------  --------------
36096  test_process  False

	 ** No Running Threads **

process suspend 36096
[[ PROCESS [PID=36096] SUSPENDED ]]
>>>MSG FROM PROCESS : Process paused.

os list

		- Processes -
  pid  name          is_suspended
-----  ------------  --------------
36096  test_process  True

	 ** No Running Threads **

process resume 36096
[[ PROCESS [PID=36096] RESUMED ]]

os list

		- Processes -
  pid  name          is_suspended
-----  ------------  --------------
36096  test_process  False

	 ** No Running Threads **

process kill 36096
>>>MSG FROM PROCESS : Process stopped.
```

## Threads 
```
os apps
Name          Function
------------  --------------
test_process  test_process()
test_thread   test_thread()
count         process_file()

thread start test_thread
Thread with [TID=13880] has started

thread suspend 13880
Thread with [TID=13880] has been paused

thread resume 13880
Thread with [TID=13880] has been resumed

thread kill 13880
(<Thread(Thread-1, started 13880)>, <threading.Event object at 0x0000029100C940D0>, <threading.Event object at 0x0000029100C01730>)
13880
Thread 13880 has been stopped
```

## IPC 
IPC was performed using test functions located in `tests/test_process_ipc.py`. This was done since wed be generating many processes and threads and facillitating their communication as well as passing hundreds of messages

```
C:\Users\aaron\AppData\Local\Programs\Python\Python39\python.exe "C:/Program Files/JetBrains/PyCharm 2023.2.1/plugins/python/helpers/pycharm/_jb_trialtest_runner.py" --path C:\Users\aaron\Projects\classWork\CMPSC472\OperatingSystemSimulation\tests\test_process_ipc.py 
Testing started at 12:33 AM ...
Launching trial with arguments --reporter=teamcity C:\Users\aaron\Projects\classWork\CMPSC472\OperatingSystemSimulation\tests\test_process_ipc.py in C:\Users\aaron\Projects\classWork\CMPSC472\OperatingSystemSimulation\tests


===============================================================================
[ERROR]
Traceback (most recent call last):
Failure: builtins.tuple: (<class 'AttributeError'>, AttributeError("'int' object has no attribute 'start'"), <traceback object at 0x000001ACFEFF22C0>)

test_process_ipc.TestProcessManagerIPC.test_shared_value_message_passing
-------------------------------------------------------------------------------
Ran 5 tests in 3.104s

FAILED (errors=1, successes=4)
[[ Started process 'ipc_message_queue_test' | PID: 35944 ]]
[[ Started process 'Producer' | PID: 16924 ]]

Time for long messages: 1.0836842060089111

[[ Started process 'Producer' | PID: 24072 ]]
[[ Started process 'Consumer' | PID: 25156 ]]

Time for short messages: 0.8217775821685791

[[ Started process 'increment' | PID: 12908 ]]
[[ Started process 'decrement' | PID: 33032 ]]

Error
Traceback (most recent call last):
Failure: builtins.tuple: (<class 'AttributeError'>, AttributeError("'int' object has no attribute 'start'"), <traceback object at 0x000001ACFEFF22C0>)

<Synchronized wrapper for c_long(0)>
-1
0

Process finished with exit code 1
```

## File Processing Demonstration
the last component of this demonstration is use of these OS functions to efficiently breakdown a task and dispatch the partioned substasks to worker processes and threads. The task at hand is to do the following: given a text file, count the occurence of each charecter and create a new file with all words capitalized. This program is invoked by creating a process which runs the function `process_file`. Within that function the following occurs:

1. the text file is partioned into roughly equal parts specified by the hard-coded value `num_threads` which denotes the number of threads that will be used to handle the partioned work.
2. a shared queue is created to hold counts for the letters and a separate shared queue is created to hold the capitalized text of the
3. two loops are then employed to create threads that each work on their partition. The first loop creates threads responsible for counting the character occurances within their specific chunk of text. The second loop is used to store a list of capitalized letters from its chuck of text.
4. The shared queue is either logged (in the case of the character count) or a new file is created (for the capitalized words).

In my demonstration we are parsing the script of the movie 'Shrek'.

### Running the process and threads
```
process start count
[[ Started process 'count' | PID: 13204 ]]
Thread with [TID=41180] has started
Thread with [TID=41996] has started
Thread with [TID=31716] has started
Thread with [TID=34568] has started
Thread with [TID=45112] has started
Thread with [TID=45240] has started
Thread with [TID=31128] has started
Thread with [TID=46124] has started
[[ PROCESS FINISHED ]]
```
above, we have created 8 threads. The first 4 are responsible for counting their sections of the text. The latter 4 are responsible for capitalizing the text in their chunk. 

### Original Text 
```
SHREK
                         Once upon a time there was a lovely
                         princess. But she had an enchantment
                         upon her of a fearful sort which could
                         only be broken by love's first kiss.
                         She was locked away in a castle guarded
                         by a terrible fire-breathing dragon.
                         Many brave knights had attempted to
                         free her from this dreadful prison,
                         but non prevailed. She waited in the
                         dragon's keep in the highest room of
                         the tallest tower for her true love
                         and true love's first kiss. (laughs)
                         Like that's ever gonna happen. What
                         a load of - (toilet flush)

               Allstar - by Smashmouth begins to play. Shrek goes about his
               day. While in a nearby town, the villagers get together to go
               after the ogre...
```
### Charecter Count Output (in log)
a log is used to track all commands and events within a session. Below is a snippet of the log showing the result of the charecter count process (this may be found in `USER_SESSION.log`): 
```
2024-03-13 00:45:11,350 - INFO - main - [[ STARTUP SUCCESFUL ]]
2024-03-13 00:45:16,672 - INFO - main - USER_INPUT: process start count
2024-03-13 00:45:16,672 - INFO - main - [[ USER INPUT : Namespace(command='process', process_command='start', process_name='count')
2024-03-13 00:45:16,683 - INFO - process_manager - [[ Started process 'count' | PID: 31576 ]]
2024-03-13 00:45:16,953 - INFO - thread_manager - Thread with [TID=16868] has started
2024-03-13 00:45:16,957 - INFO - thread_manager - Thread with [TID=27876] has started
2024-03-13 00:45:16,960 - INFO - thread_manager - Thread with [TID=16808] has started
2024-03-13 00:45:16,963 - INFO - thread_manager - Thread with [TID=44448] has started
2024-03-13 00:45:16,969 - INFO - thread_manager - Thread with [TID=8372] has started
2024-03-13 00:45:16,978 - INFO - thread_manager - Thread with [TID=41948] has started
2024-03-13 00:45:16,984 - INFO - thread_manager - Thread with [TID=34724] has started
2024-03-13 00:45:16,989 - INFO - thread_manager - Thread with [TID=10516] has started
2024-03-13 00:45:16,991 - INFO - app_manager - Char Count: {'S': 115, 'H': 126, 'R': 141, 'E': 148, 'K': 89, '\n': 917, ' ': 20646, 'O': 123, 'n': 807, 'c': 241, 'e': 1457, 'u': 449, 'p': 161, 'o': 988, 'a': 977, 't': 1034, 'i': 691, 'm': 280, 'h': 752, 'r': 674, 'w': 223, 's': 697, 'l': 544, 'v': 102, 'y': 330, '.': 365, 'B': 39, 'd': 416, 'f': 228, 'b': 180, 'k': 227, "'": 153, 'g': 300, '-': 24, 'M': 51, ',': 163, '(': 65, ')': 65, 'L': 50, 'W': 60, 'A': 162, 'N': 116, 'I': 140, 'G': 71, 'T': 105, '1': 5, '?': 62, '2': 4, '!': 129, 'D': 165, '3': 6, 'Y': 69, 'q': 20, 'z': 5, 'j': 15, 'x': 12, '"': 4, 'F': 42, 'X': 1, 'P': 32, 'U': 52, 'C': 28, '0': 2, 'J': 2, 'Q': 21, '4': 1}
```
### Capitalized Text File 
a new text file is created and all the lines from the shared queue for capitalization processes was created (capitalized_shrek.text). A snippet of this is given below: 
```SHREK
                         ONCE UPON A TIME THERE WAS A LOVELY
                         PRINCESS. BUT SHE HAD AN ENCHANTMENT
                         UPON HER OF A FEARFUL SORT WHICH COULD
                         ONLY BE BROKEN BY LOVE'S FIRST KISS.
                         SHE WAS LOCKED AWAY IN A CASTLE GUARDED
                         BY A TERRIBLE FIRE-BREATHING DRAGON.
                         MANY BRAVE KNIGHTS HAD ATTEMPTED TO
                         FREE HER FROM THIS DREADFUL PRISON,
                         BUT NON PREVAILED. SHE WAITED IN THE
                         DRAGON'S KEEP IN THE HIGHEST ROOM OF
                         THE TALLEST TOWER FOR HER TRUE LOVE
                         AND TRUE LOVE'S FIRST KISS. (LAUGHS)
                         LIKE THAT'S EVER GONNA HAPPEN. WHAT
                         A LOAD OF - (TOILET FLUSH)

               ALLSTAR - BY SMASHMOUTH BEGINS TO PLAY. SHREK GOES ABOUT HIS
               DAY. WHILE IN A NEARBY TOWN, THE VILLAGERS GET TOGETHER TO GO
               AFTER THE OGRE...
```


# Discussion
This project made me think about the way that concurrent processes and threads must be sequenced and coordinated. I had many issues with strange behavior or errors that had to be worked out by carefully following the execution. The structure of this project also made me think about the importance of good structuring of my code and heavy use of the single responsibility principle for functions. Although at first the use of many files to hold different functionalities was tedious, this allowed a clean way to integrate different parts of the project together and to be sure that things would only need to be written once and work. 

Although a high level programming language like python makes it easy to quickly prototype some OS functions, a lot of thought an akward solutions had to be used to simulate true parallel processing, something that would have been a bit more straight forward had I used a lower level language like C. However, using libraries like multithreading and psutil I was able to create a relatively stable and somewhat realistic (at the user level) rudimentary OS demonstrator. Some issues that were most impactful was the fact that all threads and processes had to have listeners for signals to pause, resume, or terminate them. Also, there were issues getting a smooth cli experience, especially for processes as sometimes a processes's output would block the users input prompt or, in the completet opposite direction, the user prompt would block processes from printing their outputs to the screen. Threads however were not impacted by this issue and performed as desired. Overall this was an interesting project and I feel I have become more comfortable with processes and threads. 

