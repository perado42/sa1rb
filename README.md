# Extract Van Gogh Paintings

## About Richard's Submission

### Installation

```
python3 -mvenv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -e .
```

### Step 1. Simple Usage

You can generate the `*-carousel.json` files from the corresponding `.html` files as follows.
(So, this is the main solution to the challenge)
```
python3 -m sa1rb
```

### Step 2. Ad-Hoc Debugging

Having done that, you can use the following to convert the `.json` files to `.yaml` files with canonical field ordering.  These are useful for debugging.
```
python3 -m sa1rb preprocess-json-for-comparison
diff files/expected-array.yaml files/van-gogh-paintings-carousel.yaml
```
If the diff has any differences to report, then something went wrong in the above step.


## About the Challenge

Goal is to extract a list of Van Gogh paintings from the attached Google search results page.

![Van Gogh paintings](https://github.com/serpapi/code-challenge/blob/master/files/van-gogh-paintings.png?raw=true "Van Gogh paintings")

### Instructions

This is already fully supported on SerpApi. ([relevant test], [html file], [sample json], and [expected array].)
Try to come up with your own solution and your own test.
Extract the painting `name`, `extensions` array (date), and Google `link` in an array.

Fork this repository and make a PR when ready.

Programming language wise, Ruby (with RSpec tests) is strongly suggested but feel free to use whatever you feel like.

Parse directly the HTML result page ([html file]) in this repository. No extra HTTP requests should be needed for anything.

[relevant test]: https://github.com/serpapi/test-knowledge-graph-desktop/blob/master/spec/knowledge_graph_claude_monet_paintings_spec.rb
[sample json]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/van-gogh-paintings.json
[html file]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/van-gogh-paintings.html
[expected array]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/expected-array.json

Add also to your array the painting thumbnails present in the result page file (not the ones where extra requests are needed). 

Test against 2 other similar result pages to make sure it works against different layouts. (Pages that contain the same kind of carrousel. Don't necessarily have to be paintings.)

The suggested time for this challenge is 4 hours. But, you can take your time and work more on it if you want.
