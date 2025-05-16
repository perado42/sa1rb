import unittest

from io import StringIO, BytesIO
from json import load as json_load

import sa1rb
from sa1rb import html_with_artwork_to_json



class TestHtmlWithArtworkToJson( unittest.TestCase ):


    def test_basic_noscript( self ):

        f_outp_json = StringIO()

        f_inp_html \
          = BytesIO(
                r"""
                <html>
                <div data-attrid="kc:/visual_art/visual_artist:works">

                <div>
                <a href="/href1">
                <img id="img1" src="img1-src">
                <div>
                  <div>title1</div>
                  <div>extra1</div>
                </div>
                </a>
                </div>

                <div>
                <a href="/href2">
                <img id="img2" src="img2-src">
                <div>
                  <div>title2</div>
                  <div>extra2</div>
                  <div>extra3</div>
                </div>
                </a>
                </div>

                </div>
                </html>
                """.encode( "utf-8" ) )
        
        html_with_artwork_to_json( f_inp_html, f_outp_json )

        f_outp_json.seek( 0 )
        outp_json = json_load( f_outp_json )

        self.assertIn( "artworks", outp_json )

        artworks = outp_json[ "artworks" ]

        self.assertEqual( len(artworks), 2 )

        self.assertEqual( artworks[ 0 ][ "name" ], "title1" )
        self.assertEqual( artworks[ 0 ][ "link" ], "https://www.google.com/href1" )
        self.assertEqual( artworks[ 0 ][ "extensions" ], [ "extra1" ] )
        self.assertEqual( artworks[ 0 ][ "image" ], "img1-src" )

        self.assertEqual( artworks[ 1 ][ "name" ], "title2" )
        self.assertEqual( artworks[ 1 ][ "link" ], "https://www.google.com/href2" )
        self.assertEqual( artworks[ 1 ][ "extensions" ], [ "extra2", "extra3" ] )
        self.assertEqual( artworks[ 1 ][ "image" ], "img2-src" )


    def test_no_artwork_1( self ):

        f_outp_json = StringIO()

        f_inp_html \
          = BytesIO(
                r"""
                <html>
                <div>

                <div>
                <a href="/href1">
                <img id="img1" src="img1-src">
                <div>
                  <div>title1</div>
                  <div>extra1</div>
                </div>
                </a>
                </div>

                <div>
                <a href="/href2">
                <img id="img2" src="img2-src">
                <div>
                  <div>title2</div>
                  <div>extra2</div>
                  <div>extra3</div>
                </div>
                </a>
                </div>

                </div>
                </html>
                """.encode( "utf-8" ) )
        
        html_with_artwork_to_json( f_inp_html, f_outp_json )

        f_outp_json.seek( 0 )
        outp_json = json_load( f_outp_json )

        self.assertNotIn( "artworks", outp_json )


    def test_no_artwork_2( self ):

        f_outp_json = StringIO()

        f_inp_html \
          = BytesIO(
                r"""
                <html>
                <div data-attrid="kc:/visual_art/visual_artist:works">
                </div>
                </html>
                """.encode( "utf-8" ) )
        
        html_with_artwork_to_json( f_inp_html, f_outp_json )

        f_outp_json.seek( 0 )
        outp_json = json_load( f_outp_json )

        self.assertNotIn( "artworks", outp_json )


    def test_complicated_with_script( self ):

        f_outp_json = StringIO()

        f_inp_html \
          = BytesIO(
                r"""
                <html>

                <script></script>

                <script>
                foobar();
                </script>

                <script>
                foobar();
                _setImagesSrc(null, null, null);
                </script>

                <script>
                (function () {
                    var s =
                        "img1-actual-src";
                    var ii = ["img1"];
                    var r = "";
                    _setImagesSrc(ii, s, r);
                })();
                </script>

                <script>
                (function () {
                    var s =
                        "img2-actual-src";
                    var ii = "img2";
                    var r = "";
                    _setImagesSrc(ii, s, r);
                })();
                </script>

                <div data-attrid="kc:/visual_art/visual_artist:works">

                <div>
                <a href="/href1">
                <img id="img1" src="img1-placeholder-src">
                <div>
                  <div>title1</div>
                  <div>extra1</div>
                </div>
                </a>
                </div>

                <div><div>
                <a href="/href2">
                <img id="img2" src="img2-placeholder-src">
                <div>
                  <div>title2</div>
                  <div>extra2</div>
                  <div>extra3</div>
                </div>
                </a>
                </div></div>

                </div>
                </html>
                """.encode( "utf-8" ) )
        
        html_with_artwork_to_json( f_inp_html, f_outp_json )

        f_outp_json.seek( 0 )
        outp_json = json_load( f_outp_json )

        self.assertIn( "artworks", outp_json )

        artworks = outp_json[ "artworks" ]

        self.assertEqual( len(artworks), 2 )

        self.assertEqual( artworks[ 0 ][ "name" ], "title1" )
        self.assertEqual( artworks[ 0 ][ "link" ], "https://www.google.com/href1" )
        self.assertEqual( artworks[ 0 ][ "extensions" ], [ "extra1" ] )
        self.assertEqual( artworks[ 0 ][ "image" ], "img1-actual-src" )

        self.assertEqual( artworks[ 1 ][ "name" ], "title2" )
        self.assertEqual( artworks[ 1 ][ "link" ], "https://www.google.com/href2" )
        self.assertEqual( artworks[ 1 ][ "extensions" ], [ "extra2", "extra3" ] )
        self.assertEqual( artworks[ 1 ][ "image" ], "img2-actual-src" )


    def test_malformed_1( self ):

        f_outp_json = StringIO()

        f_inp_html \
          = BytesIO(
                r"""
                <html>
                <div data-attrid="kc:/visual_art/visual_artist:works">

                <div>
                <a href="/mf1-href">
                <img id="mf1-img1" src="mf1-img1-src">
                <img id="mf1-img2" src="mf1-img2-src">
                <div>
                  <div>mf1-title</div>
                  <div>mf1-extra</div>
                </div>
                </a>
                </div>

                <div>
                <a href="/mf2-href">
                <img id="mf2-img1" src="mf2-img1-src">
                <div>
                </div>
                </a>
                </div>

                <div>
                <a>
                <img id="mf3-img1" src="mf3-img1-src">
                <div>
                  <div>mf3-title</div>
                  <div>mf3-extra</div>
                </div>
                </a>
                </div>

                <div>
                <a href="/href1">
                <img id="img1" src="img1-src">
                <div>
                  <div>title1</div>
                  <div>extra1</div>
                </div>
                </a>
                </div>

                </div>
                </html>
                """.encode( "utf-8" ) )

        html_with_artwork_to_json( f_inp_html, f_outp_json )

        print( f_outp_json.getvalue() )

        f_outp_json.seek( 0 )
        outp_json = json_load( f_outp_json )

        self.assertIn( "artworks", outp_json )

        artworks = outp_json[ "artworks" ]

        self.assertEqual( len(artworks), 1 )

        self.assertEqual( artworks[ 0 ][ "name" ], "title1" )
        self.assertEqual( artworks[ 0 ][ "link" ], "https://www.google.com/href1" )
        self.assertEqual( artworks[ 0 ][ "extensions" ], [ "extra1" ] )
        self.assertEqual( artworks[ 0 ][ "image" ], "img1-src" )



if __name__ == '__main__': # pragma: no cover

    unittest.main() # pragma: no cover
