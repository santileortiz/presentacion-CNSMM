#!/usr/bin/python3
from mkpy.utility import *

def default():
    target = pers ('last_target', 'database_expl')
    call_user_function(target)

pers ('i', 1)
def alg_1_next():
    i = pers('i')
    i = i+1

    filename = 'alg_1_'+str(i)+'.svg'
    svg_path = pathlib.Path(filename)
    if not svg_path.is_file():
        if get_cli_option('-d'):
            ex ('cp alg_1_'+str(i-1)+'.svg '+filename)
        else:
            ex ('cp alg_1.svg alg_1_'+filename)

    pers('i', value=i)
    ex ('inkscape alg_1_'+str(i)+'.svg&')

def alg_1_to_pdf():
    i = 1
    filename = 'alg_1_'+str(i)

    svg_path = pathlib.Path(filename+'.svg')
    while svg_path.is_file():
        ex ('inkscape --export-pdf='+filename+'.pdf '+filename+'.svg')
        i = i+1
        filename = 'alg_1_'+str(i)
        svg_path = pathlib.Path(filename+'.svg')

def alg_1_reset():
    i_opt = get_cli_option('-i', has_argument=True)
    set_val = 0
    if i_opt != None:
        set_val = int(i_opt)
    pers('i', value=set_val)

if __name__ == "__main__":
    pymk_default()

