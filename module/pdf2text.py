import subprocess


class Pdf2Text:

    def __init__(self):
        pass

    def pdf2text(self, file_name, file_path):
        chk = 0
        try:
            NODE_EXECUTABLE = 'node'
            PDFJS_GETINFO = ('/usr/local/src/sungjin/pdf.js/' + 'examples/node/getinfo_txtonly.js')
            filePath = file_path + file_name
            proc = subprocess.Popen([NODE_EXECUTABLE, PDFJS_GETINFO, filePath],stdout=subprocess.PIPE)
            texts = list()
            for line in iter(proc.stdout.readline, ''):
                texts.append(line)

           
        except:
            print ("pdf to text error")
            chk = 1
        if(chk == 0):
            print ("pdf2text가 정상 출력되었습니다")
            return texts
        else :
            return "pdf2textError"
