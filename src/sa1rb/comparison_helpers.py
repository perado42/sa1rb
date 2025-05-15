"""Richard's Submission to SerpApi's Code Challenge: various comparison helper functions."""

from yaml import load_all as yaml_load_all
from yaml import Loader
from json import load as json_load
from glob import glob

from pprint import pprint
from itertools import chain


def preprocess_json_for_comparison( fn_inp_json, fn_outp_yaml ):

    fns \
      = chain(
            glob( "files/expected-array.json" ),
            glob( "files/*-carousel.json" ) )

    for fn_inp in fns:

        print( fn_inp )

        assert fn_inp.endswith( ".json" )
        fn_outp = fn_inp[ :-len(".json") ] + ".yaml"

        doc = None
        with open( fn_inp, "rt", encoding="utf-8" ) as inp_f:
            doc = json_load( inp_f )

        with open( fn_outp, "wt", encoding="utf-8" ) as outp_f:

            for artwork in doc[ "artworks" ]:

                outp_f.write( "---\n" )

                outp_f.write( "name: {}\n".format( repr( artwork["name"] ) ) )

                ext = artwork.get( "extensions" )
                if ext:
                    outp_f.write( "extensions: {}\n".format( repr( ext ) ) )

                outp_f.write( "link: {}\n".format( repr( artwork["link"] ) ) )

                image = artwork.get( "image" )
                if image:
                  outp_f.write( "image: {}\n".format( repr( artwork["image"] ) ) )

        with open( fn_outp, "rt", encoding="utf-8" ) as f:
            for doc in yaml_load_all( f, Loader ):
                # pprint( doc )
                pass
