import re
import json
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
    
class IOUtils:

    @staticmethod
    def save_score_details(music_score, output_dir):
        file_name = IOUtils.safe_filename(music_score.title, "json")
        output_file = output_dir / file_name
        # Create folder if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        # Get the music score as Json
        json_str = json.dumps(music_score.to_json(), cls=CustomEncoder, indent=2)
        # Save the file
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(json_str, f, indent=2)

    @staticmethod
    def safe_filename(name: str, extension: str, max_length: int = 255) -> str:
        # Replace spaces with underscores
        name = name.replace(" ", "_")
        # Remove invalid characters (Windows + Unix)
        name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', name)
        # Remove leading/trailing dots and underscores
        name = name.strip("._")
        # Collapse multiple underscores
        name = re.sub(r'_+', '_', name)
        # Limit length
        return name[:max_length] + f".{extension}"
