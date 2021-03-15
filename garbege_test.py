import pandas as pd 
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
from collections import Counter
from config import CONFIG

max_len =300
mecab = CONFIG.mecab()
tokenizer = pickle.load(open('./deeplearning/premorph_PickleFile.pkl', 'rb',))
garbage_words=pickle.load(open('./deeplearning/garbage_words_tokenizer_PickleFile.pkl', 'rb',))
loaded_model=load_model("./deeplearning/premorph_ck_model.h5")

def garbage_predict(data):
    df = pd.DataFrame()

    df['text'] =data['제목'] + data['원문']
    df['text'] = df['text'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")


    df['tokenized'] = df['text'].apply(mecab.morphs)
    df['tokenized'] = df['tokenized'].apply(lambda x : [item for item in x if len(item) > 1] )

    X_predict = df['tokenized'].values
    X_predict_encoded = tokenizer.texts_to_sequences(X_predict)
    X_predict_pad = pad_sequences(X_predict_encoded, maxlen=max_len)

    # print(X_predict[0])
    Y_predict = loaded_model.predict(X_predict_pad)
    keyword=[]
    word=[]
    garbage_list=garbage_words.tolist()

    for i in range(len(Y_predict)) :
        if (Y_predict[i] <= 0.5):
            for j in range(len(df['tokenized'][i])) :
                if df['tokenized'][i][j] in garbage_list :
                    word.append(df['tokenized'][i][j])
                    word=list(set(word))
            word=["{:.2f}% 확률로 진성 데이터입니다".format((Y_predict[i][0]) * 100)+" \n   ====> 머신러닝 가비지 패턴 : "]+word
            keyword.append(word)
            word=[]
        else :
            keyword.append(["{:.2f}% 확률로 진성 데이터입니다.".format(Y_predict[i][0] * 100)])
    return keyword


if __name__ =="__main__":
    data = pd.read_excel('LGE_PP_공기청정기_1672건_1Q_만기.xlsx')
    garbage_predict(data)
