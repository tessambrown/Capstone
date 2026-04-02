
import time
import random
import re
from io import BytesIO
from typing import List, Optional, Dict
from backend.errors import appError

import requests
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract 

class fetchImage:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.apiframe.pro"

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.api_key
            }
    
    # Watermark detection helpers

    def _pil_from_url(self, url: str, timeout: int = 20) -> Image.Image:
        # conver the url into a pil image
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return Image.open(BytesIO(resp.content)).convert("RGB")
    
    def _preprocess_for_ocr(self, crop: Image.Image) -> Image.Image:
        # translate cropped image corners into greyscale so it's easier to detect text
        # upscale if crop is small
        w, h = crop.size
        if w < 300 or h < 300:
            scale = max(300 / w, 300 / h)
            crop = crop.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        gray = ImageOps.grayscale(crop)
        enhanced = ImageOps.autocontrast(gray)
        sharpened = enhanced.filter(ImageFilter.SHARPEN)
        return sharpened
    
    # specfically focus on the corners because that's generally where watermarks live
    def _crop_corners(self, img: Image.Image, frac: float = 0.08) -> Dict[str, Image.Image]:
        # crop the corners and return the four coners by width/height
        w, h = img.size
        th = max(1, int(h * frac))  # thickness for top/bottom strips
        tw = max(1, int(w * frac))  # thickness for left/right strips
        return {
            "top":    img.crop((0,      0,      w,  th)),
            "bottom": img.crop((0,      h - th, w,  h)),
            "left":   img.crop((0,      0,      tw, h)),
            "right":  img.crop((w - tw, 0,      w,  h)),
    }

    def _image_has_corner_text(
            self,
            img: Image.Image,
            corner_frac: float = 0.08,
            min_chars: int = 4,
            ocr_config: str = "--psm 11",
            debug: bool = False
    ) -> bool:
        w, h = img.size
        # Only check the four small corner patches, not full edge strips
        corner_size_w = max(1, int(w * corner_frac))
        corner_size_h = max(1, int(h * corner_frac))
        
        corners = {
            "top-left":     img.crop((0,         0,          corner_size_w, corner_size_h)),
            "top-right":    img.crop((w - corner_size_w, 0,  w,             corner_size_h)),
            "bottom-left":  img.crop((0,         h - corner_size_h, corner_size_w, h)),
            "bottom-right": img.crop((w - corner_size_w, h - corner_size_h, w, h)),
        }

        for name, crop in corners.items():
            gray = ImageOps.grayscale(crop)
            boosted = ImageEnhance.Contrast(gray).enhance(2.0)
            boosted = ImageOps.autocontrast(boosted)
            boosted = boosted.filter(ImageFilter.SHARPEN)

            raw = pytesseract.image_to_string(boosted, config="--psm 11")
            cleaned = re.sub(r"[^A-Za-z0-9]+", "", raw)

            # Filter out single-char repeats and short noise
            if len(set(cleaned)) < 2 or len(cleaned) < min_chars:
                if debug:
                    print(f"[{name}] SKIP | cleaned: '{cleaned}'")
                continue

            if debug:
                print(f"[{name}] raw: {repr(raw)} | cleaned: '{cleaned}'")

            return True

        return False    
    
    def pickFirstTextFreeURL(
            self,
            image_urls: List[str],
            corner_frac: float = 0.10,
            min_chars: int = 3,
            ocr_config: str = "--psm 11",
            debug: bool = False,
    ) -> Optional[str]:
        
        # return the first text free image
        for url in image_urls:
            try:
                print("trying to find text in", url)
                img = self._pil_from_url(url)
                has_text = self._image_has_corner_text (
                    img, 
                    corner_frac=corner_frac,
                    min_chars=min_chars,
                    ocr_config=ocr_config,
                    debug=debug
                )

                print("Does the image have corner text", has_text)

                if debug:
                    print(f"[CHECK] {'WATERMARK' if has_text else 'CLEAN   '} -> {url}")

                # return the url of the first free url
                if not has_text:
                    return url
                
            except Exception as e:
                if debug:
                    raise appError("Skipping URL due to error", 500)
                continue
        return None

    # check the status of the image
    def getImage(self, task_id, max_wait_seconds=180, corner_frac=0.10, min_chars=3, debug=True):
        print("Getting the image")
        url = f"{self.base_url}/fetch"
        start = time.time()
        delay = 1.5  # start small

        while True:
            # timeout protection, it it times out return None
            if time.time() - start > max_wait_seconds:
                return None 
            
            # ask the API for status, stops after 15sec
            resp = requests.post(
                url,
                headers=self.headers,
                json={"task_id": task_id},
                timeout=15
            )
            # return a HTTP error and parse json
            resp.raise_for_status()
            data = resp.json()

            # check the status of the image
            status = data.get("status")

            # if the image is finished return the first of four links
            if status == "finished":
                image_urls = data.get("image_urls", [])
                image_url = image_urls[0]
                return image_url if image_url else None

            # if fetching the image failed return None
            if status in ("failed", "error"):
                return None

            # wait before trying again
            # avoid hitting the API at perfectly timed intervals
            time.sleep(delay + random.uniform(0, 0.4))
            # each time it delays it multiples by 1.4sec and caps at 8sec (exponetial backoff)
            delay = min(delay * 1.4, 8)

    # def getImageTextFree(
    #         self,
    #         task_id: str,
    #         max_wait_seconds: int = 180,
    #         corner_frac: float = 0.22,
    #         min_chars: int = 3,
    #         debug: bool = False,
    #         regenerate_fn: Optional[Callable[[], str]] = None,
    # ) -> Optional[str]:
        
    #     urls = self.getImage(task_id, max_wait_seconds=max_wait_seconds)
    #     if not urls:
    #         return None
        
    #     chosen = self.pickFirstTextFreeURL(
    #         urls,
    #         corner_frac=corner_frac,
    #         min_chars=min_chars,
    #         debug=debug
    #     )

    #     # return the first text free image
    #     if chosen:
    #         return chosen
        
    #     # if we can't regenerate, return none
    #     if regenerate_fn is None:
    #         if debug:
    #             raise appError("All of the candidates had corner text", 500)
    #         return None

    #     return None        
