import click
import os
from utils import generate_Dockerfile, parse_config


@click.command()
def build():
    """
    build docker image
    """
    config = parse_config("./config.yaml")
    generate_Dockerfile(base_image=config["base_image"], models=config["models"])
    cmd = f"docker build -t {config['image_name']} ."
    os.system(cmd)


if __name__ == "__main__":
    build()
