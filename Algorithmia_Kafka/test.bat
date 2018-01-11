start python test-producer.py -p 9092 -t test-input-topic --ip 162.105.85.212
start python test-model.py -l -p 9092 -k sim0p9Q80e7GOrE1/4Vb6MLeVMg1 -m efzeyuan/Hello/0.1.0 --input_topic test-input-topic --output_topic test-output-topic --ip 162.105.85.212
start python test-consumer.py -l -p 9092 -t test-output-topic --ip 162.105.85.212 
