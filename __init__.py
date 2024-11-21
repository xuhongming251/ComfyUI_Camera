from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# web extension dir
# dir of menu_extention.js
WEB_DIRECTORY = "."

from aiohttp import web
from server import PromptServer

from . import camera_preview_manager

camera_controller = camera_preview_manager.CameraController()

# extend custom server api for menu "Start Local Camera" click
@PromptServer.instance.routes.post("/start_camera")
async def start_share_server(request):
    
    try:
        camera_controller.start_camera()
    except Exception as e:
        print(f"start camera, exception: {e}")
        return web.json_response(f"failed to start. {e}")
    
    return web.json_response({})

# extend custom server api for menu "Stop Local Camera" click
@PromptServer.instance.routes.post("/stop_camera")
async def start_share_server(request):

    result = camera_controller.stop_camera()
    
    if result:
        return web.json_response("Stoped")
    else:
        return web.json_response("Have Stoped")
