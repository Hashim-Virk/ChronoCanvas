import os
import json
import time
import math
import random
import urllib.request
import urllib.parse
from datetime import datetime

# AWS Boto3 import with graceful fallback for local standalone testing
try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


class ChronoCanvasAgent:
    """
    ChronoCanvas Autonomous Creative Agent.
    Fetches ambient weather & astronomical data, calculates daily mood vectors,
    generates themed digital artwork, micro-poetry, and dynamic HSL color themes,
    and stores output in AWS S3 / DynamoDB (or local fallback storage).
    """

    def __init__(self, s3_bucket=None, dynamodb_table=None):
        self.s3_bucket = s3_bucket or os.environ.get("S3_BUCKET_NAME", "chronocanvas-creations")
        self.table_name = dynamodb_table or os.environ.get("DYNAMODB_TABLE", "ChronoCanvas-Gallery")
        self.local_storage_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(self.local_storage_dir, exist_ok=True)
        os.makedirs(os.path.join(self.local_storage_dir, "images"), exist_ok=True)

    def fetch_weather(self, lat=40.7128, lon=-74.0060):
        """Fetches current weather and astronomical phase from Open-Meteo API."""
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=sunrise,sunset&timezone=auto"
            req = urllib.request.Request(url, headers={'User-Agent': 'ChronoCanvasAgent/1.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                current = data.get("current_weather", {})
                weathercode = current.get("weathercode", 0)
                temp_c = current.get("temperature", 20.0)

                return {
                    "temperature_c": temp_c,
                    "temperature_f": round(temp_c * 9/5 + 32, 1),
                    "weather_code": weathercode,
                    "condition": self._interpret_weather_code(weathercode),
                    "windspeed": current.get("windspeed", 10.0),
                    "time": current.get("time", datetime.utcnow().isoformat())
                }
        except Exception as e:
            print(f"[ChronoCanvasAgent] Weather fetch note: using ambient fallback ({e})")
            now = datetime.now()
            return {
                "temperature_c": 22.5,
                "temperature_f": 72.5,
                "weather_code": 0,
                "condition": "Clear Sky & Gentle Breeze",
                "windspeed": 8.4,
                "time": now.isoformat()
            }

    def _interpret_weather_code(self, code):
        mapping = {
            0: "Clear Sky & Sunlit Horizons",
            1: "Mainly Clear Amber Atmosphere",
            2: "Partly Cloudy Whispering Vapors",
            3: "Overcast Obsidian Shadows",
            45: "Mystic Rolling Fog",
            48: "Rime Frost Emerald Mist",
            51: "Drizzling Neon Raindrops",
            61: "Shattered Rain & Silver Echoes",
            71: "Crisp Glacial Snowflakes",
            80: "Torrential Tempest Storm",
            95: "Electric Thunderstorms & Celestial Lightning"
        }
        return mapping.get(code, "Serene Atmospheric Balance")

    def derive_mood_vector(self, weather_data):
        """Calculates solar phase, dominant mood, and color scheme based on time and weather."""
        now = datetime.now()
        hour = now.hour

        if 5 <= hour < 8:
            phase = "Dawn Awakening"
            mood = "Hopeful, Translucent, Rising"
            base_hue = 35  # Gold / Amber
        elif 8 <= hour < 17:
            phase = "Solar Zenith"
            mood = "Vibrant, Energetic, Radiant"
            base_hue = 200  # Azure / Deep Cyan
        elif 17 <= hour < 20:
            phase = "Dusk Duskscape"
            mood = "Melancholic, Retrograde, Glowing"
            base_hue = 280  # Twilight Violet / Rose
        else:
            phase = "Nocturnal Quietude"
            mood = "Mystical, Deep Cosmic, Silent"
            base_hue = 240  # Indigo / Midnight Blue

        # Adjust hue with weather code modulation
        weather_code = weather_data.get("weather_code", 0)
        hue_shift = (weather_code * 7) % 60
        primary_hue = (base_hue + hue_shift) % 360

        palette = [
            f"hsl({primary_hue}, 85%, 60%)",
            f"hsl({(primary_hue + 45) % 360}, 75%, 50%)",
            f"hsl({(primary_hue + 180) % 360}, 90%, 65%)",
            f"hsl({(primary_hue + 240) % 360}, 40%, 15%)"
        ]

        return {
            "phase": phase,
            "mood": mood,
            "primary_hue": primary_hue,
            "palette": palette,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
        }

    def generate_poem_and_title(self, weather_data, mood_vector):
        """Synthesizes atmospheric poem, lore snippet, and title."""
        condition = weather_data.get("condition", "Serene Atmosphere")
        phase = mood_vector.get("phase", "Solar Zenith")
        temp_f = weather_data.get("temperature_f", 72)

        titles = [
            f"Echoes of the {condition.split()[0]} Horizon",
            f"Solitude in {phase}",
            f"Vapors of the {temp_f}°F Twilight",
            f"Chronos & The {condition.split()[-1]} Realm",
            f"Luminous Drift: {phase}"
        ]

        stanzas = [
            f"Across the quiet canopy of {phase.lower()},\nWhere {condition.lower()} weaves through silent air,\nThe horizon holds a pulse of celestial light,\nUnbroken by the passage of hours.",
            f"Whispering currents at {temp_f}°F awaken the glass,\nA canvas drawn without human hands,\nWhere light meets shadow in harmonious resonance,\nAnd time lingers before turning the page.",
            f"Shadows tilt toward the distant perimeter,\nCaptured in the quiet pulse of an always-on observer,\nEach frame a testament to the breathing earth,\nCaptured while the world slumbers."
        ]

        title = random.choice(titles)
        poem = "\n\n".join(stanzas)
        lore = f"Synthesized during {phase} under {condition}. Environmental temperature recorded at {temp_f}°F."

        return {
            "title": title,
            "poem": poem,
            "lore": lore
        }

    def generate_image_url(self, title, mood_vector, weather_data):
        """Generates high-resolution photorealistic celestial/planetary artwork URL."""
        condition = weather_data.get("condition", "Atmospheric landscape")
        phase = mood_vector.get("phase", "Dawn")
        mood = mood_vector.get("mood", "Vibrant")

        celestial_concepts = [
            "breathtaking photorealistic astronomical photography of detailed full moon, glowing lunar surface craters, deep space cosmic stars",
            "majestic photorealistic celestial view of ringed planet Saturn rising above atmospheric cloud horizon, ultra realistic 8k space telescope photo",
            "stunning photorealistic crescent moon over ethereal atmospheric clouds, celestial cosmic nebulae, photorealistic 8k render",
            "photorealistic deep space cosmos showing distant planets, glowing astronomical dust, Hubble telescope photography style",
            "photorealistic planetary horizon with glowing lunar light, deep space stellar atmosphere, photorealistic 8k celestial photo"
        ]
        chosen_concept = random.choice(celestial_concepts)

        prompt_str = f"{chosen_concept}, during {phase}, under {condition}, {mood} atmosphere, photorealistic 8k resolution, cinematic space photography, hyperdetailed"
        encoded_prompt = urllib.parse.quote(prompt_str)

        # High-res generative visual URL via Pollinations AI generator
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&seed={random.randint(1000, 99999)}&nologo=true"
        return image_url, prompt_str

    def execute_autonomous_cycle(self, custom_location="New York, USA"):
        """Runs full autonomous creation cycle and persists output."""
        print("[ChronoCanvasAgent] Starting autonomous creation cycle...")

        weather = self.fetch_weather()
        mood = self.derive_mood_vector(weather)
        creative_text = self.generate_poem_and_title(weather, mood)
        image_url, prompt_str = self.generate_image_url(creative_text["title"], mood, weather)

        canvas_id = f"canvas-{int(time.time())}"
        record = {
            "canvas_id": canvas_id,
            "created_at": mood["timestamp"],
            "epoch_timestamp": int(time.time()),
            "location": custom_location,
            "title": creative_text["title"],
            "poem": creative_text["poem"],
            "lore": creative_text["lore"],
            "weather": weather,
            "mood": mood,
            "prompt": prompt_str,
            "image_url": image_url
        }

        # Save to local JSON history file
        self._save_to_local_history(record)

        # Attempt AWS persistence if boto3 / credentials available
        self._persist_to_aws(record)

        print(f"[ChronoCanvasAgent] Autonomous cycle complete! Created: {record['title']} ({canvas_id})")
        return record

    def _save_to_local_history(self, record):
        history_path = os.path.join(self.local_storage_dir, "history.json")
        history = []
        if os.path.exists(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []

        history.insert(0, record)
        # Keep latest 50 creations
        history = history[:50]

        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def _persist_to_aws(self, record):
        if not HAS_BOTO3:
            return

        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(self.table_name)
            table.put_item(Item=record)
            print(f"[ChronoCanvasAgent] Persisted record to AWS DynamoDB table: {self.table_name}")
        except Exception as e:
            print(f"[ChronoCanvasAgent] DynamoDB persistence note (using local fallback): {e}")

        try:
            s3 = boto3.client("s3")
            s3_key = f"canvases/{record['canvas_id']}.json"
            s3.put_object(
                Bucket=self.s3_bucket,
                Key=s3_key,
                Body=json.dumps(record, indent=2),
                ContentType="application/json"
            )
            print(f"[ChronoCanvasAgent] Persisted record JSON to AWS S3: s3://{self.s3_bucket}/{s3_key}")
        except Exception as e:
            print(f"[ChronoCanvasAgent] S3 persistence note (using local fallback): {e}")

    def get_latest_canvas(self):
        """Retrieves the latest autonomous creation."""
        history_path = os.path.join(self.local_storage_dir, "history.json")
        if os.path.exists(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    if history:
                        return history[0]
            except Exception:
                pass
        return self.execute_autonomous_cycle()

    def get_history(self):
        """Retrieves full creation history."""
        history_path = os.path.join(self.local_storage_dir, "history.json")
        if os.path.exists(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return [self.get_latest_canvas()]


if __name__ == "__main__":
    agent = ChronoCanvasAgent()
    latest = agent.execute_autonomous_cycle()
    print("Generated Canvas output summary:")
    print(json.dumps(latest, indent=2))
