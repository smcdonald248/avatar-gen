"""
Author: Stephen McDonald
Description: Quick and simple SDXL image generator for a specific person
"""
import argparse
import base64
import io
import json
import os
import random
import string
import sys
from typing import Any

import requests
import PIL.Image
from dotenv import load_dotenv


load_dotenv()
OCTOAI_TOKEN: str = os.getenv("OCTOAI_API_TOKEN")

def random_suffix(length: int = 8) -> str:
    """ return a random string with a given length """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def encode_b64(path: str, image_name: str) -> str:
    """ base64 encode the data content of an image file """
    with open(f"{path}/{image_name}", "rb") as image_file:
        image_data = image_file.read()

    return base64.b64encode(image_data).decode('ascii')

def query(url: str, data: str) -> dict[str, Any]:
    """ query an OctoAI endpoint """
    headers: dict[str, str] = {
        "Authorization": f"Bearer {OCTOAI_TOKEN}",
        "Content-Type": "application/json"
    }
    res = requests.post(url, data=data, headers=headers, timeout=30)

    if res.status_code == 200:
        return json.loads(res.text)
    else:
        print(f"ERROR: status code: {res.status_code}, message: {res.text}")
        sys.exit(1)

def main(args: argparse.Namespace) -> None:
    """ main entry point """

    SDXL_URL: str = "https://image.octoai.run/generate/sdxl"
    ADETAILER_URL: str = "https://image.octoai.run/adetailer" 
    subject_name: str = args.subject_name
    descriptor: str = args.descriptor
    image_path: str = f"images/{args.subject_name}"
    output_path: str = f"output/{subject_name}"
    base_output_name: str = f"{output_path}/base_result-{subject_name}-{random_suffix()}-%s.jpg"
    image_names: list[str] = os.listdir(image_path)
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass

    b64_images = [encode_b64(image_path, image) for image in image_names]
    payload: dict[str, Any] = {
        "prompt": f"a digital avatar of a {descriptor} {subject_name}, <lora:tokenframe1> tokenfram\
            e, rusted metal themed frame, distopian future, barren landscape, dust in the air, rays\
             of sunshine through whisps of pollution, black trenchcoat, opaque steampunk goggles, d\
            irty, rugged, wind burn, apocalyptic, sepia, dusk",
        "negative_prompt": "(asymmetry, worst quality, low quality,), open mouth, Blurry photo, dis\
            tortion, low-res, bad quality",
        # "loras": {
        #     "<custom asset output from octoai account>": 1.0 # game-avatar-token-frame from CivitAI
        #     },
        "checkpoint": "crystal-clear",
        "width": 1024,
        "height": 1024,
        "num_images": 4,
        "sampler": "K_EULER_ANCESTRAL",
        "steps": 20,
        "cfg_scale": 7,
        "transfer_images": {subject_name: b64_images},
    }
    response: dict[str, Any] = query(SDXL_URL,json.dumps(payload))

    if "images" in response:
        gen_image_names: list[str] = []
        for i, img_info in enumerate(response["images"]):
            img_bytes: bytes = base64.b64decode(img_info["image_b64"])
            img: PIL.Image = PIL.Image.open(io.BytesIO(img_bytes))
            img.load()
            img.save(base_output_name % i)
            gen_image_names.append(base_output_name % i)
    else:
        print("ERROR: images were not successfully generated")
        print(f"Photo Merge Response: {response}")

    for i in gen_image_names:
        ad_payload: dict[str, Any] = {
            "prompt":"ultra high quality, photorealism, attractive",
            "negative_prompt": "worst quality, bad face, drawing, unrealistic, ugly face, animated",
            "init_image": encode_b64(".",i),
            "detector": "face_yolov8n",
            "inpainting_base_model": "sdxl",
            "strength": 0.4,
            "cfg_scale": 8
        }
        ad_image: str = query(ADETAILER_URL, json.dumps(ad_payload))

        img_bytes: bytes = base64.b64decode(ad_image["image_b64"])
        img = PIL.Image.open(io.BytesIO(img_bytes))
        img.load()
        img.save(f"{i.replace("base","adetailer")}")


def parse_args() -> argparse.Namespace:
    """ parse cli args """
    parser = argparse.ArgumentParser()
    parser.add_argument("subject_name")
    parser.add_argument("-d", "--descriptor",
                        help="Additional subject descriptors (e.g. gender) (Default: 'person')",
                        default="person")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())