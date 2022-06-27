# coding=utf-8
import os
import shutil
import traceback


def move_file(src_path, dst_path, file):
    print("from : ", src_path)
    print("to : ", dst_path)
    try:
        f_src = os.path.join(src_path, file)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        f_dst = os.path.join(dst_path, file)
        shutil.move(f_src, f_dst)
    except Exception as e:
        print("move_file ERROR: ", e)
        traceback.print_exc()
