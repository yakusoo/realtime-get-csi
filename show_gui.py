import subprocess

def do_gui():
    cmd = "python practice_label2.py"
    subprocess.run(cmd, shell=True)

def do_predict():
    cmd = "python predict_demo.py"
    subprocess.run(cmd, shell=True)

