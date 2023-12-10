import subprocess


def init_atx( ):
    try:
        1/0
        print("success")
    except Exception:
        print("except")
    finally:
       print("finally")
    return False

print(init_atx())