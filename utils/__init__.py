import os
from .textwrap_local import fw_fill, fw_wrap
from .ocr_model import OCRModel
from .layout_model import LayoutAnalyzer
from .gui import GradioApp
from PIL import Image, ImageDraw, ImageFont
from loguru import logger
import yaml
from string import Template

__all__ = ["fw_fill", "fw_wrap", "OCRModel", "LayoutAnalyzer"]

def load_config(base_config_path, override_config_path):
    def load_and_expand(path):
        with open(path, 'r') as file:
            content = file.read()
            expanded = Template(content).safe_substitute(os.environ)
            return yaml.safe_load(expanded)

    base_config = load_and_expand(base_config_path)
    final_config = base_config

    def update(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    if os.path.exists(override_config_path):
        override_config = load_and_expand(override_config_path)
        final_config = update(base_config, override_config)

    return final_config


def draw_text(draw: ImageDraw.ImageDraw, processed_text, current_fnt, font_size, width, ygain):
    y = 0
    if isinstance(processed_text, str):
        processed_text = processed_text.split('\n')
    first = len(processed_text) > 1
    for l in processed_text:
        words = l.split(" ")
        words_length = sum(draw.textlength(w, font=current_fnt) for w in words)
        if first: words_length += 40
        space_length = (width - words_length) / (len(words))
        if (space_length > 40):
            logger.debug(f"Space length too wide, Setting to : {space_length}")
            space_length = font_size/2.4
        elif space_length < 0:
            space_length = 0
        x = 0
        if first: x+= 40
        for word in words:
            logger.debug(f"Drawing word at {x}, {y}: \n {word}")
            draw.text((x, y), word, font=current_fnt, fill="black")
            x += draw.textlength(word, font=current_fnt) + space_length
        y += ygain
        first = False