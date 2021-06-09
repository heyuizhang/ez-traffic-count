dependencies: add_darknet get_tiny_yolo_v3_weights get_yolo_v3_weights
all_dcker: get_tiny_yolo_v3_weights get_yolo_v3_weights

add_darknet:
	git submodule init 
	git submodule update 