import re


#Open file parser-output.txt which is generated by running isc-parser
#store the contents into parser_output_lines 
#Enter the parser input file
parser_file_input="./USRGenerator/parser/txt_files/parser-output.txt"
prune_file_input="./USRGenerator/parser/txt_files/prune-output.txt"
wx_file_input="./USRGenerator/parser/txt_files/wx.txt"
concept_dictionary_input="./USRGenerator/parser/H_concept-to-mrs-rels.dat"
#Open the parser file,and store its contents into a 2d-list
parser_output_list=[]
with open(parser_file_input,"r",encoding="UTF-8") as pf:
    parser_output_lines=pf.readlines()
parser_output_lines.pop()
#we append the lines into a list thereby it is 2d list parser_output_list
for line in parser_output_lines:
    parser_output_list.append(line.split())

#Open pruner file and store all its words into a 2d list
prune_output_list=[]
with open(prune_file_input,"r",encoding="UTF-8") as pf:
    prune_output_lines=pf.readlines()
#we append the lines into a list thereby it is 2d list prune_output_list
for line in prune_output_lines:
    prune_output_list.append(line.split())

#open wx file and append it into a list
wx_output_list=[]
with open(wx_file_input,"r",encoding="UTF-8") as pf:
    wx_list=pf.readlines()
    wx_output_list=wx_list[0].split()
#print(wx_output_list)
#Open Concept dictionary and store it's contents into a list
concept_dictionary_list=[]
with open(concept_dictionary_input,"r") as cd:
    for line in cd:
        concept_real=line.split(" ")[1]
        concept_dictionary_list.append(concept_real)
#---------------------------------------------------------------

#--------------------------------------------------------------------
#Create a prune output list
prune_output_trimmed_list=[] #Only the prune output part,that we require
for line in range(len(prune_output_list)):
    #print(line)
    if "Pruning" in prune_output_list[line]:
        prune_len_init=line
    elif "NER" in prune_output_list[line]:
        prune_len_final=line
prune_output_trimmed_list=prune_output_list[prune_len_init+2:prune_len_final-1]
#---------------------------------------------------------------------
root_word_dict_reverse={} #key==wx_word and value is root_word from prune output
root_word_dict={} #key=root_word and value is wx_word
for line in range (len(prune_output_trimmed_list)):
    #wx_word=line[1]
    wx_word=wx_output_list[line]
    vm_row_new=prune_output_trimmed_list[line][4]
    vm_row_split_new=vm_row_new.split(",")
    root_word_prune=suffix=vm_row_split_new[0][4:]
    root_word_dict_reverse[wx_word]=root_word_prune
    if root_word_prune:
        root_word_dict[root_word_prune]=wx_word
#print(root_word_dict_reverse.get("PlOYpI"))
#print(root_word_dict_reverse["oYPisa"])
#print(root_word_dict)
#----------------------------------------------------------------


#creating a suffix dictionary where key is word and value is suffix a.k.a 8th vector
suffix_dictionary={}
word=str()
for line in prune_output_trimmed_list:
    #print(line[4])
    wx_word=line[1]
   # print(wx_word)
   # vm_row_new=line[4]
    vm_row_split_new=vm_row_new.split(",")
   # print(vm_row_split_new)
    suffix=vm_row_split_new[7][:-2].partition("'")[0]
    #print(vm_row_split_new)
    #print(suffix)
    suffix_dictionary[wx_word]=suffix
    
#print(suffix_dictionary)
    #print(type(word))
#---------------------------------------------------------------------
#Creating a dictionary for wx_words and their indexes
wx_words_dictionary={} #wx_words are value and keys are indexes.
index=1
for words in wx_output_list:
    wx_words_dictionary[index]=words
    index+=1
temp_wx_words_dict=wx_words_dictionary#temporary for loop usage
#print(wx_words_dictionary)
#------------------------------------------------------------------------
#creating a dictionary for parser_output_list
parser_output_dict={}
index=1
for par_value in parser_output_list:
    parser_output_dict[index]=par_value
    index+=1
#print(parser_output_dict)
#--------------------------------------------------------------------
#Creating a reverse dictionary for wx_words and their indexes
wx_words_dictionary_new={} #wx_words are key and values are indexes.
index=1
for words in wx_output_list:
    wx_words_dictionary_new[words]=index
    index+=1
temp_wx_words_dict=wx_words_dictionary_new#temporary for loop usage
#print(wx_words_dictionary_new)
#---------------------------------------------------------------------
concept_list=[]
used_root_word=set()
updated_root_word={}
info_list_final=[] #list containing important values from parser output file
for line in parser_output_list:
    info_list_temp=[]
    word_index=int(line[0])
    pos_tag=line[3]
    class_index=line[6]
    word_info=line[7]
    info_list_temp.append(word_index)
    info_list_temp.append(pos_tag)
    info_list_temp.append(class_index)
    info_list_temp.append(word_info)
    info_list_final.append(info_list_temp)
#for line in info_list_final:
#    print(line)
#--------------------------------------------------------------------
#Creating a TAM dictionary
#open the file and read its data into a list[str]
#split the data by tab and append these lists into a 2-d list TAM_dictionary_list
#remove its first element because 1st and 2nd element is repeated
f=open("./USRGenerator/parser/TAM-num-per-details.tsv.wx","r")
TAM_dictionary_list=[]
data=f.readlines()
for line in data:
    line=line.split("\t")
    line=[s.strip() for s in line]
    TAM_dictionary_list.append(line)

for line in TAM_dictionary_list:
    line.pop(0)

for line in TAM_dictionary_list:
    #print(line)
    '''matched_tams={}
real_tam_search="rahawe hEM"
for line in TAM_dictionary_list:
    for value in line:
        if real_tam_search.endswith(value) and  value!="" :
            #print(line[0],value)
            #print(line)
            matched_tams[value]=line[0]
            break
print(matched_tams)
longest_key_temp=0
for key in matched_tams.keys():
    longest_key_temp=len(key)'''
#---------------------------------------------------------------------   
def search_concept(search_word):
    key=0
    for word in concept_dictionary_list:
        if word==search_word:
            key=1
            break
    if key==0:
            print("Warning:{} not found in dictionary.".format(search_word))      
#----------------------------------------------------------------
#To print 1st row of USR which is the Original Sentence
def get_row1():
    row1="#"
    #orig_sent_copy=run_generate_usr.orig_sent_copy
    '''for p_list in parser_output_list:
        row1=row1+" "+p_list[1]
    row1=row1.replace("|","।")'''
    file_temp=open("./USRGenerator/parser/bh-2","r",encoding="UTF-8")
    sent_temp=file_temp.readline()
    file_temp.close()
    row1=row1+""+sent_temp
    return row1

#To generate groups,"Not clear about it's output.please refer"
group_list=[]
index=len(parser_output_list)
for val in range(index):
    if val==index-1 or parser_output_list[val][7]=="pof" or parser_output_list[val][7]=="pof__cn":
        group_list.append("0")
        #print(parser_output_list[val][1])
    elif parser_output_list[val][7]=="lwg__psp":
        group_list.append("-1")
        #print(parser_output_list[val][1])
    else:
        group_list.append("1")
        #print(parser_output_list[val][1])
 
#-----------------------------------------------------------------------
#Row 2 of USR Which is Concept 
#for every element in wx_output_list,check its POS TAG
#the third column in parser_output_list[][3] is POS TAG,index from 0
already_visited={} #it is currently being used for VAUX and class words which have to be ignored while checking
VM_already_visited={} #To check if VM is already updated or not.Used only for verb groups.Key is wx_word and value is updated verbgroup

def for_VM_no__1(row_2):
    for word in range(len(row_2)):
        if "+" in row_2[word]:
            ini_part=row_2[word].split("+",1)[0].strip("_1")
            
            final_part=row_2[word].split("+",1)[1]
            #print("finalpart:",final_part)
            row_2[word]=ini_part+"+"+final_part
    return row_2

def get_8th_vector(word):
    vector_8th=suffix_dictionary[word]
    '''for line in morph_output_list:
        if word in line:
            vm_row=line.split()[4]
            vm_row_split=vm_row.split(",")
            vector_8th=vm_row_split[7][:-2].partition("'")[0]'''
    return vector_8th
        
def get_root_word(word):#updated
    
    root_word=root_word_dict_reverse[word]
    
    return root_word
    
def for_handling_nnc_tag_or_pof(word,class_index):
    root_word=get_root_word(word)
    class_word=wx_words_dictionary[class_index]
    already_visited[class_word]=1
    if class_word in VM_already_visited:
        root_word_class=VM_already_visited[class_word]
        concept_list.remove(root_word_class)
    else:
        root_word_class=get_root_word(class_word)
    if root_word_class in used_root_word:
        root_word_class=updated_root_word[root_word_class]
        concept_list.remove(updated_root_word[root_word_class])
        #updated_root_word[root_word_class]=root_word+"+"+root_word_class
        #print("updated root word dict:",updated_root_word[root_word_class]) 
        
    else:
        used_root_word.add(root_word_class)
        updated_root_word[root_word_class]=root_word+"+"+root_word_class
    final_word=root_word+"_1"+"+"+root_word_class+"_1"
    VM_already_visited[class_word]=final_word
    return final_word
#---------------------------------------------------------------------
#Step 1:Take the second row and identfify TAMs present in them.
def identify_vb(concept_list):
    tam_list_row2=[]
    for concept in concept_list:
        if "-" in concept:
            tam_list_row2.append(concept)
    return tam_list_row2

def word_search_from_end(search_word):
    
    if "_1" in search_word:
        search_word=search_word.strip("_1")
        search_word=root_word_dict[search_word]
    #else:
     #   search_word=root_word_dict[search_word]
    #print("search_word:",search_word)
    match_key_list=[]
    matched_tams={}
    real_tam_search=search_word
    for line in TAM_dictionary_list:
        
        for value in line:
            if real_tam_search.endswith(value) and  value!="" :
                key=value
                line0_length=len(line[0])
                if key not in matched_tams.keys():
                    matched_tams[value]=line[0]
                else:
                    if line0_length > len(matched_tams[value]):
                        matched_tams[value]=line[0]
                
                #print(line[0],value)
        #matched_tams[value]=max(match_key_list,key=len)
        #print(match_key_list)
            
                #break
    #print(matched_tams)
    longest_key=int(0)
    longest_key_value=int(0)
    key_tam=None
    for key in matched_tams:
        key_temp_length=len(key)
        if key_temp_length>longest_key:
            longest_key_value=key
            longest_key=key_temp_length
    try:
        if longest_key_value !=0:
            key_tam=matched_tams[longest_key_value]
    
        
    #print(key_tam)
    #key_tam is the value of longest matched TAM from TAM dictionary.
        return key_tam
    except Exception as e:
        print(e)
    
   
    
 


def search_tam_row2(concept_list):
    tam_list_row2=identify_vb(concept_list)
    #print("This is our TAM:",tam_list_row2)
     
    for concept_with_hyphen in tam_list_row2:
        #print("The verb group to be replaced:",concept_with_hyphen)
        #concept_with_hyphen is the word in concept list that we have to replace
        if concept_with_hyphen.split("-")[1]=="":
            real_tam_temp="0"
        else:
            real_tam_temp=concept_with_hyphen.split("-")[1]
        #print(real_tam_temp)
        if real_tam_temp=="0":
            root_concept=concept_with_hyphen.split("-")[0]
            #print(root_concept)
            search_word=root_concept.strip("_1")
            if "+" in root_concept:
                search_word=root_concept.split("+")[1]
            if "_1" in search_word:
                search_word=search_word.strip("_1")
            search_word=root_word_dict[search_word]
            #print("sw in row2:",search_word)
            
            key_tam=word_search_from_end(search_word)
            #print("key_tam value in search_tam_row2:",key_tam)
            if key_tam !=None:
                final_concept=root_concept+"-"+key_tam
            else:
                final_concept=root_concept
            #print(final_concept)
        else:
            #Word after hyphen in verb group
            root_concept=concept_with_hyphen.split("-")[0] 
            #Word before hyphen in verb group
            #print("root_concept:",root_concept)
            root_concept=root_concept.strip("_1")
            if "+" in root_concept:
                root_concept=root_concept.split("+")[1]
            if "_1" in root_concept:
                root_concept=root_concept.strip("_1")
            wx_word_for_root_concept=root_word_dict[root_concept]
            #this is the original word for root_concept
            #print(wx_word_for_root_concept)
            #real_tam_temp=real_tam_temp.strip("_")
            for char in real_tam_temp:
                if char=="_":
                    real_tam_temp=real_tam_temp.replace(char," ")
            #print("real_tam_temp",real_tam_temp)
            #if real_tam_temp=="0":

            real_tam_search=wx_word_for_root_concept+""+real_tam_temp
            #if "_" in real_tam_search:
            #    real_tam_search=real_tam_search.strip("_")
            #print("real tam search_2:",real_tam_search) #This is the real TAM that we work with,searching in the backend happens on this.
            key_tam=word_search_from_end(real_tam_search)
            #The above function,returns the actual TAM matching from the TAM dictionary
            #if no match found in TAM dictionary,it returns none.
            #print("print key_tam is:",key_tam)
            #concept_list=list(map(lambda x:x.replace(concept_with_hyphen,key_tam),concept_list))
            init_part=concept_with_hyphen.split("-")[0]
            if key_tam is not None:
                final_concept=init_part+"-"+key_tam
            else:
                final_concept=init_part
        #print("final concept:",final_concept)
        #print("This is the final concept:",final_concept)
        concept_list=list(map(lambda x:x.replace(concept_with_hyphen,final_concept),concept_list))
        #print(concept_list)
        
    return concept_list
#----------------------------------------------------------------------
def pronouns_to_replace(concept_list):
    concept_list_temp=concept_list
    category_1=["wuma","wumhArA","wumako","wuJe","wU","wuJako","Apa"]
    category_2=["mEM","hama","hamArA","hamako","hameM","muJe","muJako"]
    category_3=["Ji"]
    for index in range(len(concept_list_temp)):
        word=concept_list_temp[index]
        if "+" in word:
            continue
        else:
            if word in category_1:
                concept_list_temp[index]="addressee"
            elif word in category_2:
                concept_list_temp[index]="speaker"
            elif word in category_3:
                concept_list_temp[index]="respect"
            else:
                continue
    return concept_list_temp
#----------------------------------------------------------------------------------------------------------
def get_row2():
    #pos_tag_dictionary={}#where key is wx_word and value is pos_tag
    
    #already_visited={}
    
    
    counter=0
    for word in wx_output_list:
        
        word_index=wx_words_dictionary_new[word] #word index of the word in wx_list
        for line in info_list_final:
            if word_index in line:
                pos_tag=line[1]
                class_index=int(line[2])
                word_info=line[3]
        #main condition check begins here:
        
        if pos_tag=="PSP"  or pos_tag=="SYM":
            continue
        elif pos_tag=="VM": #Do not add suffix for these words because we have to do TAM search on them and it creates a problem later.
            #print("this is the word:",word)
            root_word=get_root_word(word)
            vector_8th=get_8th_vector(word)
            if word in VM_already_visited:
                
                root_word=VM_already_visited[word]
                concept_list.remove(root_word)

                final_word=root_word+"-"
            else:
                final_word=root_word+"_1"+"-"
            
            
            
            for line in info_list_final[word_index:-1]: #updated simply vaux to vaux root
                pos_tag=line[1]
                if pos_tag=="VAUX":
                    word_index=line[0]
                    temp=wx_words_dictionary[word_index]
                    #temp_root=root_word_dict_reverse[temp]
                    final_word=final_word+"_"+temp
                    #print(final_word)
                    already_visited[temp]=1
                else:
                    break
            
            VM_already_visited[word]=final_word #adding to the dictionary
            #sprint("this is final word:",final_word)
            concept_list.append(final_word)
        elif pos_tag=="VAUX" :
            if word in already_visited:
                if already_visited[word]==1:
                    continue
            else:
                root_word=get_root_word(word)
                concept_list.append(root_word+"_1")
        elif pos_tag=="NNC" or word_info=="pof":

            final_word=for_handling_nnc_tag_or_pof(word,class_index)
            '''if pos_tag=="NN":
                f_right=final_word.split("+")[1]
                final_word_temp=final_word.split("+")[0].strip("_1")
                final_word=final_word_temp+"+"+f_right'''
                
            concept_list.append(final_word)
        else:
            if word in already_visited:
                continue
            root_word=get_root_word(word)
            if pos_tag=="PRP" or pos_tag=="DEM" or pos_tag=="NNP" :
                concept_list.append(root_word)
            else:
                concept_list.append(root_word+"_1")
        counter+=1
    
    #print(concept_list)
    concept_list_final=search_tam_row2(concept_list)
    #print("concept list final:",concept_list_final)
    return concept_list_final

#--------------------------------------------------------------------
  

#Row 3 of USR:Index for concepts
def get_row3(concept_list):
    index_for_concepts=[]
    for ind in range(len(concept_list)):
        index_for_concepts.append(ind+1)
    return index_for_concepts
#----------------------------------------------------------------------
#Row 4 of USR:Semantic category of Nouns
def get_row4(row_2):
     # print(row_2)
    sem_category_list=[]
    index_value_list=[]
    for vax in range(len(prune_output_lines)):
        if "NER" in prune_output_lines[vax]:
            break
    NER_list=prune_output_lines[vax:-1]
    #for word in NER_list:
    #    print(word)
    row_4_temp=[]
    for concept in row_2:
        if "+" in concept:
            row_4_temp.append(",")
            index_value_list.append(",")
        elif "-" in concept:
            row_4_temp.append(",")
            index_value_list.append(",")
        else:
            concept=concept.split("_")[0]
            original_word=root_word_dict[concept]
            row_4_temp.append(original_word)
            index_value_list.append(wx_words_dictionary_new[original_word])
        #print(row_4_temp)
        #print(index_value_list)
    for index in index_value_list:
        index=str(index)
        if index==",":
            sem_category_list.append("")
        else:
            flag=0
            for word in NER_list:
                if index in word and "location" in word:
                    sem_category_list.append("loc")
                    flag=1
                    break
                elif index in word and "person" in word:
                    sem_category_list.append("per")
                    flag=1
                    break
                elif index in word and "organization" in word:
                    sem_category_list.append("org")
                    flag=1
                    break
            if flag==0:
                sem_category_list.append("")
    return sem_category_list
#---------------------------------------------------------------------   
#Row 5 :Gender,Number,Person Information only for nouns (NN tag in parser)
#updated 20th august 2022:GNP also for Pronouns..PRP tag in parser
def get_row5(row_2):
    gnp_list_temp=[]
    row_5_temp=[]
    for concept in row_2:
       # print(concept)
        if "+" in concept or "-" in concept:
           #print(concept)
            row_5_temp.append(",")
        else:
            concept=concept.split("_")[0]
            original_word=root_word_dict[concept]
            row_5_temp.append(original_word)
    #row_5_temporary is a list containing words and commas which we need to check
    
    
    for word in row_5_temp:
        if word==",":
            gnp_list_temp.append("")
        else:
            for line in prune_output_trimmed_list:
                if word in line and (line[2]=="NN" or line[2]=="PRP" or line[2]=="NNP" or line[2]=="NNPC"):
                    af_values=line[4].split(",")
                    #print(af_values)
                    gender="-" if af_values[2] is None else af_values[2]
                    number="-" if af_values[3] is None else af_values[3]
                    person="-" if af_values[4] is None else af_values[4]
                    #print(gender)
                    if (gender=="" or number=="" or person==""):
                        gnp_list_temp.append("")
                        break
                    if gender=="any":
                        gender="-"
                    if number=="any":
                        number="-"
                    if person=="any":
                        person="-"
                    if person=="1":
                        person="u"
                    elif person=="2":
                        person="m"
                    elif person=="3":
                        person="a"
                    

                    gnp_list_temp.append("["+""+gender+" "+number+" "+person+"]")
                elif word in line and (line[3]!="NN" or line[3]!="PRP"):
                    gnp_list_temp.append("")
    return gnp_list_temp
#---------------------------------------------------------------------
#Row 6:Dependencies


def get_row2_index(word):
    matched_concepts={}
    counter=1
    for concept_final in row_2:
        temp_list=concept_final.split("+")
        matched_concepts[counter]=temp_list
        counter+=1
    #print(matched_concepts)
    #print(row_2)
    for key,value in matched_concepts.items():
        for root_words in value:
            if "-" in root_words:
                root_words=root_words.split("-")[0]
            if "_1" in root_words:
                root_words=root_words.strip("_1")
            if word==root_words:
                corr_index=key
            #print("matched word is:",root_words)
            #print("Correct index is:",key)
            

    return corr_index

def get_row6(row_2):
    
    #print("This is row_2:",row_2)
    #wx_word_inx=0
    row_6=[]
    row2_iter=[]#a list which is cleaned part of row2 to be worked upon
    row2_wx_index_iter=[]#list which has correct indexes of words in row_2
    class_word_index_list=[]#list which contains indexes of all class_words
    class_word_index_dict={}
    class_word_list=[]#list of class words from their indexexes in wx_format
    root_word_from_wx=[]#list of root words from their wx words
    dependency_col7_list=[]#list of col7 values in parser output
    correct_index_list=[]#list of final indexexs of dependencies in row2
    pos_tag_list=[]#list of pos tags of words present.
    #print(row_2)
    for concepts in row_2:
        if "+" in concepts:
            concepts=concepts.split("+")[1]
        if "-" in concepts:
            concepts=concepts.split("-")[0]
        concepts=concepts.split("_")[0]
        row2_iter.append(concepts)
    #print("iterable:",row2_iter) #iterable after cleaning
    
    for root_word in row2_iter:
        wx_word=root_word_dict.get(root_word)
        #print(wx_word)
        wx_word_inx=wx_words_dictionary_new[wx_word]
        #for key,value in temp_wx_words_dict.items():
         #   if value==wx_word:
          #      wx_word_inx=key
           #     value=0
        row2_wx_index_iter.append(wx_word_inx)
    
    #print("row2_wx_index:",row2_wx_index_iter) #indexes for same wx words
    
    for index_value in row2_wx_index_iter:
        par_value=parser_output_dict[index_value]
        class_word_index=int(par_value[6])
        pos_tag_value=par_value[3]
        dependency=par_value[7]
        class_word_index_list.append(class_word_index)
        dependency_col7_list.append(dependency)
        pos_tag_list.append(pos_tag_value)
    #print("class_word_indx_list:",class_word_index_list)
    #print("pos tag:",pos_tag_list)
    
    
    for index_6 in class_word_index_list:
        #do something about index_6==0 here
        if index_6==0:
            class_word_list.append(0)
        else:
            class_word_list.append(wx_words_dictionary[index_6])    
            
       # print(index_6)
    #print("This is class_word:",class_word_list)
    for word in class_word_list:
        if word==0:
            root_word_from_wx.append(0)
        else :
            key=root_word_dict_reverse[word]
            root_word_from_wx.append(key)
    #print("root of that class:",root_word_from_wx)
    #Now we have to find,where this word is in row_2 and get that index
    for word in root_word_from_wx:
        if word==0:
            correct_index_list.append(0)
            continue
        correct_index=get_row2_index(word)
        correct_index_list.append(correct_index)
    #print(correct_index_list)
    #print(dependency_col7_list)
    for val in range(len(dependency_col7_list)):
        if dependency_col7_list[val]=="main":
            row_6.insert(val,"0:main")
        else:
            #print(pos_tag_list[val])
            index_6a=str(correct_index_list[val])
            dependency_col7=dependency_col7_list[val]
            if  pos_tag_list[val]=="JJ":
                dependency_col7="mod"
            elif pos_tag_list[val]=="QC":
                dependency_col7="card"
            elif pos_tag_list[val]=="QO":
                dependency_col7="ord"
            elif dependency_col7=="lwg__neg":
                dependency_col7="neg"
            elif dependency_col7=="r6-k2":
                dependency_col7="k2"
            row_6.append(index_6a+":"+dependency_col7)
    #for word in row_6:
     #  if "r6-k2" in word:
      #  word.replace("r6-k2","r6")'''
    '''for inx in range(len(row_6)):
        if "lwg__neg" in row_6[inx]:
            word=row_6[inx]
            init_value=word.split(":")[0]
            row_6[inx]=init_value+":"+"neg"
        if "r6-k2" in row_6[inx]:
            word=row_6[inx]
            init_value=word.split(":")[0]
            row_6[inx]=init_value+":"+"k2"'''

    return row_6
#----------------------------------------------------------------------
#row 7
def get_row_unk(row_2):
    comma_list=[]
    for x in range(len(row_2)):
        comma_list.append("")
    return comma_list 
#--------------------------------------------------------------------
#Row 10:Sentence type
def get_row10():
    sentence_type=[]
    if "nahI" in wx_output_list or "nahIM" in wx_output_list:
        sentence_type.append('negative')
    else:
        if "?" in wx_output_list:
            sentence_type.append("interrogative")
        elif "." in wx_output_list:
            sentence_type.append("affirmative")
        elif "!" in wx_output_list:
            sentence_type.append("exclamatory")
    return sentence_type
#--------------------------------------------------------------------
def get_warning(row_2):
    for concept in row_2:
        if "_1" in concept:
            if "+" in concept and "-" in concept:
                search_word=concept.split("+")[1].split("-")[0]
                search_concept(search_word)
            elif "-" in concept:
                search_word=concept.split("-")[0]
                search_concept(search_word)
            else:
                search_concept(concept)

if __name__=="__main__":
    #row2 copy is a newlist,a copy of older one just to replace the pronouns.
    
        row_2=get_row2()
        #print("Final output main:",row_2)
        row_2_final=for_VM_no__1(row_2)
        #print("Final output main:",row_2_final)
        row_1=get_row1()
        #row_2=get_row2()
        #print(row_2)
        row_2_temp=row_2.copy()
        row_2_chg=pronouns_to_replace(row_2_temp)
        row_3=get_row3(row_2)
        row_4=get_row4(row_2)
        row_5=get_row5(row_2)
        row_6=get_row6(row_2)
        row_7=get_row_unk(row_2)
        row_8=get_row_unk(row_2)
        row_9=get_row_unk(row_2)
        row_10=get_row10()
        #get_warning(row_2)
        print(row_1)
        print(",".join(row_2_temp))
        print(",".join(map(str,row_3)))
        print(",".join(row_4))
        print(",".join(map(str,row_5)))
        print(",".join(row_6))
        print(",".join(row_7))
        print(",".join(row_8))
        print(",".join(row_9))
        print(",".join(row_10))
        
                    
                

        
        

        







  






    





    


    
