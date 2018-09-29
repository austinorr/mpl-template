# -*- coding: utf-8 -*-
from __future__ import division
import os
from pkg_resources import resource_filename

import pytest

from PIL import Image
from mpl_template import template
import matplotlib.pyplot as plt

DEMO_PNG_URL = "https://raw.githubusercontent.com/austinorr/mpl-template/14496e1965e8b360093e0a559ae3f9aba6205a56/template/tests/img/polar_bar_demo.png"
DEMO_PNG_FILE = resource_filename(
    "mpl_template.tests.img", "polar_bar_demo.png")
IMG_TOL = 12
BASELINE_DIR = "baseline_images"
SCRIPTNAME = os.path.join("mpl_template", "tests", "test_template.py")


@pytest.mark.parametrize(('size', 'scale', 'expected'), [
    (100, .5, (-50, 150)),
    (20, 1.5, (10 / 3., 20 - 10 / 3.))
])
def test_calc_extents(size, scale, expected):

    lower, upper = template._calc_extents(size, scale)

    assert abs(lower - expected[0]) < 0.0001
    assert abs(upper - expected[1]) < 0.0001


@pytest.mark.parametrize('filepath', [
    (resource_filename("mpl_template.tests.img", "grace_hopper_{}.jpeg".format(i))) for i in range(4)
])
@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL, filename='grace_hopper.png', savefig_kwargs={'dpi': 96})
def test__apply_exif_rotation(filepath):
    img = Image.open(filepath)
    im_rot = template._apply_exif_rotation(img)
    dpi = 96
    fig = plt.figure(dpi=dpi, figsize=(
        im_rot.width / dpi, im_rot.height / dpi))
    ax = fig.add_axes([0, 0, 1, 1])
    _ = plt.imshow(im_rot)
    plt.axis('off')
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_blank():

    testfig = template.Template(figsize=(8.5, 11), scriptname="")
    testfig.path_text = SCRIPTNAME
    blank = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url():

    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, url, scale=1)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url_shrink_half():

    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, url, scale=.5)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url_zoom_10x():

    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, url, scale=10)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url_zoom_10x_expand():

    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, url, scale=10, expand=True)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file():

    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, file, scale=1)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file_shrink_half():

    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, file, scale=.5)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file_zoom_10x():

    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, file, scale=10)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file_zoom_10x_expand():

    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    logo_ax = template.insert_image(
        ax, file, scale=10, expand=True)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_custom_spans():
    test = [
        {"span": [0,  .8,  3.2, .8]},
        {"span": [1.6, 0, 1.4, .3]},
        {"span": [0, 0,  1.6, .3]},
        {"span": [0, .3,  3.2, .5]},
        {"span": [3.2, .3, .8, 1.3]},
        {"span": [3, 0, 1, .3]},
    ]

    testfig = template.Template(figsize=(5, 3), scriptname="",
                                titleblock_content=test)
    testfig.path_text = SCRIPTNAME
    blank = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_titleblock_on_left():

    testfig = template.Template(figsize=(8.5, 11), scriptname="",
                                titleblock_loc=(.4, .4))
    # testfig.gstitleblock = testfig.gsfig[
    #     -(testfig.bottom + testfig.t_h) or None:-testfig.bottom or None,
    #     (testfig.left) or None:-(testfig.left + testfig.t_w) or None
    # ]

    blank = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_zero_margins():

    testfig = template.Template(figsize=(8.5, 11), scriptname="tests.py",
                                margins=(0, 0, 0, 0))

    blank = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_custom_titleblock():
    custom = [
        {
            'span': [0, 0, 1.6, 1.6],
            'name':'Title',
            'text':[
                {
                    "ha": "center",
                    "s": "Test\nCustom Block",
                    "va": "baseline",
                    "weight": "bold",
                    "x": 0.5,
                    "y": 0.52,
                },
                {
                    "color": (.3, 0.3, 0.3),
                    "ha": "center",
                    "s": "Blank Example",
                    "va": "top",
                    "weight": "light",
                    "x": 0.5,
                    "y": 0.48,
                },
            ],
        },
        {
            'name': 'logo',
            'image': {
                'path': DEMO_PNG_FILE,
                'scale': 1,
            },
            'span': [1.6, 0, 1.6, 1.6],
        },
        {
            'name': 'fignum',
            'text': {
                's': '5',
                'x': .5,
                'y': .5,
                'ha': 'center',
                'va': 'center',
            },
            'span': [3.2, 0, .8, 1.6],
        },
    ]

    testfig = template.Template(figsize=(8.5, 11),
                                scriptname="",
                                titleblock_content=custom)

    testfig.path_text = SCRIPTNAME
    fig = testfig.setup_figure()

    return testfig.fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_fancy_titleblock():
    fancy = [
        {
            'name': 'title',
            'text': [
                {
                    "ha": "center",
                    "s": "Fancy Template Example",
                    "va": "baseline",
                    "weight": "bold",
                    "x": 0.5,
                    "y": 0.6,
                },
                {
                    "color": (.3, 0.3, 0.3),
                    "ha": "center",
                    "s": "Feeling Gray",
                    "va": "top",
                    "weight": "light",
                    "x": 0.5,
                    "y": 0.4,
                },
            ],
        },
        {
            'name': 'logo',
            'image': {
                'path': DEMO_PNG_FILE,
                'scale': 0.8,
            },
        },
        {},  # placeholders for empty default boxes
        {},
        {
            'name': 'fignum',
            'text': {
                "ha": "center",
                "s": "Figure\n{:02d}",
                "va": "center",
                "weight": "bold",
                "x": 0.5,
                "y": 0.5,
            },
        },
    ]

    testfig = template.Template(figsize=(8.5, 11),
                                scriptname="",
                                titleblock_content=fancy)
    testfig.path_text = SCRIPTNAME
    fig = testfig.setup_figure()

    return testfig.fig
