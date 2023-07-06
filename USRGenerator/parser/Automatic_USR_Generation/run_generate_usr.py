import os
file_name=open("sentences_for_USR","r",encoding="UTF-8")
file_to_paste=open("txt_files/bh-1","r+",encoding="UTF-8")
file_to_paste_temp=open("bh-2","r+",encoding="UTF-8") #creating a temporary file,just to keep record of the original sentence
for sentence in file_name:
    sentence=sentence.strip()
    print(sentence)
    try:
        file_to_paste=open("txt_files/bh-1","r+",encoding="UTF-8")
        s_id=sentence.split("  ")[0]
        print(s_id)
        orig_sent=sentence.split("  ")[1].strip()
        orig_sent_copy=sentence.split("  ")[1]
        file_to_paste.seek(0)
        file_to_paste.write(orig_sent)
        file_to_paste.truncate()
        file_to_paste.close()
        print("bh-1 closed")
        #------------------------------------------------------
        #Creating a temporary file for keeping record of the original sentence
        file_to_paste_temp.seek(0)
        file_to_paste_temp.write(orig_sent)
        file_to_paste_temp.truncate()
        #file_to_paste_temp.close()
        print("bh-2 created")
        #----------------------------------------------------------
        os.system("python3 sentence_check.py")
        os.system("sh makenewusr.sh txt_files/bh-1")
        os.system("python3 generate_usr.py>bulk_USRs/"+s_id)
        os.system("python3 delete_1.py")
    except Exception as e:
        print(e)
