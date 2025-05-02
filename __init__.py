import os
import json
import numpy as np
import requests
import base64
from PIL import Image
import folder_paths

class UploadToPushOver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "webhook_url": ("STRING", {"default": "https://api.pushover.net/1/messages.json"}),
                "token": ("STRING", {"default": "enter your application key"}),
                "user": ("STRING", {"default": "enter user or group key"}),
                "title": ("STRING", {"default": ""}),
                "priority": ("INT", {"default": 0, "lowest": -2, "max": 2}),
                "sound":(["pushover", "bike", "bugle", "cashregister", "classical", "cosmic", "falling", "gamelan", "incoming", "intermission", "magic", "mechanical", "pianobar", "siren", "spacealarm", "tugboat", "alien", "climb", "persistent", "echo", "updown", "vibrate", "none"],),
                "attachment_type":("STRING", {"default": "image/png"}),
                "attach_image": ("BOOLEAN", {"default": True}),
                "prompt_id": ("STRING", {"default": "Will be your pushover message, when empty: Workflow ready", "multiline": True})
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True
    CATEGORY = "Notification"
    FUNCTION = "generate_and_upload_image"

    def generate_and_upload_image(
        self,
        images,
        webhook_url: str,
        token: str,
        title: str,
        user: str,
        priority: int,
        sound: str,
        attachment_type: str,
        attach_image: True,
        save_image=True,
        prompt_id: str = "",
    ):
        output_dir = folder_paths.get_output_directory() if save_image else folder_paths.get_temp_directory()

        (
            full_output_folder,
            filename,
            counter,
            subfolder,
            _,
        ) = folder_paths.get_save_image_path("final", output_dir)

        parsed_data = {}

        if prompt_id:
            parsed_data["message"] = prompt_id
        else:
            parsed_data["message"] = "Workflow ready" # message can't be empty, pushover wont accept it.
        parsed_data["token"] = token
        parsed_data["user"] = user
        parsed_data["title"] = title
        parsed_data["priority"] = priority
        parsed_data["sound"] = sound


        if len(images) == 1:
            single_file_path = os.path.join(full_output_folder, f"{filename}_.png")
            single_image = 255.0 * images[0].cpu().numpy()
            single_image_pil = Image.fromarray(single_image.astype(np.uint8))
            single_image_pil.save(single_file_path)

            with open(single_file_path, "rb") as file:
                encoded_image = base64.b64encode(file.read()).decode("utf-8")
                if attach_image:
                    parsed_data["attachment_base64"] = encoded_image 
                response = requests.post(
                    webhook_url,
                    data=parsed_data
                )

        # Response output
        if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
            print("✅ Successfully uploaded to Webhook.")
            print(f"Response Code: {response.status_code}")
            print(f"Response Text: {response.text}")
        else:
            print(f"❌ Failed to upload. Status code: {response.status_code} - {response.text}")

        return ("Uploading Completed",)


NODE_CLASS_MAPPINGS = {
    "UploadToPushOver": UploadToPushOver,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UploadToPushOver": "Send To PushOver",
}