import time
import cv2
import tkinter as tk

import set_shared_memory

def get_supported_resolutions(cap, resolutions):
    supported_resolutions = []
    
    for width, height in resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        current_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        current_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        if current_width == width and current_height == height:
            supported_resolutions.append((width, height))
    
    return supported_resolutions

def select_resolution(supported_resolutions):
    
    root = tk.Tk()
    
    root.title("Camera Resolution")
    
    root.geometry("300x150")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 300
    window_height = 150

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    selected_resolution = tk.StringVar(root)
    
    resolution_options = [f"{width}x{height}" for width, height in supported_resolutions]

    selected_resolution.set(resolution_options[0])

    dropdown = tk.OptionMenu(root, selected_resolution, *resolution_options)
    dropdown.pack(pady=20)

    def on_select():
        selected = selected_resolution.get()
        root.quit()

        for res in supported_resolutions:
            if f"{res[0]}x{res[1]}" == selected:
                print(f"Selected resolution: {selected}")
                root.destroy()
                return res
            print("Invalid resolution selected.")
        root.destroy()
        return None

    select_button = tk.Button(root, text="OK", command=on_select)
    select_button.pack()

    root.mainloop()

    ret = selected_resolution.get()
    return ret
def image_data_producer_by_camera(cap, share_memory_base_name):

    have_inited_share_memory = False
    width = 0
    height = 0
    shared_memory_handler = None
    while True:
        
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        if not have_inited_share_memory or width != frame.shape[1] or height != frame.shape[0]:
            
            width = frame.shape[1]
            height = frame.shape[0]
            have_inited_share_memory = True
            
            shared_memory_handler = set_shared_memory.SetSharedMemoryHandler(base_name=share_memory_base_name, width=width, height=height)

        frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        
        shared_memory_handler.send_image_data_by_switch_buffer(frame_bgra)

        cv2.imshow("Camera Preview", frame)

        cv2.waitKey(1)
        
        time.sleep(0.03) # 30fps

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    share_memory_base_name = "camera_to_comfy"

    cap = cv2.VideoCapture(0)

    resolutions = [
        (1920, 1080),  # 1080p
        (1080, 1920),  # 1080p
        (1280, 720),   # 720p
        (720, 1280),   # 720p
        (640, 480),    # VGA
        (480, 640),    # VGA
        (320, 240),    # QVGA
        (240, 320),    # QVGA
    ]

    supported_resolutions = get_supported_resolutions(cap, resolutions)

    if not supported_resolutions:
        supported_resolutions = resolutions

    selected_resolution_str = select_resolution(supported_resolutions)
    
    width = 0
    height = 0

    if selected_resolution_str:
        
        selected_resolution = [int(x) for x in selected_resolution_str.split('x')]
        
        print(f"selected: {selected_resolution[0]}x{selected_resolution[1]}")
        width = selected_resolution[0]
        height = selected_resolution[1]
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, selected_resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, selected_resolution[1])
    else:
        print("not seleted")
        cap.release()
        exit()
    
    image_data_producer_by_camera(cap, share_memory_base_name)

