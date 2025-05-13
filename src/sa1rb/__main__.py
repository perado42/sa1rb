"""Richard's Submission to SerpApi's Code Challenge: Main Program."""

from os.path import isfile

from sa1rb import paintings_html_to_json



def main():
    """main entrypoint"""

    try:

        paintings_html_to_json(
            "files/van-gogh-paintings.html",
            "files/van-gogh-paintings-converted.json" )

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
