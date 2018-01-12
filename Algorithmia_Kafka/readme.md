Run run.bat to start the program on windows.
Run run.sh to start the program on linux.
You can run your own program by modifying operating parameters, see comments in python files.

The script will start a kafka producer, a kafka consumer and a Algorithmia model.
The Algorithmia model will consume the data from input topic, process the data, and send the processed data to the output topic.

The program supports both python 2&3 now.
