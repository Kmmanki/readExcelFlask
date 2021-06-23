import sys

CONFIG = None
class Dev_config:
    env_name="DEV"
    excel_form_dir = "C:/Users/A61590/Desktop/evaluatuon_git/excel_form/"
    FILE_DIR='D:/File/'
    debug=True
    host='localhost'
    remove_day = 1
    '''
    no Tensor
    from eunjeon import Mecab
    mecab = Mecab
    '''
    port = 5000


class Live_config:
    env_name="LIVE"
    FILE_DIR='/mnt/disks/app001/userFile/'
    excel_form_dir = "/mnt/disks/app001/excel_form"

    debug=False
    host='?'
    remove_day = 31
    '''
    no Tensor
    from konlpy.tag import Mecab
    mecab = Mecab
    '''
    port = 5000

class Live_Test_config:
    env_name="LIVE"
    FILE_DIR='/home/sysadm01/analysis-work/userFile/'
    excel_form_dir = "/home/sysadm01/analysis-work/excel_form/"

    debug=False
    host='?'
    remove_day = 31
    '''
    no Tensor
    from konlpy.tag import Mecab
    mecab = Mecab
    '''
    port = 5001

#실행 시 첫 번째 파라미터가 LIVE 라면 / 라이브클래스 / 아니라면 DEV 클래스
if len(sys.argv) > 1 and sys.argv[1] =='LIVE':
        CONFIG = Live_config()
elif len(sys.argv) > 1 and sys.argv[1] =='LIVE_TEST':
    CONFIG = Live_Test_config()
else:
        CONFIG = Dev_config()



