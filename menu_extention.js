
import { app } from '../../scripts/app.js'


app.showDialog = async function (str) {
    this.ui.dialog.show(`<span style="color: white; ">${str}</span>`)
}

function getLocalComfyUIServerUrl() {
    let api_host = `${window.location.hostname}:${window.location.port}`
    // console.log("port:", window.location.port)
    let api_base = ''
    let url = `${window.location.protocol}//${api_host}${api_base}`
    return url
}
export async function requestServer(path, json_obj_data) {
    let base_url = getLocalComfyUIServerUrl()
    let url = `${base_url}${path}`
    console.log(url)
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_obj_data)
    })
    console.log("response:", res)
    return await res.json()
}

// Add context menu for comfyui
// Start Local Camera
// Stop Local Camera
app.registerExtension({
    name: 'Comfy.XCamera.ui',
    setup() {
        setTimeout(async () => {
            const menus = LGraphCanvas.prototype.getCanvasMenuOptions
            LGraphCanvas.prototype.getCanvasMenuOptions = function () {
                const options = menus.apply(this, arguments)
                options.push(
                    null,
                    {
                        content: `Start Local Camera`,
                        disabled: false,
                        callback: async () => {
                            
                            await app.showDialog("Starting, Wait for a moment...")

                            let response_data = await requestServer('/start_camera', { })

                            console.log(response_data)

                            // await app.showDialog(`${response_data}`)
                        }
                    },
                    {
                        content: `Stop Local Camera`,
                        disabled: false,
                        callback: async () => {
                            
                            await app.showDialog("Stoping, Wait for a moment...")

                            let response_data = await requestServer('/stop_camera', { })
                            console.log(response_data)
                            await app.showDialog(`${response_data}`)
                        }
                    },
                )
                return options
            }
        }, 1100)
    }
})
