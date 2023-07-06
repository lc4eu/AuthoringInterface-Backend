import os
try:
    os.remove("txt_files/parser-output.txt")
    os.remove("txt_files/prune-output.txt")
    #os.remove("txt_files/tmp.txt")
    os.remove("txt_files/wx.txt")
    #os.remove("txt_files/hello_test.txt")
    #os.remove("txt_files/bh-1")
except Exception as e:
    print(e)
