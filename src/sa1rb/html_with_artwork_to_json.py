"""
Richard's Submission to SerpApi's Code Challenge:
html_with_artwork_to_json function.
"""

from json import dump as json_dump # pragma: no cover

from bs4 import BeautifulSoup # pragma: no cover
from py_mini_racer import MiniRacer, JSEvalException # pragma: no cover

ARTWORK_KCs = [ # pragma: no cover
      "kc:/visual_art/visual_artist:works",
      "kc:/architecture/architect:designed" ]


def html_with_artwork_to_json( f_inp_html, f_outp_json ): # pragma: no cover
    """Extract Van Gogh Paintings from HTML to JSON"""


    soup = None
    soup = BeautifulSoup( f_inp_html.read(), features="html.parser" )


    image_by_id = {}

    for script_ in soup.find_all( "script" ):

        script = script_.string
        if not script:
            continue
        if "_setImagesSrc" not in script:
            continue

        script = script.strip()

        jsctx = MiniRacer()
        jsctx.eval( r"""
            CAPTURED_II = null;
            CAPTURED_S = null;
            function _setImagesSrc( ii, s, r ) {
                CAPTURED_II = ii;
                CAPTURED_S = s;
            }
            """ )

        ii = None
        s = None

        try:
            jsctx.eval( script )  # SECURITY!!!  I wouldn't do this in
            # production, but for purposes of this challenge, it'll do.
        except JSEvalException:
            pass

        ii = jsctx.eval( "CAPTURED_II" )
        s = jsctx.eval( "CAPTURED_S" )

        if ii and isinstance( s, str ):
            if isinstance( ii, str ):
                ii = [ ii ]
            for image_id in ii:
                image_by_id[ image_id ] = s


    hrefs_seen = set()

    artworks = []

    for kc in ARTWORK_KCs:

        for container in soup.find_all( attrs = { "data-attrid": kc } ):

            for record in container.find_all( "div" ):

                links = record.find_all( "a", limit=2 )
                imgs = record.find_all( "img", limit=2 )
                strings = []
                for div in record.find_all( "div" ):
                    if div.string:
                        stripped = div.string.strip()
                        if not stripped:
                            continue
                        if stripped not in strings:
                            strings.append( stripped )

                if not len(links) == 1:
                    continue
                if not len(imgs) == 1:
                    continue
                if not len(strings) >= 1:
                    continue

                link_href = links[0].get( "href" )
                if not link_href:
                    continue

                link_href = "https://www.google.com" + link_href

                if link_href in hrefs_seen:
                    continue
                hrefs_seen.add( link_href )

                img_id = imgs[0].get( "id" )

                new_artwork \
                  = { "name": strings[ 0 ],
                      "link": link_href }

                image = None
                if img_id in image_by_id:
                    image = image_by_id.get( img_id, None )
                if not image:
                    image = imgs[0].get( "data-src", None )
                if not image:
                    image = imgs[0].get( "src", None )

                if image:
                    new_artwork[ "image" ] = image

                if len( strings ) > 1:
                    new_artwork[ "extensions" ] = strings[ 1: ]

                artworks.append( new_artwork )


    if artworks:
        json_dump(
            { "artworks": artworks },
            f_outp_json,
            indent=2, ensure_ascii=False )

    else:
        json_dump(
            {},
            f_outp_json,
            indent=2, ensure_ascii=False )
