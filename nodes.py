import torch
import numpy as np
import cv2

import comfy

from . import get_shared_memory
from . import set_shared_memory

class LoadImageFromLocalCamera:

    node_status_change_all_the_time_value = 0
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {

            },
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = (
        "image",
    )

    FUNCTION = "run"
    CATEGORY = "LocalCamera"

    def run(self):

        base_name = "camera_to_comfy"
        shared_memory_handler = get_shared_memory.GetSharedMemoryHandler(base_name)
        shared_memory_handler.initialize()

        bgra_data = shared_memory_handler.get_image_data()

        # bgra_data => tensor_img
        img_rgb = cv2.cvtColor(bgra_data, cv2.COLOR_BGR2RGB)
        numpy_image = np.array(img_rgb)
        numpy_image = numpy_image / 255.0
        tensor_img = torch.from_numpy(numpy_image)

        image_out = [tensor_img]
        
        return (torch.stack(image_out, dim=0), )

    @classmethod
    def IS_CHANGED(this_cls):
        this_cls.node_status_change_all_the_time_value ^= 1
        return this_cls.node_status_change_all_the_time_value

class SaveImageToLocalCamera:

    change_id = 0
    def __init__(self):
        self.shm = None
        self.width = 0
        self.height = 0
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    FUNCTION = "run"
    CATEGORY = "LocalCamera"

    def run(self, images):

        base_name = "comfy_to_camera"

        idx = 0
        pbar = comfy.utils.ProgressBar(len(images))
        for image in images:
            
            height, width, channels = image.shape 
            
            if height != self.height or width != self.width or self.shm is None:
                self.shm = None
                self.shm = set_shared_memory.SetSharedMemoryHandler(base_name=base_name, width=width, height=height)
                self.width = width
                self.height = height
                print("new shm for send image", self.width, self.height)

            numpy_image = image.numpy()
            numpy_image = numpy_image * 255.0
            numpy_image = numpy_image.astype('uint8')

            bgra_image_data = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGRA)

            self.shm.send_image_data_by_switch_buffer(bgra_image_data)

            idx = idx + 1

            pbar.update(1)
            
        return {}


NODE_CLASS_MAPPINGS = {
    "Load Image From Local Camera": LoadImageFromLocalCamera,
    "Save Image To Local Camera": SaveImageToLocalCamera,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Load Image From Local Camera": "Load Image From Local Camera",
    "Save Image To Local Camera": "Save Image To Local Camera",
}