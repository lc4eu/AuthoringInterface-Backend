from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
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

# from client.src.Navigation import login
# from flask_restx import Api, Resource, fields
# import jwt
# from .models import db, Users
# from flask_restx import Api, Resource, fields
# import jwt
# from .models import db, Users

Session(app)
CORS(app)
auth_id = 1
dis_id = 0


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        email = data.get('email')
        password = data.get('password')
        reviewer_role = data.get('reviewer_role')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT author_id, author_name, email, reviewer_role FROM author WHERE email = % s AND password = % s ', (email, password))
        author = cursor.fetchone()
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
# @login_required
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
        row_id = cursor.lastrowid
        list_usr = list(displayUSR(discourse))

        # saving generated usr in database in usr table
        for i in range(len(list_usr)):
            cursor.execute("INSERT INTO usr(author_id,discourse_id,sentence_id,orignal_USR_json,USR_status) VALUES(%s,%s,%s,%s,%s)",
                           (author_id, row_id, i+1, list_usr[i], "In Edit"))
            cursor.execute("INSERT INTO edit(author_id,discourse_id,sent_id,edited_USR,status) VALUES(%s,%s,%s,%s,%s)",
                           (author_id, row_id, i+1, list_usr[i], "In Edit"))
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

        return jsonify(message='USR Generated!'), 200
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
        # generated_usrs[file]=usr_dict
        gs.append(usr_dict)
    return gs
    # return jsonify(generated_usrs)


@app.route('/fileinsert', methods=['POST'])
def fileinsert():
    global dis_id
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
        row_id = cursor.lastrowid
        dis_id = row_id

        for i in range(no_sentences):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "INSERT INTO usr(author_id, discourse_id, orignal_USR_json, USR_status) VALUES(%s, %s, %s, %s)", (author_id, dis_id, jsondata[i], "In Edit"))
            mysql.connection.commit()
            usrid = cursor.lastrowid
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO edit(author_id, discourse_id, edited_USR, status, USR_ID, sent_id) VALUES(%s, %s, %s, %s, %s, %s)",
                           (author_id, dis_id, jsondata[i], "In Edit", usrid, '2'))
            mysql.connection.commit()

    return redirect(url_for('orignal_usr_fetch'))


@app.route('/orignal_usr_fetch', methods=['GET'])
def orignal_usr_fetch():
    if request.method == 'GET':
        global dis_id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # print("Hello ",dis_id)
        query = 'SELECT e1.usr_id, e1.edited_usr, e1.edit_date,e1.status FROM edit e1 INNER JOIN ( SELECT usr_id, MAX(edit_date) AS max_edit_date FROM edit WHERE discourse_id =%s GROUP BY usr_id ) e2 ON e1.usr_id = e2.usr_id AND e1.edit_date = e2.max_edit_date WHERE e1.discourse_id = %s ORDER BY e1.usr_id'
        params = (dis_id, dis_id)
        cursor.execute(query, params)
        data = cursor.fetchall()
        return jsonify(data), 200
    else:
        return "Data could not be fetched because of some error!", 400


@app.route('/specific_usrs/<discourse_id>', methods=['GET'])
def specific_usrs(discourse_id):
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT orignal_USR_json FROM usr WHERE discourse_id = {0}".format(discourse_id))
        result = cursor.fetchall()
        return jsonify(result), 200
    else:
        return "Could not fetch data", 400


@app.route('/specific_discoursename/<discourse_id>', methods=['GET'])
def specific_discoursename(discourse_id):
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT discourse_name FROM discourse WHERE discourse_id = {0}".format(discourse_id))
        result = cursor.fetchaone()
        return jsonify(result), 200
    else:
        return "Could not fetch data", 400


@app.route('/specific_sentence/<discourse_id>')
def specific_sentence(discourse_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT sentences FROM discourse WHERE discourse_id= {0}".format(discourse_id))
    response = cursor.fetchone()
    return jsonify(response), 200


@app.route('/specific_discourse_usr/<discourse_id>')
def specific_discourse_usr(discourse_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT USR_ID,USR_status,create_date,orignal_USR_json FROM usr WHERE discourse_id= {0}'.format(discourse_id))
    response = cursor.fetchall()
    return jsonify(response), 200


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


@ app.route('/authors')
def author():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT author_id, author_name, email, password, reviewer_role FROM author")
        authRows = cursor.fetchall()
        respone = jsonify(authRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@ app.route('/discourse')
def discourse():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT discourse_id, author_id, no_sentences, domain,create_date, other_attributes, sentences, discourse_name FROM discourse")
        disRows = cursor.fetchall()
        respone = jsonify(disRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@ app.route('/USR')
def USR():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM usr")
        usrRows = cursor.fetchall()
        respone = jsonify(usrRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@ app.route('/USR/<USR_ID>')
def usr_details(USR_ID):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT author_id, discourse_id, sentence_id, USR_ID, orignal_USR_json, final_USR, create_date, USR_status FROM usr WHERE discourse_id =%s", [USR_ID])
        usrRow = cursor.fetchall()
        respone = jsonify(usrRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/getUSRid')
def getusrid():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT USR_ID FROM usr WHERE discourse_id = % s AND author_id = %s', (dis_id, session["author_id"]))
    usr_id = cursor.fetchall()
    respone = jsonify(usr_id)
    respone.status_code = 200
    return respone


@app.route('/editusr/', methods=['GET', 'POST'])
@cross_origin()
def editusr():
    if request.method == "POST":
        # email = session.get('email')
        # print(email)
        author_id = session["author_id"]
        discourse_id = dis_id
        data = request.get_json()
        finalJson = data.get('finalJson')
        usrid = data.get('usrid')
        print("Editusr usrid:", usrid)
        # edit_usr = request.get_json()
        # sentence_id = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO edit(author_id, discourse_id, edited_USR, status, usr_id) VALUES(%s,%s,%s,%s,%s)",
                       (author_id, dis_id, finalJson, "In Edit", usrid))
        mysql.connection.commit()
        # print(email, author_id, discourse_id)
        dat = {'message': 'Edited Successfully!!!'}
    return jsonify(dat)
    # return jsonify(message='Edited Successfully!')


@app.route('/editstatus/', methods=['GET', 'POST'])
def editstatus():
    if request.method == "POST":
        author_id = session["author_id"]
        discourse_id = dis_id
        data = request.get_json()
        status = data.get('status')
        usrid = data.get('usrid')
        print(status)
        print(usrid)
        # sentence_id = data.get('sentence_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "UPDATE edit SET status=%s WHERE usr_id=%s and discourse_id=%s AND author_id = %s", (status, usrid, dis_id, author_id))
        mysql.connection.commit()
        # print(email, author_id, discourse_id)
        dat = {'message': 'Status updated successfully'}
    return jsonify(dat)


@app.route('/get_edit_usr', methods=['GET'])
def get_edit_usr():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT edit_id, author_id, discourse_id, edited_USR, status, sent_id, edit_date FROM edit WHERE author_id = %s", session["author_id"])
        usrRows = cursor.fetchall()
        respone = jsonify(usrRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/sentence_id_fetch')
def sentence_id_fetch():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT sent_id FROM edit WHERE discourse_id = % s ', (dis_id, ))
    sent_id = cursor.fetchall()
    respone = jsonify(sent_id)
    respone.status_code = 200
    return respone


def disc_id():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT discourse_id FROM discourse ORDER BY discourse_id DESC LIMIT 1;")
    dis_id = cursor.fetchall()
    a = dis_id[0]
    dis_id = a["discourse_id"]
    mysql.connection.commit()
    return dis_id


@app.route('/view_btn_data')
def orignal_usr_fetch2():
    dis_id = request.args.get('dis_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM discourse JOIN edit ON discourse.discourse_id=edit.discourse_id WHERE edit.discourse_id={0}'.format(dis_id))
    view_data = cursor.fetchall()
    response = jsonify(view_data)
    response.status_code = 200
    mysql.connection.commit()
    return response


@app.route('/delete_discourse')
def delete_discourse():
    dis_id = request.args.get('dis_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        'DELETE FROM edit WHERE edit.discourse_id={0}'.format(dis_id))
    cursor.execute(
        'DELETE FROM usr WHERE usr.discourse_id={0}'.format(dis_id))
    cursor.execute(
        'DELETE FROM discourse WHERE discourse.discourse_id={0}'.format(dis_id))
    mysql.connection.commit()
    # return "Done",200
    return redirect("http://localhost:3000/dashboard")


@app.route('/update_status')
def update_status():
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


@app.route('/semcateofnouns', methods=['GET'])
def get_nouns():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM semcateofnouns;")
        result = cursor.fetchall()
        return jsonify(result), 200
    else:
        return "Data could not be fecthed", 400


@app.route('/dbsentencetype/', methods=['GET'])
def get_sentencetype():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM sentencetype;")
    result = cursor.fetchall()
    return jsonify([dict(row) for row in result])


@app.route('/dbspeakersview/', methods=['GET'])
def get_speakersview():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM speakersview;")
    result = cursor.fetchall()
    return jsonify([dict(row) for row in result])


@app.route('/dbdeprelation/', methods=['GET'])
def get_deprelation():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM deprelation;")
    result = cursor.fetchall()
    return jsonify([dict(row) for row in result])
