from main.segmentation_main import Monitoring
import subprocess
import pandas as pd

model_id = 135


def test_use_python():
    Monitoring(model_id)
    assert pd.DataFrame


def test_use_command_line():
    subprocess.call(["python3", "../main/segmentation_main.py", str(model_id)])
    assert pd.DataFrame


if __name__ == '__main__':
    test_use_python()
    test_use_command_line()
