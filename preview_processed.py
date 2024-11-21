import time
import numpy as np
import cv2

import get_shared_memory
def recv_and_display_images(base_name):
    
    while True:
        
        # local var. release per loop for windows can recreate shared memory when resize image
        shared_memory_handler = get_shared_memory.GetSharedMemoryHandler(base_name)
        
        shared_memory_handler.initialize()

        image_data = shared_memory_handler.get_image_data()
        
        if image_data is None:
            print("Error: Image data is None")
            time.sleep(1)
        elif isinstance(image_data, np.ndarray) and image_data.shape[0] > 0 and image_data.shape[1] > 0:
            cv2.imshow("Processed Preview", image_data)
        else:
            print(f"Error: Invalid image data with shape {image_data.shape if isinstance(image_data, np.ndarray) else 'N/A'}")
            time.sleep(1)

        cv2.waitKey(1)
        
        time.sleep(0.03) # 30fps
    
    cv2.destroyAllWindows()

if __name__ == "__main__":

    base_name = "comfy_to_camera"

    recv_and_display_images(base_name)
    
