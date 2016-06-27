import pytest

from template import template
import matplotlib.pyplot as plt

# def test_dict_merge():
# 
#     input_dict1 = dict(x=1,y=dict(g=7,z=9),p=3)
#     input_dict2 = dict(x=1,y=dict(h=8,g=8),p=5)
#     
#     expected_out = dict(x=1,y=dict(h=8,g=8,z=9),p=5)
#  
#     result = template._dict_merge(input_dict1, input_dict2)
#     
#     assert expected_out == result

@pytest.mark.parametrize(('size','scale','expected'),[(100,.5,(-50,150)),(20,1.5,(10/3.,20-10/3.))])
def test_calc_extents(size, scale, expected):
    
    lower,upper = template._calc_extents(size, scale)
    
    assert abs(lower-expected[0]) < 0.0001
    assert abs(upper-expected[1]) < 0.0001
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_blank():

    testfig = template.Template(figsize = (8.5,11), scriptname = "tests.py")
    blank = testfig.blank()
    
    return testfig.fig

@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_url():
    
    url = "http://matplotlib.org/_images/polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, url, scale = 1, dpi = ax.get_figure().get_dpi())
    return fig

@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_url_shrink_half():
    
    url = "http://matplotlib.org/_images/polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, url, scale = .5, dpi = ax.get_figure().get_dpi())
    return fig

@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_url_zoom_10x():
    
    url = "http://matplotlib.org/_images/polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, url, scale = 10, dpi = ax.get_figure().get_dpi())
    return fig

@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_url_zoom_10x_expand():
    
    url = "http://matplotlib.org/_images/polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, url, scale = 10, dpi = ax.get_figure().get_dpi(), expand = True)
    return fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_file():
    
    file = "template//tests//img//polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, file, scale = 1, dpi = ax.get_figure().get_dpi())
    return fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_file_shrink_half():
    
    file = "template//tests//img//polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, file, scale = .5, dpi = ax.get_figure().get_dpi())
    return fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_file_zoom_10x():
    
    file = "template//tests//img//polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, file, scale = 10, dpi = ax.get_figure().get_dpi())
    return fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_insert_image_from_file_zoom_10x_expand():
    
    file = "template//tests//img//polar_bar_demo.png"
    
    fig, ax = plt.subplots(figsize = (9,9), dpi = 300)
    logo_ax = template.insert_image(ax, file, scale = 10, dpi = ax.get_figure().get_dpi(), expand = True)
    return fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_custom_spans():
    test = [    {"span":[  0,  8,  0, 32]},
                {"span":[ 13, 16, 16, 30]},
                {"span":[ 13, 16,  0, 16]},
                {"span":[  8, 13,  0, 32]},
                {"span":[  0, 13, 32, 40]},
                {"span":[ 13, 16, 30, 40]},
            ]

    testfig = template.Template(figsize = (5,3), scriptname = "tests.py",
                                titleblock_content=test)
    blank = testfig.blank()

    return testfig.fig

@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_titleblock_on_left():

    testfig = template.Template(figsize = (8.5,11), scriptname = "tests.py")
    testfig.gstitleblock = testfig.gsfig[-(testfig.bottom+testfig.t_h) or None:-testfig.bottom or None,
                                         (testfig.left) or None:-(testfig.left+testfig.t_w) or None
                                        ]
    blank = testfig.blank()

    return testfig.fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_zero_margins():

    testfig = template.Template(figsize = (8.5,11), scriptname = "tests.py", 
                                margins = (0,0,0,0))

    blank = testfig.blank()

    return testfig.fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_custom_titleblock():
    custom = [
                {
                 'span':[0,32,0,16],
                 'name':'Title',
                 'text':[{
                            "ha":"center",
                            "s":"Test\nCustom Block",
                            "va":"baseline",
                            "weight":"bold",
                            "x":0.5,
                            "y":0.52,
                            },
                        {
                            "color":(.3,0.3,0.3),
                            "ha":"center",
                            "s":"Blank Example",
                            "va":"top",
                            "weight":"light",
                            "x":0.5,
                            "y":0.48,
                            },
                        ],
                },
                {
                 'name':'logo',
                 'image':{'path':'template//tests//img//polar_bar_demo.png',
                          'scale': 1,
                          },
                 'span':[0,32,16,32],
                },
                {
                 'name':'fignum',
                 'text':{'s':'5',
                         'x':.5,
                         'y':.5,
                         'ha':'center',
                         'va':'center',
                        },
                         
                 'span':[0,32,32,48],
                },
            ]

    testfig = template.Template(figsize = (8.5,11), 
                                scriptname = "tests.py", 
                                titleblock_content = custom)

    fig = testfig.setup_figure()

    return testfig.fig
    
@pytest.mark.mpl_image_compare(baseline_dir = "baseline_images", tolerance = 10)
def test_fancy_titleblock():
    fancy = [{'name':'title', 
             'text':[{
                    "ha":"center",
                    "s":"Fancy Template Example",
                    "va":"baseline",
                    "weight":"bold",
                    "x":0.5,
                    "y":0.52,
                    },
                {
                    "color":(.3,0.3,0.3),
                    "ha":"center",
                    "s":"Feeling Gray",
                    "va":"top",
                    "weight":"light",
                    "x":0.5,
                    "y":0.48,
                    },
                ],
             },
            {'name':'logo',
             'image':{'path':'template//tests//img//polar_bar_demo.png',
                      'scale':0.8,
                      },
             },
            {}, #placeholders for empty default boxes
            {},
            {'name':'fignum',
             'text':{
                    "ha":"center",
                    "s":"Figure\n{:02d}",
                    "va":"center",
                    "weight":"bold",
                    "x":0.5,
                    "y":0.5,
                },
             },
            ]

    testfig = template.Template(figsize = (8.5,11), 
                                scriptname = "tests.py", 
                                titleblock_content = fancy)

    fig = testfig.setup_figure()

    return testfig.fig