#!/usr/bin/python3
from mkpy.utility import *
import time, glob

class h:
    @staticmethod
    def f_time(fname):
        res = 0
        tgt_path = pathlib.Path(fname)
        if tgt_path.is_file():
            res = os.stat(fname).st_mtime
        return res

def default():
    target = pers ('last_target', 'database_expl')
    call_user_function(target)

pers ('i', 0)
def anim_next():
    i = pers('i')
    i = i+1

    base = 'svg/alg_1'
    svg_path = pathlib.Path(base+'_'+str(i)+'.svg')
    if not svg_path.is_file():
        if get_cli_option('-d'):
            if i>1:
                ex ('cp alg_1_'+str(i-1)+'.svg '+filename)
            else:
                print('-d inválida no hay frame anterior')
        else:
            ex ('cp '+base+'.svg '+str(svg_path))

    pers('i', value=i)
    ex ('inkscape '+str(svg_path)+' 2>/dev/null&')

def anim_reset():
    v = int(get_cli_option('-v', has_argument=True))
    set_val = 0
    if v != None:
        set_val = int(v)
    pers('i', value=v)

def svg_update():
    target_filenames = []
    tex_filename = 'presentacion.tex'
    first_run = True
    while True:
        try:
            svg_files = glob.glob ('svg/*')
            svg_files.sort()

            tex_time = os.stat(tex_filename).st_mtime
            pdf_time = h.f_time(os.path.splitext(tex_filename)[0]+'.pdf')
            if tex_time > pdf_time or first_run:
                files = []
                target_filenames = []
                for f in svg_files:
                    base = os.path.splitext(os.path.basename(f))[0]
                    files.append (base+'\\.');
                target_filenames = ex ('grep -o -P \'('+'|'.join (files)+').*\\b\' '+tex_filename, ret_stdout=True, echo=False).splitlines()
                target_filenames.sort()

            i_src = 0
            for i_tgt in range(len(target_filenames)):
                tgt_name = os.path.splitext(os.path.basename(target_filenames[i_tgt]))[0]
                svg_name = os.path.splitext(os.path.basename(svg_files[i_src]))[0]
                while (tgt_name != svg_name):
                    i_src = i_src + 1
                    tgt_name = os.path.splitext(os.path.basename(target_filenames[i_tgt]))[0]
                    svg_name = os.path.splitext(os.path.basename(svg_files[i_src]))[0]

                src_time = os.stat(svg_files[i_src]).st_mtime
                out_time = h.f_time (target_filenames[i_tgt])

                if src_time > out_time:
                    if os.path.splitext(target_filenames[i_tgt])[1] == '.png':
                        ex ('inkscape --export-png='+target_filenames[i_tgt]+' '+svg_files[i_src]+' 2>/dev/null')
                    elif os.path.splitext(target_filenames[i_tgt])[1] == '.pdf_tex':
                        pdf_name = os.path.splitext(target_filenames[i_tgt])[0] + '.pdf'
                        ex ('inkscape --export-latex --export-pdf='+pdf_name+' '+svg_files[i_src]+' 2>/dev/null')
                    elif os.path.splitext(target_filenames[i_tgt])[1] == '.pdf':
                        ex ('inkscape --export-pdf='+target_filenames[i_tgt]+' '+svg_files[i_src]+' 2>/dev/null')


            #if tex_time > pdf_time:
            #    retval = ex ('latexmk -interaction=nonstopmode -pdf '+tex_filename, no_stdout=True)
            #    while retval != 0:
            #        ex (
            #        error_time = tex_time
            #        time.sleep (1)
            #        tex_time = os.stat(tex_filename).st_mtime
            #        if error_time < tex_time:
            #            retval = ex ('latexmk -interaction=nonstopmode -pdf '+tex_filename, no_stdout=True)
            first_run = False
            time.sleep (1)
        except KeyboardInterrupt:
            print ()
            break

if __name__ == "__main__":
    pymk_default()

