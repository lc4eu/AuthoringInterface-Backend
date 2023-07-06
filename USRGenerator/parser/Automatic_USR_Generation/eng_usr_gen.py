#Enter the path of concept_dictionary and tam mapping here:
concept_dictionary="H_concept-to-mrs-rels.dat"
tam_mapping="/home/manash/lc4eu/dictionaries/tam_mapping.dat"

concept_dictionary_list=[]
tam_mapping_list=[]


f= open(concept_dictionary,"r")
for line in f:
    concept_dictionary_list.append(line)
f.close()

f1=open(tam_mapping,"r")
for line in f1:
    #line=line.strip()
    if line=="\n":
        continue
    tam_mapping_list.append(line)
#print(tam_mapping_list)
def usr_list_creation(usr_file):
    with open(usr_file,"r") as f:
        for row in f:
            #print("in usr_creation_list:",row)
            usr_list.append(row.split(","))
    return usr_list
def search_concept(word):
    for line1 in concept_dictionary_list:
        concept=line1.split("\t")[1]
        concept=concept.strip()
        if word==concept:
            return line1.split("\t")[2]
def search_tam(tam_word):
    tam_word.strip()
    for line_tam in tam_mapping_list:
        #print(line_tam)
        if line_tam==" ":
            continue
        list_sp=line_tam.split("  ",1)[1]
        h_tam=list_sp.split("  ",1)[0]
        #print(h_tam)
        #print("this is tam_word:",tam_word)
        e_tam=list_sp.split("  ",1)[1][:-3]
        #print("this is e_tam:",e_tam)
        if tam_word==h_tam.strip():
            #print("the tam being returned:",e_tam)
            return e_tam
            


#search_tam() 
def eng_concepts_for_row2(row_2):
    eng_row2=[]
    #usr_file="verified_sent/3"
    '''with open(usr_file,"r") as f:
        for row in f:
            usr_list.append(row.split(",")) '''         
    for word in row_2:
        word=word.strip()
        if word=="addressee" :
            eng_row2.append("addressee")
        elif word=="speaker":
            eng_row2.append("speaker")
        elif word=="respect":
            eng_row2.append("respect")
        elif "-" in word:
            word1=word.split("-")[0]
            word2=word.split("-")[1].strip()
            #print(word2)
            e_word=search_concept(word1)
            t_word=search_tam(word2)
            #print(word2)
        #e_word=search_concept(word)
            eng_row2.append(e_word+"-"+t_word)
        else:
            e_word=search_concept(word)
            if e_word is None:
                e_word=word
            eng_row2.append(e_word)
    return eng_row2
    #print(eng_row2)
if __name__=="__main__":
    #index="1"
    usr_list=[] 
    #Enter the number of Hindi USRs present in verified_sent directory
    for i in range(1,10):
        index=str(i)
        #Enter the usr file path here
        usr_file="verified_sent/"+index
        #print(usr_file)
        usr_list=usr_list_creation(usr_file)
        '''for line in usr_list:
            print(line)'''
        row_2=usr_list[1]
        #print(row_2)
        row_2_updated=eng_concepts_for_row2(row_2)
        #print("updated_row2",row_2_updated)
        usr_list[1]=row_2_updated
        for line in usr_list:
            line=[str(di) if di is None else di for di in line]
            line=[di.replace("None","") if di == "None" else di for di in line]
            print(",".join(line))
            ##print(line)
        usr_list.clear()
        