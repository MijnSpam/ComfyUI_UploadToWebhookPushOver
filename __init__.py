import os
import json
import numpy as np
import requests
import base64
from PIL import Image
import folder_paths

# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_typ = AnyType("*")
def load_env_variable(file_path, variable_name):
    # Read the .env file
    try:
      with open(file_path, 'r') as env_file:
          for line in env_file:
              key_value = line.strip().split('=')
              if len(key_value) == 2 and key_value[0] == variable_name:
                  return key_value[1].strip()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the .env file: {e}")
    # Return None if the variable is not found
    return None

class UploadToPushOver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "connect_anything": (any_typ,),
                "webhook_url": ("STRING", {"default": "https://api.pushover.net/1/messages.json"}),
                "title": ("STRING", {"default": "Comfy push title"}),
                "priority": ("INT", {"default": 0, "lowest": -2, "max": 2}),
                "sound":(["pushover", "bike", "bugle", "cashregister", "classical", "cosmic", "falling", "gamelan", "incoming", "intermission", "magic", "mechanical", "pianobar", "siren", "spacealarm", "tugboat", "alien", "climb", "persistent", "echo", "updown", "vibrate", "none"],),
               # "attachment_type":("STRING", {"default": "image/png"}),
                "attach_image": ("BOOLEAN", {"default": True}),
                "prompt_id": ("STRING", {"default": "Will be your pushover message, when empty: Workflow ready", "multiline": True})
            },
            "optional": {
                "images": ("IMAGE",),
                "token": ("STRING", {"default": "enter your application key"}),
                "user": ("STRING", {"default": "enter user or group key"}),
                "use_stored_credentials": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = (any_typ,)
    OUTPUT_NODE = True
    CATEGORY = "Notification"
    FUNCTION = "generate_and_upload_image"
    
    def generate_and_upload_image(
        self,
        connect_anything,
        webhook_url: str,
        use_stored_credentials:False,
        token: str,
        title: str,
        user: str,
        priority: int,
        sound: str,
        attach_image:True,
        prompt_id: str = "",
        images: str = "",
    ):
        output_dir = folder_paths.get_temp_directory()
        #output_dir = folder_paths.get_output_directory() if save_image else folder_paths.get_temp_directory()
        # above is old line from original webhook creator
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
        ## if stored credentials are used load from file else use input fields.
        if use_stored_credentials:
            env_file_path = './.env'
            apptoken = load_env_variable(env_file_path, 'apptoken')
            usertoken = load_env_variable(env_file_path, 'usertoken')
            parsed_data["token"] = apptoken
            parsed_data["user"] = usertoken
            print(f"env loading: {apptoken}")
        else:
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
        else:
            response = requests.post(
                webhook_url,
                data=parsed_data
            )
        # Response output
        if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
            print("✅ Successfully uploaded to Pushover.")
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