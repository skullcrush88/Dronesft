import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2, os, json
from core.router import handle_command
from core.state import telemetry
import tkintermapview

def launch_gui():
    root = tk.Tk()
    root.title("SkyMindOS v4+")
    root.geometry("1400x800")

    cap = [None]
    current_mode = ["camera"]
    map_widget = tkintermapview.TkinterMapView(root, width=400, height=300, corner_radius=0)
    map_widget.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    lmain = tk.Label(root)
    lmain.grid(row=0, column=0, columnspan=2)

    def send(cmd, params={}):
        try:
            handle_command(json.dumps({"command": cmd, "params": params}))
        except Exception as e:
            print("[GUI ERROR]", e)

    def show_image(frame):
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)

    def update_video():
        if cap[0] and current_mode[0] in ["camera", "video"]:
            ret, frame = cap[0].read()
            if ret: show_image(frame)
        lmain.after(30, update_video)

    def update_map():
        gps = telemetry.get("gps", [0, 0])
        map_widget.set_position(gps[0], gps[1])
        map_widget.set_marker(gps[0], gps[1], text="Drone")
        root.after(3000, update_map)

    def open_camera():
        if cap[0]: cap[0].release()
        cap[0] = cv2.VideoCapture(0)
        current_mode[0] = "camera"

    def open_video():
        path = filedialog.askopenfilename(filetypes=[("Video", "*.mp4;*.avi")])
        if path:
            if cap[0]: cap[0].release()
            cap[0] = cv2.VideoCapture(path)
            current_mode[0] = "video"

    def open_image():
        path = filedialog.askopenfilename(filetypes=[("Image", "*.jpg;*.png")])
        if path and os.path.exists(path):
            img = cv2.imread(path)
            show_image(img)
            current_mode[0] = "image"

    update_video()
    update_map()

    control = tk.Frame(root)
    control.grid(row=1, column=2, sticky="nsew")

    tk.Button(control, text="Live Camera", command=open_camera).pack(pady=2)
    tk.Button(control, text="Load Video", command=open_video).pack(pady=2)
    tk.Button(control, text="Load Image", command=open_image).pack(pady=2)

    tk.Label(control, text="Altitude:").pack()
    alt_entry = tk.Entry(control)
    alt_entry.insert(0, "5")
    alt_entry.pack()

    tk.Button(control, text="🛫 Takeoff", command=lambda: send("takeoff", {"altitude": float(alt_entry.get())})).pack(pady=2)
    tk.Button(control, text="🛬 Land", command=lambda: send("land")).pack(pady=2)
    tk.Button(control, text="🛑 Disarm", command=lambda: send("disarm")).pack(pady=2)
    tk.Button(control, text="✈️ Set Mode", command=lambda: send("set_mode", {"mode": "GUIDED"})).pack(pady=2)

    features = [
        ("Start Analysis", "analyze", {}),
        ("Geo-Fence", "geofence", {"zone": "A"}),
        ("Battery Trigger", "trigger", {"battery_threshold": 11.0}),
        ("Set Param", "param", {"name": "P1", "value": 42}),
        ("Mode: AUTO", "set_mode", {"mode": "AUTO"}),
        ("Altitude 10", "takeoff", {"altitude": 10}),
        ("Battery <10.5", "trigger", {"battery_threshold": 10.5}),
        ("Waypoint", "mission", {"steps":[{"command":"takeoff"},{"command":"land"}]}),
        ("Disarm Now", "disarm", {}),
        ("Upload CFG", "param", {"name": "UPLOAD", "value": 1}),
        ("Download Logs", "analyze", {}),
        ("Return RTL", "set_mode", {"mode":"RTL"}),
        ("Hover", "set_mode", {"mode": "LOITER"}),
        ("AI Plan", "analyze", {}),
        ("PX4 Sync", "param", {"name":"SYNC", "value":1}),
        ("Reset Mission", "mission", {"steps":[]}),
        ("Enable AI", "param", {"name":"AI", "value":1}),
        ("Disable AI", "param", {"name":"AI", "value":0}),
        ("Live Track", "analyze", {}),
        ("Heartbeat", "trigger", {"battery_threshold": 10.0})
    ]

    adv = tk.Frame(root)
    adv.grid(row=2, column=0, columnspan=3)

    for i, (label, cmd, param) in enumerate(features):
        tk.Button(adv, text=label, width=25, command=lambda c=cmd, p=param: send(c, p)).grid(row=i//3, column=i%3, padx=4, pady=2)

    root.mainloop()
