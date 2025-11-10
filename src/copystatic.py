import os
import shutil

def copystatic(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    
    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
        if os.path.isfile(src_path):
            print(f"copy {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copystatic(src_path, dst_path)
