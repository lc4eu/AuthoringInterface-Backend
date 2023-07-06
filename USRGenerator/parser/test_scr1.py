w=open("usr_combined","w")
for i in range(1,30):
    f=open("bulk_USRs/"+str(i))
    for line in f:
        w.write(line)
    w.write("\n")
    w.write("\n")
