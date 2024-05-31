import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2
from skimage.metrics import structural_similarity as ssim

# Match Threshold
THRESHOLD = 85

def browsefunc(ent, img_label):
    filename = askopenfilename(filetypes=[
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ])
    if filename:
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
        display_image(img_label, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:  # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp')
            img_name = f"./temp/test_img{sign}.png"
            cv2.imwrite(filename=img_name, img=frame)
            print(f"{img_name} written!")
            break
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, img_label, sign=1):
    filename = os.getcwd() + f'/temp/test_img{sign}.png'
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
        display_image(img_label, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure: Signatures Do Not Match",
                             f"Signatures are {result:.2f}% similar!!")
    else:
        messagebox.showinfo("Success: Signatures Match",
                            f"Signatures are {result:.2f}% similar!!")
    return True

def match(path1, path2):
    img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    similarity_value = ssim(img1, img2) * 100
    return similarity_value

def display_image(label, path):
    img = Image.open(path)
    img = img.resize((150, 150), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")

uname_label = tk.Label(root, text="Compare Two Signatures:", font=10)
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Signature 1", font=10)
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=150, y=120)

img1_label = tk.Label(root)
img1_label.place(x=150, y=150)

img1_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image1_path_entry, img_label=img1_label, sign=1))
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry, img_label=img1_label))
img1_browse_button.place(x=400, y=140)

img2_message = tk.Label(root, text="Signature 2", font=10)
img2_message.place(x=10, y=250)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.place(x=150, y=240)

img2_label = tk.Label(root)
img2_label.place(x=150, y=270)

img2_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image2_path_entry, img_label=img2_label, sign=2))
img2_capture_button.place(x=400, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image2_path_entry, img_label=img2_label))
img2_browse_button.place(x=400, y=260)

compare_button = tk.Button(
    root, text="Compare", font=10, command=lambda: checkSimilarity(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get()))
compare_button.place(x=200, y=320)

root.mainloop()
