"""Richard's Submission to SerpApi's Code Challenge: main program."""

from os.path import isfile

from sa1rb import html_with_carousel_to_json
from sa1rb import preprocess_json_for_comparison



def main( cmd=None ):
    """main entrypoint"""

    try:

        if cmd is None:
            
            html_with_carousel_to_json(
                "files/van-gogh-paintings.html",
                "files/van-gogh-paintings-carousel.json" )

        elif cmd == "preprocess-json-for-comparison":

            preprocess_json_for_comparison(
                "files/expected-array.json",
                "files/expected-array.yaml" )

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
