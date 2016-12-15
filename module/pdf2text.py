import subprocess


def pdf2txt(pdf_file):
    NODE_EXECUTABLE = 'node'
    PDFJS_GETINFO = ('/usr/local/pdf.js/examples/node'
                     + '/getinfo_txtonly.js')

    # python2:
    # proc = subprocess.Popen([NODE_EXECUTABLE, PDFJS_GETINFO, pdf_file],
    #                         stdout=subprocess.PIPE)
    # outs = iter(proc.stdout.readline, '')

    # Python3
    proc = subprocess.Popen([NODE_EXECUTABLE, PDFJS_GETINFO, pdf_file],
                            stdout=subprocess.PIPE)
    outs, errs = proc.communicate()

    texts = list()

    # Python2
    # for line in outs:
    # Python3
    for line in outs.decode('utf-8').splitlines():
        texts.append(line)

    return texts


if __name__ == '__main__':
    texts = pdf2txt('./test1.pdf')

    for text in texts:
        print(text)
        print('------------------------------------------------------')

    print("number of pages = {}".format(len(texts)))