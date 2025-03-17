all: 
	python src/main.py -dq "data/dynamic_queue.csv" -eds "data/execution_dataset.csv" -sa "FIFO"
	python src/main.py -dq "data/dynamic_queue.csv" -eds "data/execution_dataset.csv" -sa "WEIGHTED_PRIORITY"
	python src/main.py -ubp -bsf "data/bp_scheduler.csv" -dq "data/dynamic_queue.csv" -eds "data/execution_dataset.csv" -sa "FIFO"


clean:
	find logs/ -maxdepth 1 -type f -delete