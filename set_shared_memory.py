
import numpy as np
from multiprocessing import shared_memory

class SetSharedMemoryHandler:
    def __init__(self, base_name, width, height):

        self.base_name = base_name
        self.width = width
        self.height = height

        self.shm_name_image_data_1 = f"{base_name}_1"
        self.shm_name_image_data_2 = f"{base_name}_2"
        self.shm_name_prepared_index = f"{base_name}_index"
        self.shm_name_res_width = f"{base_name}_res_w"
        self.shm_name_res_height = f"{base_name}_res_h"

        self.shm_image_data_1 = self.create_shared_memory(self.shm_name_image_data_1, self.width * self.height * 4)
        self.shm_image_data_2 = self.create_shared_memory(self.shm_name_image_data_2, self.width * self.height * 4)
        
        self.shm_prepared_index = self.create_or_open_shared_memory(self.shm_name_prepared_index, 4)
        
        self.shm_res_width = self.create_or_open_shared_memory(self.shm_name_res_width, 4)
        self.shm_res_height = self.create_or_open_shared_memory(self.shm_name_res_height, 4)

        self.prepared_index_data = np.ndarray((1,), dtype=np.int32, buffer=self.shm_prepared_index.buf)
        self.prepared_index_data[0] = 0
        
        self.res_width_data = np.ndarray((1,), dtype=np.int32, buffer=self.shm_res_width.buf)
        self.res_width_data[0] = width
        self.res_height_data = np.ndarray((1,), dtype=np.int32, buffer=self.shm_res_height.buf)
        self.res_height_data[0] = height

    def create_or_open_shared_memory(self, name, size):
        try:
            shm = shared_memory.SharedMemory(name=name)
            # print(f"Shared memory '{name}' already exists, opening existing memory.")
        except FileNotFoundError:
            shm = shared_memory.SharedMemory(create=True, size=size, name=name)
            # print(f"Shared memory '{name}' created.")
        return shm
    
    def create_shared_memory(self, name, size):
        try:
            shm = shared_memory.SharedMemory(name=name)
            print(f"Shared memory '{name}' already exists, deleting and recreating.")
            
            shm.close()
            shm.unlink()
            
        except FileNotFoundError:
            print(f"Shared memory '{name}' does not exist.")
        
        shm = shared_memory.SharedMemory(create=True, size=size, name=name)
        print(f"Shared memory '{name}' created.")
        
        return shm    

    def send_image_data(self, shm, image_data):
        img_data = np.ndarray(image_data.shape, dtype=np.uint8, buffer=shm.buf)
        np.copyto(img_data, image_data)

    def send_image_data_by_switch_buffer(self, image_data):
        if self.prepared_index_data[0] == 1:
            self.send_image_data(self.shm_image_data_1, image_data)
            self.prepared_index_data[0] = 2
            # print("Sent new image data to shm1.")
        else:
            self.send_image_data(self.shm_image_data_2, image_data)
            self.prepared_index_data[0] = 1
            # print("Sent new image data to shm2.")

    def get_shared_memory_buffers(self):
        return self.shm_image_data_1, self.shm_image_data_2, self.shm_prepared_index, self.prepared_index_data
