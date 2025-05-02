# ComfyUI_UploadToWebHookPushover <br>
Thanks to Jerryswap UploadToWebhook customnode which I could use as base code for the pushover node.
[![GitHub stars](https://img.shields.io/github/stars/jerrywap/ComfyUI_UploadToWebHookHTTP?style=social)](https://github.com/jerrywap/ComfyUI_UploadToWebhookHTTP/stargazers)



![ComfyUI Node](node1.png)

A custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that allows you to **send generated image(s) ** directly to Pushover, you can also choose only to get a notifycation. Videos aren't supported.

---

## ✨ Features

- 🔗 Upload a single image (from image sequence) with your pushover notification (optional)
- 📦 Includes additional message text (prompt for example)

---

## 🔧 Installation

1. Clone or download this repo into your `ComfyUI/custom_nodes` directory:

```
cd /workspace/ComfyUI/custom_nodes
git clone https://github.com/MijnSpam/ComfyUI_UploadToWebhookPushOver.git
```

2. Install dependencies:

```
cd ComfyUI_UploadToWebHook
bash install.sh
This part can fail with pip env but just check if it runs without doing the packages install.
```

3. Restart ComfyUI (or use the **Reload Custom Nodes** button if available).
4. Refesh browser.

---

## 🧩 How to Use

In Pushover.net create an application token and paste this into your Token field.
Optional, edit default value in __init__.py (line 18)
Optional: Create a delivery group if you want to be flexible in notifying devices. _(then you only need to edit in pushover instead of changing userkeys)_
In User field, enter specific device key **or** add group key.

In ComfyUI:

1. Drag your image output (e.g., from `VAE Decode`) to the **Send To Http Webhook** node.
![ComfyUI Node](node2.png)
2. Configure:
    - `webhook_url`: default is correct.
    - `token`: the pushover app token
    - `user`: Your user OR group key.
---

## 🖼️ UI Example

![ComfyUI Node](node1.png)

---



## 📁 Folder Structure

```
ComfyUI_UploadToWebHookPushOver/
├── __init__.py
├── requirements.txt
└── install.sh
```

---

## 🧑‍💻 Contributing

Pull requests and feature ideas are welcome!  
Feel free to fork and create a PR.

---

## 📄 License

This project is licensed under the MIT License.  
See [LICENSE](./LICENSE) for details.
