from flask import Flask, flash, request, session, jsonify
from flask_mysqldb import MySQL
from flask_session import Session
from config import app
from wxconv import WXC
import MySQLdb.cursors
import re
from config import mysql
import os
import json
from flask_cors import CORS, cross_origin

Session(app)
CORS(app)


@app.route('/')
def index():
    return "Backend Running", 200


@app.route('/create_database')
def create_database():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS author (author_id int AUTO_INCREMENT , author_name varchar(255), email varchar(255), password varchar(16), reviewer_role varchar(255), PRIMARY KEY(author_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS discourse (discourse_id int NOT NULL AUTO_INCREMENT, discourse_name varchar(255),author_id int, no_sentences int, domain varchar(255), create_date datetime default now(), other_attributes VARCHAR(255), sentences MEDIUMTEXT,PRIMARY KEY (discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS usr (author_id int,  discourse_id int, sentence_id varchar(255) ,USR_ID int NOT NULL AUTO_INCREMENT, orignal_USR_json MEDIUMTEXT,final_USR json,create_date datetime default now(),USR_status varchar(255),FOREIGN KEY (discourse_id) REFERENCES discourse(discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id), PRIMARY KEY (USR_ID))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS demlo(demlo_id int AUTO_INCREMENT, demlo_txt JSON, PRIMARY KEY (demlo_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS edit(edit_id int AUTO_INCREMENT, edited_USR MEDIUMTEXT, edit_date datetime default now(), author_id int,  discourse_id int, USR_ID int, FOREIGN KEY (author_id) REFERENCES author(author_id),FOREIGN KEY (discourse_id) REFERENCES discourse(discourse_id), FOREIGN KEY (USR_ID) REFERENCES usr(USR_ID), status varchar(255), PRIMARY KEY(edit_id), sent_id varchar(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS `semcateofnouns` (`scn_id` INT NOT NULL AUTO_INCREMENT,`scn_value` VARCHAR(45) NULL,`scn_title` VARCHAR(255) NULL,PRIMARY KEY (`scn_id`));")
    cursor.execute("INSERT INTO `semcateofnouns` (`scn_value`, `scn_title`) VALUES ('',''),('anim','Animacy'),('org','Organization'),('mass','Mass'),('abs','Abstract'),('place','Place'),('dow','Day of week'),('moy','Month of year'),('yoc','Year of Century'),('ne','Names of movies or medicine or cuisine or games or disease');")
    cursor.execute("CREATE TABLE IF NOT EXISTS `sentencetype` ( `sen_id` int NOT NULL AUTO_INCREMENT, `sen_value` varchar(45) DEFAULT NULL, PRIMARY KEY (`sen_id`) ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
    cursor.execute("INSERT INTO `sentencetype` (`sen_value`) VALUES(''),('negative'),('affirmative'),('interrogative'),('yn_interrogative'),('imperative'),('pass-affirmative'),('pass-interrogative');")
    cursor.execute("CREATE TABLE IF NOT EXISTS `speakersview` ( `spv_id` int NOT NULL AUTO_INCREMENT, `spv_value` varchar(45) DEFAULT NULL, `spv_title` varchar(255) DEFAULT NULL, PRIMARY KEY (`spv_id`) ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
    cursor.execute("INSERT INTO `speakersview` (`spv_value`, `spv_title`) VALUES('',''),('respect','respect'),('def','definiteness'),('deic','deicticity'),('RPs','Relation particles or discourse particles');")
    cursor.execute("CREATE TABLE IF NOT EXISTS `deprelation` ( `dpr_id` int NOT NULL AUTO_INCREMENT, `dpr_value` varchar(45) DEFAULT NULL, `dpr_title` varchar(255) DEFAULT NULL, PRIMARY KEY (`dpr_id`) ) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
    cursor.execute("INSERT INTO `deprelation` (`dpr_value`, `dpr_title`) VALUES('main','main'), ('card','Cardinals'), ('dem','demonstrative'), ('intf','intensifier'), ('jk1','prayojya karta'), ('k1','kartaa'), ('k1s','karta samAnAdhikaraNa'), ('k2','karmaa'), ('k2p','gola, destination'), ('k2g','gauna karma'), ('k2s','karma samanadhikarana'), ('k3','karaNa'), ('k4','sampradana'), ('k4a','experienecer,anubhava karta'), ('k5','apadana'), ('k5prk','prakruti apadana'), ('k7','vishayadhikarana'), ('k7p','xeSaXiKaraNa'), ('k7t','kAlaXikaraNa'), ('krvn','manner adverb'), ('mk1','madhyastha karta'), ('mod','Quality'), ('neg',''), ('ord','Ordinals'), ('pk1','prayojaka karta'), ('quant','quantifier'), ('r6','sasthi or samandha pada'), ('re','relation elaboration'), ('rh','relation hetu'), ('rt','relation tadartha'), ('ru','relation upamAna'), ('rv','relation ViBAjana'), ('rd','relation direction'), ('rkl','relation kAlalakRaNa'), ('rdl','relation kAlalakRaNa'), ('rask1','relation associate kartaa'), ('rask2','relation associate karma'), ('rask4','relation associate sampradan'), ('rblak','relation Bava lakRaNa ananwarakAlika'), ('rblpk','relation Bava lakRaNa purvakAlika'), ('rpk','relation purvakalika'), ('rsm','relation sWAyi swAmi'), ('rsma','relation asWAyi swami'), ('rsk','relation samAnakAlika'), ('rhh','relation human to human'), ('rblsk','relation BAvalakRaNa samAnakAlika'), ('rvks','relation varwamAnakAlikasamAnAXikaraNa'), ('rbks','relation BhhowakAlikasamAnAXikaraNa'), ('vk2','vakya karma');")
    mysql.connection.commit()
    return "Database Created", 200


@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = json.loads(request.data)
    author_name = data.get('author_name')
    email = data.get('email')
    password = data.get('password')
    reviewer_role = data.get('reviewer_role')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT author_id FROM author WHERE email = %s and reviewer_role=%s', (email, reviewer_role))
    author = cursor.fetchone()
    if author is not None:
        return jsonify(message='Author already exists!'), 409
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return jsonify(message='Invalid email address!'), 400
    else:
        cursor.execute('INSERT INTO author VALUES (NULL, %s, %s, %s, %s)',
                       (author_name, email, password, reviewer_role))
        mysql.connection.commit()
        return jsonify(message='You have successfully registered!'), 200


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        email = data.get('email')
        password = data.get('password')
        reviewer_role = data.get('reviewer_role')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM author WHERE email=%s AND password=%s;', (email, password))

        author = cursor.fetchone()
        print(author)
        print(author)
        if author:
            session['loggedIn'] = True
            session['author_id'] = author['author_id']
            session['user_type'] = reviewer_role
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT author_id, author_name, email, reviewer_role FROM author WHERE author_id = %s", str(session['author_id']))
            authdet = cursor.fetchone()
            return jsonify(authdet), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401


@ app.route('/logout')
def logout():
    session["logged_in"] = True
    session.clear()
    return jsonify("Logged out"), 200


@app.route('/usrgenerate', methods=['POST'])
@cross_origin()
def usrgenerate():
    if request.method == "POST":
        data = json.loads(request.data)
        discourse = data.get('discourse')
        discourse_name = data.get('discourse_name')
        author_id = data.get('author_id')

        # if request.form.get('Save Sentences') == 'Save discourse':
        # Saving user details to the discourse table

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("INSERT INTO discourse(author_id, sentences, discourse_name) VALUES(%s, %s, %s)",
                       (author_id, discourse, discourse_name))
        mysql.connection.commit()
        discourse_id = cursor.lastrowid
        list_usr = list(displayUSR(discourse))

        # saving generated usr in database in usr table
        for i in range(len(list_usr)):
            cursor.execute("INSERT INTO usr(author_id,discourse_id,sentence_id,orignal_USR_json,USR_status) VALUES(%s,%s,%s,%s,%s)",
                           (author_id, discourse_id, i+1, list_usr[i], "In Edit"))
            mysql.connection.commit()

            cursor.execute("INSERT INTO edit(author_id,discourse_id,sent_id,edited_USR,status) VALUES(%s,%s,%s,%s,%s)",
                           (author_id, discourse_id, i+1, list_usr[i], "In Edit"))
            mysql.connection.commit()

        # saving sentence entered by user in updatedSentence.txt
        with open("../client/public/updatedSentence.txt", "w", encoding='utf-8') as sentfile:
            str2 = ""
            str_end = ["।", "|", "?", "."]
            for word in discourse:
                str2 += word
                if word in str_end:
                    str2 = str2.strip()
                    sentfile.write(str2+"\n")
                    str2 = ""

        # saving generated usr in data.json
        with open("../client/src/data/data.json", "w", encoding='utf-8') as f:
            f.write(str(list_usr).replace("'", '"'))
            f.close()
            flash("USR Generated")

        return jsonify(discourse_id), 200
    else:
        return "Something went wrong", 400


def displayUSR(corpus_for_usr):
    # Pre-processing of the corpus for USR generation.
    str1 = corpus_for_usr
    if corpus_for_usr is None:
        return jsonify("Not a Valid Sentence")
    f = open("./USRGenerator/parser/sentences_for_USR", "w", encoding='utf-8')
    str_end = ["।", "|", "?", "."]
    str2 = ""
    sent_id = 0
    for word in str1:
        str2 += word
        if word in str_end:
            str2 = str2.strip()
            f.write(str(sent_id)+"  "+str2+"\n")
            sent_id += 1
            str2 = ""
    f.close()
    # Clean up bulk USRs directory
    for file in os.listdir("./USRGenerator/parser/bulk_USRs"):
        os.remove("./USRGenerator/parser/bulk_USRs/"+file)
    with open("./USRGenerator/parser/sentences_for_USR", "r", encoding='utf-8') as f:
        for data in f:
            file_to_paste = open(
                "./USRGenerator/parser/txt_files/bh-1", "w", encoding='utf-8')
            file_to_paste_temp = open(
                "./USRGenerator/parser/bh-2", "w", encoding='utf-8')
            sent = data.split("  ")[1]
            s_id = data.split("  ")[0]
            file_to_paste.write(sent)
            file_to_paste_temp.write(sent)
            file_to_paste_temp.close()
            file_to_paste.close()
            # os.system("cd /mnt/c/Users/gupta/OneDrive/Desktop/USR_GENERATOR/parser && ls" )
            # os.system("ls")
            os.system("python3 ./USRGenerator/parser/sentence_check.py")
            os.system(
                "sh ./USRGenerator/parser/makenewusr.sh ./USRGenerator/parser/txt_files/bh-1")
            os.system(
                "python3 ./USRGenerator/parser/generate_usr.py>./USRGenerator/parser/bulk_USRs/"+s_id)
            os.system("python3 ./USRGenerator/parser/delete_1.py")
    generated_usrs = {}
    gs = []
    for file in os.listdir("./USRGenerator/parser/bulk_USRs"):
        usr_file = open("./USRGenerator/parser/bulk_USRs/" +
                        file, "r", encoding='utf-8')

        usr_list = usr_file.readlines()
        usr_dict = {}
        # usr_dict["sentence_id"]=0,
        # usr_dict['sentence']=usr_list[0].strip()
        usr_dict['Concept'] = usr_list[2].strip().split(",")
        usr_dict['Index'] = [int(x) for x in usr_list[3].split(",")]
        usr_dict['SemCateOfNouns'] = usr_list[4].strip().split(",")
        usr_dict['GNP'] = usr_list[5].strip().split(",")
        usr_dict['DepRel'] = usr_list[6].strip().split(",")
        usr_dict['Discourse'] = usr_list[7].strip().split(",")
        usr_dict['SpeakersView'] = usr_list[8].strip().split(",")
        usr_dict['Scope'] = usr_list[9].strip().split(",")
        usr_dict['SentenceType'] = usr_list[10].strip().split(",")
        usr_dict['Construction'] = ""
        # generated_usrs[file]=usr_dict
        gs.append(usr_dict)
    return gs


@app.route('/fileinsert', methods=['POST'])
def fileinsert():
    if request.method == "POST":
        data = request.get_json()
        sentences = data.get('sentences')
        discourse_name = data.get('discourse_name')
        jsondata = data.get('jsondata')
        sentencearray = data.get('sentencearray')
        author_id = data.get('author_id')

        no_sentences = len(sentencearray)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute(
        #     'SELECT author_name FROM author WHERE author_id = {0} '.format(author_id))
        # author_id = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO discourse(author_id, sentences, discourse_name, no_sentences) VALUES(%s, %s, %s,%s)",
                       (author_id, sentences, discourse_name, no_sentences))
        mysql.connection.commit()
        discourse_id = cursor.lastrowid
        print(discourse_id)

        for i in range(no_sentences):

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "INSERT INTO usr(author_id, discourse_id, orignal_USR_json, USR_status) VALUES(%s, %s, %s, %s)", (author_id, discourse_id, jsondata[i], "In Edit"))
            mysql.connection.commit()
            usrid = cursor.lastrowid
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO edit(author_id, discourse_id, edited_USR, status, USR_ID, sent_id) VALUES(%s, %s, %s, %s, %s, %s)",
                           (author_id, discourse_id, jsondata[i], "In Edit", usrid, '2'))
            mysql.connection.commit()

        return jsonify(discourse_id), 200
    else:
        return "USRs could not be uploaded!", 400


@app.route('/orignal_usr_fetch/<discourse_id>', methods=['GET'])
def orignal_usr_fetch(discourse_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # print("Hello ",dis_id)
        query = 'SELECT e1.usr_id, e1.edited_usr, e1.edit_date,e1.status FROM edit e1 INNER JOIN ( SELECT usr_id, MAX(edit_date) AS max_edit_date FROM edit WHERE discourse_id =%s GROUP BY usr_id ) e2 ON e1.usr_id = e2.usr_id AND e1.edit_date = e2.max_edit_date WHERE e1.discourse_id = %s ORDER BY e1.usr_id'
        params = (discourse_id, discourse_id)
        cursor.execute(query, params)
        data = cursor.fetchall()
        return jsonify(data), 200
    else:
        return "Data could not be fetched because of some error!", 400


@app.route('/dicourses_for_a_user/<author_id>', methods=['GET'])
def uniqu_dis(author_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT distinct discourse.discourse_id,discourse_name,sentences,USR_status FROM discourse JOIN usr ON discourse.discourse_id=usr.discourse_id WHERE discourse.author_id = {0}".format(author_id))
        dasdata = cursor.fetchall()
        return jsonify(dasdata), 200
    else:
        return "Data could not be fetched due to some error!", 400


@ app.route('/card_data/<author_id>', methods=['GET'])
def card_data(author_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * from discourse WHERE author_id = {0} '.format(author_id))
        discourse = cursor.fetchall()
        no_of_discourses = len(discourse)
        cursor.execute(
            'SELECT * from usr WHERE author_id = {0} '.format(author_id))
        usr = cursor.fetchall()
        no_of_usrs = len(usr)
        cursor.execute(
            'SELECT distinct discourse_id from edit WHERE author_id = {0} AND status= {0}'.format(author_id, "Approved"))
        no_of_approved = len(cursor.fetchall())
        return jsonify(discourse_count=no_of_discourses, usr_count=no_of_usrs, approved_count=no_of_approved), 200
    else:
        return "Data could not be fetched because of some error!", 400


@ app.route('/usr_corresponding_to_discourse/<author_id>', methods=['GET'])
def usr_corresponding_to_discourse(author_id):
    try:
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM discourse JOIN usr ON discourse.discourse_id=usr.discourse_id WHERE discourse.author_id = {0}".format(author_id))
            usrRows = cursor.fetchall()
            return jsonify(usrRows), 200
        else:
            return "Data could not be fetched because of some error!", 400
    except Exception as e:
        print(e)


@ app.route('/discourse/<discourse_id>')
def discourse(discourse_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM discourse WHERE discourse_id={0}".format(discourse_id))
        disRows = cursor.fetchone()
        respone = jsonify(disRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/editusr', methods=['POST'])
@cross_origin()
def editusr():
    if request.method == "POST":
        data = request.get_json()
        finalJson = data.get('finalJson')
        discourseid = data.get('discourseid')
        usrid = data.get('usrid')
        author_id = data.get('author_id')
        print(usrid)
        print(discourseid)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO edit(author_id, discourse_id, edited_USR, status, usr_id) VALUES(%s,%s,%s,%s,%s)",
                       (author_id, discourseid, finalJson, "In Edit", usrid))
        mysql.connection.commit()

        return jsonify("Edited Successfully!!!"), 200
    else:
        return "Could not make changes, Something went wrong!", 400


@app.route('/editstatus', methods=['POST'])
def editstatus():
    if request.method == "POST":
        data = request.get_json()
        status = data.get('status')
        usrid = data.get('usrid')
        author_id = data.get('author_id')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "UPDATE edit SET status=%s WHERE usr_id=%s AND author_id = %s", (status, usrid, author_id))
        mysql.connection.commit()
        return jsonify("Status updated successfully"), 200
    else:
        return "Could not make changes, Something went wrong!", 400


@app.route('/delete_discourse/<discourse_id>', methods=['DELETE'])
def delete_discourse(discourse_id):
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'DELETE FROM edit WHERE edit.discourse_id={0}'.format(discourse_id))
        cursor.execute(
            'DELETE FROM usr WHERE usr.discourse_id={0}'.format(discourse_id))
        cursor.execute(
            'DELETE FROM discourse WHERE discourse.discourse_id={0}'.format(discourse_id))
        mysql.connection.commit()
        return "Discourse Deleted Successfully!", 200
    else:
        return "Could not delete the discourse!", 400


@app.route('/semcateofnouns', methods=['GET'])
def get_nouns():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM semcateofnouns;")
        result = cursor.fetchall()
        return jsonify(result), 200
    else:
        return "Data could not be fecthed", 400


@app.route('/sentencetype', methods=['GET'])
def get_sentencetype():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM sentencetype;")
    result = cursor.fetchall()
    return jsonify([dict(row) for row in result])


@app.route('/speakersview', methods=['GET'])
def get_speakersview():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM speakersview;")
    result = cursor.fetchall()
    return jsonify([dict(row) for row in result])


@app.route('/deprelation', methods=['GET'])
def get_deprelation():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM deprelation;")
    result = cursor.fetchall()
    return jsonify([dict(row) for row in result])


@app.route('/update_status', methods=['PUT'])
def update_status():
    if request.method == 'PUT':
        dis_id = request.args.get('dis_id')
        s_value = request.args.get('s_value')
        usr_id = request.args.get('usr_id')
        print("bdsfbd", usr_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'UPDATE usr SET USR_status={0} WHERE discourse_id={1} AND USR_ID={2}'.format(s_value, dis_id, usr_id))
        cursor.execute(
            'UPDATE edit SET status={0} WHERE discourse_id={1} AND USR_ID={2}'.format(s_value, dis_id, usr_id))

        mysql.connection.commit()
        return "Status updated", 200
    else:
        return "Could not update the status", 400


@app.route('/usrs_for_a_discourse/<discourse_id>', methods=['GET'])
def specific_usrs(discourse_id):
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT orignal_USR_json,USR_ID FROM usr WHERE discourse_id = {0}".format(discourse_id))
        result = cursor.fetchall()
        return jsonify(result), 200
    else:
        return "Could not fetch data", 400


@app.route('/suggestedConcept', methods=['GET', 'POST'])
def suggestedConcept():
    if request.method == "POST":
        data = json.loads(request.data)
        concept = data.get('concept')
        list_of_related_concept = []

        concept_file = open('H_concept-to-mrs-rels.dat', 'r', encoding='utf-8')

        for line in concept_file:
            if line.startswith("("):
                each_line_list = line.split(" ")
                if each_line_list[1].split("_")[0] == concept.split("_")[0]:
                    list_of_related_concept.append(
                        each_line_list[1]+":"+each_line_list[2])

        return jsonify(list_of_related_concept), 200
    else:
        return "Could not fetch concepts!", 400
