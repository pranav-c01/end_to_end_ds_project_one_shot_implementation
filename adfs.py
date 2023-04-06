from src.exception import Custom_exception
try:
    d = 1/0
except Exception as e:
    import sys
    raise Custom_exception(e,sys)
print("done")