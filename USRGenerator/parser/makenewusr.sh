#rm txt_files/*
isc-parser -i $1 > ./USRGenerator/parser/txt_files/parser-output.txt
utf8_wx $1 > ./USRGenerator/parser/txt_files/wx.txt


python2.7 ./USRGenerator/parser/getMorphPruneAndNER.py -i $1 -o ./USRGenerator/parser/txt_files/prune-output.txt


