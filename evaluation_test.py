from flask import Flask, render_template, request, redirect, send_file, jsonify
from flask import url_for
import pandas as pd
import os
import time
import uuid
import pickle
from tensorflow.keras.models import load_model
# from eunjeon import Mecab
from io import BytesIO, StringIO
from apscheduler.schedulers.background import BackgroundScheduler

import garbege_test
from tensorflow.keras.preprocessing.sequence import pad_sequences


#로컬, 라이브에 따라 변동하는 설정파일
from config import CONFIG

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



#크론(스케줄러) 시작
sched = BackgroundScheduler(daemon=True)
from utils.schedule_func import del_excel_files

#개발 환경이라면 각분의 1초 마다 실행하는 스케쥴 / 라이브환경이라면 매일 01시에 동작하는 스케쥴
#ps 플라스크가 디버그모드로 실행된다면 스캐줄러가 두번 실행됨 참고
if CONFIG.env_name =='DEV':
    sched.add_job(del_excel_files,'cron',minute=1)
elif CONFIG.env_name =="LIVE":
    sched.add_job(del_excel_files,'cron',hour=1)

sched.start()



#시작페이지
@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index_page():
    dir_list = os.listdir(CONFIG.FILE_DIR)
    if len(dir_list) <= 0 :
        return render_template('index.html', users= dir_list, user_files= [])
    else:

        user_files = os.listdir(CONFIG.FILE_DIR+dir_list[0])
        return render_template('index.html', users= dir_list, user_files= user_files)


#정확도 검증 숫자사용 현재 사용 x
@app.route("/validation", methods=['POST'])
def validation_page():
    excel_file_request = request.files['file']
    sheet_number = int(request.form['sheet_number'])
    excel_df = pd.read_excel(excel_file_request, sheet_name=sheet_number)
    json_data = excel_df.to_json(orient='records', double_precision=15, force_ascii=False)
    
    user_name = request.files['user_name']+"/"
    time_format = time.strftime('%m_%d')
    file_name = 'file/'+user_name+ '.xlsx'
    excel_df.to_excel(file_name)
    
    return render_template('validation.html', data=json_data, file_name= "'"+file_name+"'")

#체크박스 정확도검증 페이지 
@app.route("/validation_checkbox", methods=['POST'])
def validation_checkbox_page():
    
    excel_file_request = request.files['file']
    sheet_number = int(request.form['sheet_number'])
    user_name = request.form['user_name']+"/"

    file_name = CONFIG.FILE_DIR+user_name +excel_file_request.filename 
    if os.path.isfile(file_name):
        return "<h1>이미 존재하는 파일입니다.</h1>"
    excel_df = pd.read_excel(excel_file_request, sheet_name=sheet_number)
    if set(['진성여부', '진성여부_comment', 'L1', 'L1_comment','L3', 'L3_comment','L6', 'L6_comment' , 'L7', 'L7_comment']).issubset(excel_df.columns):
        print()
    else:
        excel_df['진성여부'] = '-'
        excel_df['진성여부_comment'] = ''
        excel_df['L1']='-'
        excel_df['L1_comment'] = ''
        excel_df['L3'] = '-'
        excel_df['L3_comment'] = ''
        excel_df['L6'] = '-'
        excel_df['L6_comment'] = ''
        excel_df['L7'] = '-'
        excel_df['L7_comment'] = '-'
        # excel_df['가비지키워드']=''
        excel_df['비고'] =''

    json_data = excel_df.to_json(orient='records', double_precision=15, force_ascii=False)
    

    time_format = time.strftime('%m_%d')
    excel_df.to_excel(file_name)
    
    return render_template('validation_checkbox.html', data=json_data, file_name= "'"+file_name+"'")

#엑셀 확인용 페이지
@app.route("/check", methods=['POST'])
def check_page():
    excel_file_request = request.files['file']
    sheet_number = int(request.form['sheet_number'])
    excel_df = pd.read_excel(excel_file_request, sheet_name=sheet_number)
    keywords= garbege_test.garbage_predict(excel_df)
    excel_df["키워드"]=keywords
    json_data = excel_df.to_json(orient='records', double_precision=15, force_ascii=False)
    
    return render_template('check.html', data=json_data)

#시소러스 검색 페이지
@app.route("/code", methods=['POST'])
def code_page():
    excel_file_request = request.files['file']
    sheet_number = int(request.form['sheet_number'])
    excel_df = pd.read_excel(excel_file_request, sheet_name=sheet_number)
    json_data = excel_df.to_json(orient='records', double_precision=15, force_ascii=False)
    
    return render_template('code.html', data=json_data)

#테스트 시 사용하는 페이지
@app.route("/templat_test", methods=['POST'])
def template_test_page():
    excel_file_request = request.files['file']
    sheet_number = int(request.form['sheet_number'])
    excel_df = pd.read_excel(excel_file_request, sheet_name=sheet_number)
    json_data = excel_df.to_json(orient='records', double_precision=15, force_ascii=False)
    

    time_format = time.strftime('%m_%d')
    file_name = 'file/'+time_format+"_"+str(uuid.uuid4()) + '.xlsx'
    excel_df.to_excel(file_name)

    return render_template('test/validation_test.html', data=json_data, file_name= "'"+file_name+"'")



### 저장 url 사용하지 x
@app.route('/result', methods=['POST'])
def result_page():
    time_format = time.strftime('%m_%d_%H_%M_%S')
    request_json = request.get_json()
    # print(request_json)
    results = pd.DataFrame(request_json)
    results.to_excel("output"+time_format+".xlsx")

    return redirect(url_for('index_page'))

# 다운로드 url
@app.route('/save', methods=['POST'])
def save():
    time_format = time.strftime('%m_%d_%H_%M_%S')

    origin = pd.read_excel(request.form['file_name'])
    results = pd.read_json(request.form['results_tag'])
    # print(request.form['results_tag'])
    origin['진성여부'] = results['진성여부']
    origin['진성여부_comment'] = results['진성여부_comment']
    origin['L1'] = results['L1']
    origin['L1_comment'] = results['L1_comment']
    origin['L3'] = results['L3']
    origin['L3_comment'] = results['L3_comment']
    origin['L6'] = results['L6']
    origin['L6_comment'] = results['L6_comment']
    origin['L7'] = results['L7']
    origin['L7_comment'] = results['L7_comment']
    # origin['가비지키워드'] = results['가비지키워드']
    origin['비고'] = results['비고']
    origin = origin.drop(['Unnamed: 0'], axis=1)

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    #taken from the original question
    origin.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]


    #the writer has done its job
    writer.close()

    #go back to the beginning of the stream
    output.seek(0)

    #finally return the file
    return send_file(output, attachment_filename="testing.xlsx", as_attachment=True)

#test_tamplate에서 테스트에 사용하는 save_test
@app.route('/save_test', methods=['POST'])
def save_test():
    excel_file_request = request.files['file']
    
    excel_file = pd.read_json(excel_file_request)

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    excel_file.to_xml
    #taken from the original question
    excel_file.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]


    #the writer has done its job
    writer.close()

    #go back to the beginning of the stream
    output.seek(0)

    #finally return the file
    return send_file(output, attachment_filename="dir.xlsx", as_attachment=True)
    
# 엑셀 양식 다운로드 url
@app.route('/form_download')
def form_download():
    # excel_form = open('excel_form/cxcel_form.xlsx')
        return send_file(CONFIG.excel_form_dir+'cxcel_form.xlsx',
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    attachment_filename='excel_form.xlsx',# 다운받아지는 파일 이름. 
                     as_attachment=True)


# 가비지 찾아서 새 파일로 다운받기
@app.route('/predict', methods=['POST'])
def predict():

    mecab = CONFIG.mecab()
    tokenizer=pickle.load(open('./deeplearning/premorph_PickleFile.pkl', 'rb'))
    max_len = 300

    origin = pd.read_excel(request.files['file'])
    predict=pd.DataFrame()
    predict['reviews']=origin['제목']+origin['원문']

    loaded_model=load_model("./deeplearning/premorph_ck_model.h5")
    score=[]

    for items in predict['reviews'] :
        
        new_sentence = mecab.morphs(items) # 토큰화
        new_sentence = [word for word in new_sentence if word=='원' or len(word) > 1] # 한글자 제거
        encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
        score.append(float(loaded_model.predict(pad_new))) # 예측

 
    origin['진성여부']=['Y' if i > 0.5 else 'N' for i in score]

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    #taken from the original question
    origin.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]

    writer.close()

    output.seek(0)

    return send_file(output, attachment_filename="garbage_finder.xlsx", as_attachment=True)









































@app.route('/duplicateUserCheck', methods=['POST'])
def duplicateUserCheck():
    
    dir_list = os.listdir(CONFIG.FILE_DIR)
    userName = request.form['userName']

    if userName  in dir_list:
        msg = 'is duplicated'
    else:
        msg = "is not duplicated"
    return {"msg": msg}

@app.route('/makeUser', methods=['POST'])
def makeUser():
    
    dir_list = os.listdir(CONFIG.FILE_DIR)
    userName = request.form['userName']

    if userName  in dir_list:
        msg = 'is duplicated'
    else:
        os.mkdir(CONFIG.FILE_DIR+'/'+userName)
        msg = "is created"
    return {"msg": msg}

@app.route('/search_files', methods=['POST'])
def search_files():
    user_name = request.form['user_name']
    dir_list = os.listdir(CONFIG.FILE_DIR+"/"+user_name)
    
    return {"files": dir_list}

@app.route("/load_validation", methods=['POST'])
def load_validation():
    user_name = request.form["load_user_name_slelct"]
    file_name = request.form["file_names"]
    file_name = CONFIG.FILE_DIR+ user_name+"/" + file_name
    excel_df = pd.read_excel(file_name)
    
    json_data = excel_df.to_json(orient='records', double_precision=15, force_ascii=False)
    

    
    return render_template('validation_checkbox.html', data=json_data, file_name= "'"+file_name+"'")



@app.route('/row_save', methods=['POST'])
def rowsave() :
    data_path = request.form['file_name']
    count = int(request.form['count'])
    row_json = request.form['json_data']
    row_json = row_json.replace('null', '"-"')

    save_data=pd.read_excel(data_path)
    row_data = eval(row_json)
    print(save_data['원문'][count])
    save_data['진성여부'][count]=row_data['진성여부']
    save_data['진성여부_comment'][count]=row_data['진성여부_comment']
    save_data['L1'][count]=row_data['L1']
    save_data['L1_comment'][count]=row_data['L1_comment']
    save_data['L3'][count]=row_data['L3']
    save_data['L3_comment'][count]=row_data['L3_comment']
    save_data['L6'][count]=row_data['L6']
    save_data['L6_comment'][count]=row_data['L6_comment']
    save_data['L7'][count]=row_data['L7']
    save_data['L7_comment'][count]=row_data['L7_comment']
    save_data['비고'][count]=row_data['비고']
    
    
    save_data.to_excel(data_path, index=False)
    return {"msg":"saved"}


### 저장 url 끝
if __name__ ==  "__main__":
    
    print('flaskRun')
    app.run(debug=CONFIG.debug, host=CONFIG.host, port=CONFIG.port)




    
