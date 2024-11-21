import os
import sys
import subprocess
import psutil

# control preview capture and processed image
# controle process start and stop
class CameraController:
    def __init__(self):
        self.global_preview_camera_process = None
        self.global_preview_processed_process = None

    def start_child_process(self, py_module_abs_path, args_params=None):
        if args_params is None:
            args_params = []
        args = [sys.executable, py_module_abs_path] + args_params
        return subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def kill_proc_tree(self, pid, including_parent=True):
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                child.terminate()
            psutil.wait_procs(children, timeout=5)
            if including_parent:
                parent.terminate()
                parent.wait(5)
        except psutil.NoSuchProcess:
            pass

    def stop_camera(self):
        if self.global_preview_camera_process or self.global_preview_processed_process:
            if self.global_preview_camera_process:
                self.kill_proc_tree(self.global_preview_camera_process.pid)
                self.global_preview_camera_process = None

            if self.global_preview_processed_process:
                self.kill_proc_tree(self.global_preview_processed_process.pid)
                self.global_preview_processed_process = None

            print("Stopped")
            return True
        else:
            print("No process to stop")
            return False

    def start_camera(self):
        if self.global_preview_camera_process or self.global_preview_processed_process:
            self.stop_camera()

        current_dir = os.path.abspath(os.path.dirname(__file__))

        preview_camera_path = os.path.join(current_dir, "preview_camera.py")
        preview_processed_path = os.path.join(current_dir, "preview_processed.py")

        self.global_preview_camera_process = self.start_child_process(preview_camera_path)
        self.global_preview_processed_process = self.start_child_process(preview_processed_path)

        print("Camera started")

if __name__ == "__main__":
    controller = CameraController()
    controller.start_camera()  # Start the camera
    # controller.stop_camera()  # Uncomment to stop the camera
