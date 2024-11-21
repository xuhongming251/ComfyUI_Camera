import numpy as np
import time
from multiprocessing import shared_memory

class GetSharedMemoryHandler:
    def __init__(self, base_name):
        self.base_name = base_name
        self.width = 0
        self.height = 0
        
        self.shm_name_image_data_1 = f"{base_name}_1"
        self.shm_name_image_data_2 = f"{base_name}_2"
        self.shm_name_prepared_index = f"{base_name}_index"
        self.shm_name_res_width = f"{base_name}_res_w"
        self.shm_name_res_height = f"{base_name}_res_h"
        
        self.shm_image_data_1 = None
        self.shm_image_data_2 = None
        self.shm_prepared_index = None
        self.shm_res_width = None
        self.shm_res_height = None
        
        self.img_data1 = None
        self.img_data2 = None
        self.prepared_index_data = None
        self.res_width_data = None
        self.res_height_data = None
    
    def get_res_width(self):
        return self.res_width_data[0]
    
    def get_res_height(self):
        return self.res_height_data[0]
    def open_shared_memory(self):
        while True:
            try:
                self.shm_image_data_1 = shared_memory.SharedMemory(name=self.shm_name_image_data_1)
                self.shm_image_data_2 = shared_memory.SharedMemory(name=self.shm_name_image_data_2)
                self.shm_prepared_index = shared_memory.SharedMemory(name=self.shm_name_prepared_index)
                self.shm_res_width = shared_memory.SharedMemory(name=self.shm_name_res_width)
                self.shm_res_height = shared_memory.SharedMemory(name=self.shm_name_res_height)
                
                self.res_width_data = np.ndarray((1,), dtype=np.int32, buffer=self.shm_res_width.buf)
                self.res_height_data = np.ndarray((1,), dtype=np.int32, buffer=self.shm_res_height.buf)
                
                self.width = self.res_width_data[0]
                self.height = self.res_height_data[0]
                
                # print("Shared memory opened.", self.width, self.height)
                
                self.img_data1 = np.ndarray((self.height, self.width, 4), dtype=np.uint8, buffer=self.shm_image_data_1.buf)
                self.img_data2 = np.ndarray((self.height, self.width, 4), dtype=np.uint8, buffer=self.shm_image_data_2.buf)
                
                self.prepared_index_data = np.ndarray((1,), dtype=np.int32, buffer=self.shm_prepared_index.buf)
                
                break
            except FileNotFoundError:
                print("Shared memory not found, waiting...")
                time.sleep(1)

    def get_image_data(self):
        if self.prepared_index_data[0] == 1:
            # print("1")
            return self.img_data2
        elif self.prepared_index_data[0] == 2:
            # print("2")
            return self.img_data1
        else:
            return None
    
    def initialize(self):
        self.open_shared_memory()
        return self.shm_image_data_1, self.shm_image_data_2, self.shm_prepared_index, self.img_data1, self.img_data2, self.prepared_index_data

