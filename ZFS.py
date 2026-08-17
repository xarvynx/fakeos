import os

ROOT = os.path.join(os.getcwd(),"FakeOS_FS")
os.makedirs(ROOT, exist_ok=True)

def path(relative_path):
    