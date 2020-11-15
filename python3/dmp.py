import gc
import os
import sys
import time
import pathlib
import webbrowser

import diff_match_patch as dmp_module

import click

@click.group()
def cli():
    pass

@cli.command(help='Calculates diff of 2 files')
@click.argument('file1')
@click.argument('file2')
def diff(file1, file2):
    here = pathlib.Path(__file__).parent.absolute()
    cwd = pathlib.Path().parent.absolute()

    text1 = open(cwd / file1).read()
    text2 = open(cwd / file2).read()

    dmp = dmp_module.diff_match_patch()
    dmp.Diff_Timeout = 0.0

    # Execute one reverse diff as a warmup.
    res = dmp.diff_main(text2, text1, False)

    dmp.diff_cleanupSemantic(res)
    res = dmp.diff_prettyHtml(res)

    with open(here / 'tmp' / 'tmp_dump.html','w') as res_html:
        res_html.write(res)

    new = 2 # open in a new tab, if possible

    #  open an HTML file on my own (Windows) computer
    url = f"file:///{here / 'tmp_dump.html'}"
    webbrowser.open(url,new=new)

    gc.collect()
    start_time = time.time()
    dmp.diff_main(text1, text2, False)
    end_time = time.time()
    print("Elapsed time: %f" % (end_time - start_time))


def run():
    cli(prog_name='dmp')


if __name__ == "__main__":
    run()
