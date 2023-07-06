import os


def check_punctuation(sentence):
    flag=0
    list_punc_with_space=[" |"," ?"," !"," ।"]
    list_punc_without_space=["|","?","!","।"]
    
    if sentence.endswith(tuple(list_punc_with_space))==True:
        
        length=len(sentence)
        last_word=sentence[-1]
        if last_word=="।":
            sentence=sentence.replace(last_word,"|")
    elif sentence.endswith(tuple(list_punc_without_space))==True: 
        length=len(sentence)
        last_word=sentence[-1]
        if last_word=="।":
            sentence=sentence.replace(last_word," "+"|")
        else:
            sentence=sentence.replace(last_word," "+last_word)
    
    

    return sentence

def call_packages(filename):
    os.system("isc-parser -i"+filename+" > txt_files/parser-output.txt")
    os.system("utf8_wx "+filename+" > txt_files/wx.txt")
    os.system("python2.7 /home/manash/usrproginst/parser/getMorphPruneAndNER.py -i"+filename+" -o txt_files/prune-output.txt")
def call_usr_program():
    os.system("python3 generate_usr.py>hellow.txt")

    

    
        
    
           
    






if __name__=="__main__":
    file_name=input("Enter file name:")
    with open(file_name,"r",encoding="UTF-8") as f:
        sentence=f.readline()
        sentence=check_punctuation(sentence)
    
    f=open("txt_files/tmp.txt","w",encoding="UTF-8")
    f.write(sentence)
    f.close()
    call_packages("txt_files/tmp.txt")
    call_usr_program()

    

