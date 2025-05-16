"""
Richard's Submission to SerpApi's Code Challenge:
main program
"""

from os.path import isfile

from glob import glob
from itertools import chain

from sa1rb import html_with_artwork_to_json
from sa1rb import json_to_html



def main( cmd=None ):
    """main entrypoint"""

    try:

        if cmd is None:

            fns = glob( "files/*.html" )

            for fn_inp in fns:
                if fn_inp.endswith( "-unminified.html" ):
                    continue
                if fn_inp.endswith( "-recomposed.html" ):
                    continue
                print( fn_inp )
                assert fn_inp.endswith( ".html" )
                fn_outp = fn_inp[ :-len(".html") ] + "-artwork.json"

                html_with_artwork_to_json( fn_inp, fn_outp )

        elif cmd == "recompose":

            fns \
              = chain(
                    glob( "files/expected-array.json" ),
                    glob( "files/*-artwork.json" ) )

            for fn_inp in fns:
                print( fn_inp )
                assert fn_inp.endswith( ".json" )
                fn_outp = fn_inp[ :-len(".json") ] + "-recomposed.html"

                json_to_html( fn_inp, fn_outp )

    except:

        if not isfile( "files/van-gogh-paintings.html" ):
            print( "!!!", "files/van-gogh-paintings.html not found" )
            print( "!!!",
                "note: the main program must be run with the repo root as "
              + "its current working dir" )

        raise


if __name__ == "__main__":

    import sys
    main( *sys.argv[1:] )
