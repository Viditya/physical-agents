"""CLI entrypoint — run a provider against a single image and print the result.

Usage:
    python -m prototype.cli --provider gemini --image path/to/image.jpg
    python -m prototype.cli --provider magma  --image path/to/image.jpg \
        --prompt "What objects are visible?"
"""

import argparse
import importlib
import json

from dotenv import load_dotenv

load_dotenv()

PROVIDERS = {
    "gemini": "prototype.providers.gemini_robotics.GeminiRoboticsProvider",
    "magma": "prototype.providers.magma.MagmaProvider",
}


def _load_provider(name: str):
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider '{name}'. Choose from: {list(PROVIDERS)}")
    module_path, class_name = PROVIDERS[name].rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a vision-spatial AI provider against an image."
    )
    parser.add_argument(
        "--provider",
        required=True,
        choices=list(PROVIDERS),
        help="Provider to use.",
    )
    parser.add_argument("--image", required=True, help="Path to the image file.")
    parser.add_argument(
        "--prompt",
        default="Describe this image in detail.",
        help="Prompt to send to the model.",
    )
    args = parser.parse_args()

    provider = _load_provider(args.provider)
    result = provider.describe_image(args.image, args.prompt)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
