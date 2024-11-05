from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest
from PIL import Image
from importlib.resources import files

from mpl_template import template

matplotlib.use("agg")

DEMO_PNG_URL = "https://raw.githubusercontent.com/austinorr/mpl-template/14496e1965e8b360093e0a559ae3f9aba6205a56/template/tests/img/polar_bar_demo.png"
DEMO_PNG_FILE = str(files("mpl_template.tests.img") / "polar_bar_demo.png")
IMG_TOL = 10
BASELINE_DIR = "baseline_images"
SCRIPTNAME = str(Path("mpl_template") / "tests" / "test_template.py")


@pytest.mark.parametrize(
    ("size", "scale", "expected"),
    [(100, 0.5, (-50, 150)), (20, 1.5, (10 / 3.0, 20 - 10 / 3.0))],
)
def test_calc_extents(size, scale, expected):
    lower, upper = template._calc_extents(size, scale)

    assert abs(lower - expected[0]) < 0.0001
    assert abs(upper - expected[1]) < 0.0001


@pytest.mark.parametrize("i", range(4))
@pytest.mark.mpl_image_compare(
    baseline_dir=BASELINE_DIR,
    tolerance=IMG_TOL,
    filename="grace_hopper.png",
    savefig_kwargs={"dpi": 96},
)
def test__apply_exif_rotation(i):
    filepath = str(files("mpl_template.tests.img") / "grace_hopper_{}.jpeg".format(i))
    img = Image.open(filepath)
    im_rot = template._apply_exif_rotation(img)
    dpi = 96
    fig = plt.figure(dpi=dpi, figsize=(im_rot.width / dpi, im_rot.height / dpi))
    ax = fig.add_axes([0, 0, 1, 1])
    _ = ax.imshow(im_rot)
    ax.axis("off")
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_blank():
    testfig = template.Template(figsize=(8.5, 11), scriptname="")
    testfig.path_text = SCRIPTNAME
    _ = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url():
    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, url, scale=1)
    return fig


def test_insert_svg_image_from_url():
    url = "https://matplotlib.org/_static/logo2_compressed.svg"
    fig, ax = plt.subplots(figsize=(9, 9))
    with pytest.raises(ValueError):
        _ = template.insert_image(ax, url, scale=1)


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url_shrink_half():
    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, url, scale=0.5)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url_zoom_10x():
    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, url, scale=10)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_url_zoom_10x_expand():
    url = DEMO_PNG_URL
    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, url, scale=10, expand=True)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file():
    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, file, scale=1)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file_shrink_half():
    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, file, scale=0.5)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file_zoom_10x():
    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, file, scale=10)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_insert_image_from_file_zoom_10x_expand():
    file = DEMO_PNG_FILE

    fig, ax = plt.subplots(figsize=(9, 9))
    _ = template.insert_image(ax, file, scale=10, expand=True)
    return fig


@pytest.mark.mpl_image_compare(
    baseline_dir=BASELINE_DIR, tolerance=IMG_TOL, filename="test_custom_spans.png"
)
@pytest.mark.parametrize("base", [None, 10])
def test_custom_spans(base):
    test = [
        {"span": [0, 8, 0, 32]},
        {"span": [13, 16, 16, 30]},
        {"span": [13, 16, 0, 16]},
        {"span": [8, 13, 0, 32]},
        {"span": [0, 13, 32, 40]},
        {"span": [13, 16, 30, 40]},
    ]

    testfig = template.Template(
        figsize=(5, 3), scriptname="", titleblock_content=test, base=base
    )
    testfig.path_text = SCRIPTNAME
    _ = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(
    baseline_dir=BASELINE_DIR, tolerance=IMG_TOL, filename="test_custom_spans.png"
)
def test_custom_spans_100():
    test = [
        {"span": [0, 80, 0, 320]},
        {"span": [130, 160, 160, 300]},
        {"span": [130, 160, 0, 160]},
        {"span": [80, 130, 0, 320]},
        {"span": [0, 130, 320, 400]},
        {"span": [130, 160, 300, 400]},
    ]

    testfig = template.Template(
        figsize=(5, 3), scriptname="", titleblock_content=test, base=100
    )
    testfig.path_text = SCRIPTNAME
    _ = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(
    baseline_dir=BASELINE_DIR,
    tolerance=IMG_TOL,
    filename="test_titleblock_on_left.png",
)
@pytest.mark.parametrize("base", [None, 10, 100])
def test_titleblock_on_left(base):
    testfig = template.Template(figsize=(8.5, 11), scriptname="", base=base)
    testfig.gstitleblock = testfig.gsfig[
        -(testfig.bottom + testfig.t_h) or None : -testfig.bottom or None,
        (testfig.left) or None : -(testfig.left + testfig.t_w) or None,
    ]

    _ = testfig.blank()

    return testfig.fig


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_zero_margins():
    testfig = template.Template(
        figsize=(8.5, 11), scriptname="tests.py", margins=(0, 0, 0, 0)
    )

    _ = testfig.blank()

    return testfig.fig


@pytest.mark.parametrize(
    "bad_margin",
    [
        (0, 0, 0),
        (0, 0, 0, 0.0),
    ],  # 3 margins  # float margins
)
def test_bad_margins(bad_margin):
    with pytest.raises(ValueError):
        _ = template.Template(
            figsize=(8.5, 11), scriptname="tests.py", margins=bad_margin
        )


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=IMG_TOL)
def test_custom_titleblock():
    custom = [
        {
            "span": [0, 32, 0, 16],
            "name": "Title",
            "text": [
                {
                    "ha": "center",
                    "s": "Test\nCustom Block",
                    "va": "baseline",
                    "weight": "bold",
                    "x": 0.5,
                    "y": 0.52,
                },
                {
                    "color": (0.3, 0.3, 0.3),
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
            "name": "logo",
            "image": {
                "path": DEMO_PNG_FILE,
                "scale": 1,
            },
            "span": [0, 32, 16, 32],
        },
        {
            "name": "fignum",
            "text": {
                "s": "5",
                "x": 0.5,
                "y": 0.5,
                "ha": "center",
                "va": "center",
            },
            "span": [0, 32, 32, 48],
        },
    ]

    testfig = template.Template(
        figsize=(8.5, 11), scriptname="", titleblock_content=custom
    )

    testfig.path_text = SCRIPTNAME
    _ = testfig.setup_figure()

    return testfig.fig


@pytest.mark.parametrize("base", [None, 10, 100])
@pytest.mark.mpl_image_compare(
    baseline_dir=BASELINE_DIR,
    tolerance=IMG_TOL,
    filename="test_fancy_titleblock.png",
)
def test_fancy_titleblock(base):
    fancy = [
        {
            "name": "title",
            "text": [
                {
                    "ha": "center",
                    "s": "Fancy Template Example",
                    "va": "baseline",
                    "weight": "bold",
                    "x": 0.5,
                    "y": 0.6,
                },
                {
                    "color": (0.3, 0.3, 0.3),
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
            "name": "logo",
            "image": {
                "path": DEMO_PNG_FILE,
                "scale": 0.8,
            },
        },
        {},  # placeholders for empty default boxes
        {},
        {
            "name": "fignum",
            "text": {
                "ha": "center",
                "s": "Figure\n{:02d}",
                "va": "center",
                "weight": "bold",
                "x": 0.5,
                "y": 0.5,
            },
        },
    ]

    testfig = template.Template(
        figsize=(8.5, 11), scriptname="", titleblock_content=fancy, base=base
    )
    testfig.path_text = SCRIPTNAME
    _ = testfig.setup_figure()

    return testfig.fig


def test_template_attrs():
    obj = template.Template(figsize=(8.5, 11), scriptname="")
    attrs = [i for i in dir(obj) if not callable(i) and not "_" == i[0]]
    for attr in attrs:
        t = template.Template(figsize=(8.5, 11), scriptname="")
        assert getattr(t, attr, None) is not None
