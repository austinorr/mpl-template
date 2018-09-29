# -*- coding: utf-8 -*-

from __future__ import division

__all__ = ["insert_image", "Template"]

import os
import io
import copy

import matplotlib.pyplot as plt


def _import_requests():
    import requests
    return requests


def _import_PIL_TAGS():
    from PIL.ExifTags import TAGS
    return TAGS


def _import_PIL_Image():
    from PIL import Image
    return Image


def _calc_extents(size, scale):
    """
    Calculates the view limits needed to see a
    centered image at the desired scale.
    E.g.
    Before: image spans whole width
    scale = 0.5
    |________________________|
    0                        size

    After: upper and lower boundaries are
    identified to make the original size
    appear scaled and centered.

    |......____________......|
    lower  0           size  upper

    Parameters
    ----------
    size : int
        Number of pixels in x or y dimension
    scale : float
        The relative scale of the desired output.
    """
    lower = (1 - scale) * size * (1 / scale) / 2.
    upper = size + lower
    return -lower, upper


def _image_path_or_url(path):
    """
    Prepares image path or url for loading into format ready for
    loading by PIL.Image.open()

    Parameters
    ----------
    path : string
        filepath or url to an image file. For images from the web, only
        the file extensions '.png', '.jpg', and '.jpeg' are supported.

    Returnns
    --------
    filepath for images from a file or
    io.BytesIO object for web images
    """

    if ('http' in path):
        requests = _import_requests()

        valid_types = ['.png', '.jpg', '.jpeg']
        if any(ftype in path for ftype in valid_types):
            r = requests.get(path)
            img_file_obj = io.BytesIO(r.content)
        else:
            raise ValueError(
                "Supported web image types include: {}".format(valid_types))
        return img_file_obj

    else:
        return os.path.realpath(path)


def _apply_exif_rotation(im):
    """Apply exif rotation tag to a PIL image object

    Parameters
    ----------
    im : PIL.Image
        image object that may contain rotation data

    Returns
    -------
    PIL.Image
    """
    TAGS = _import_PIL_TAGS()
    Image = _import_PIL_Image()

    try:
        exif = {TAGS.get(tag): value for tag, value in im._getexif().items()}

        # this section adapted from the following SO post:
        # https://stackoverflow.com/a/1608846/7486933
        if 'Orientation' in exif.keys():
            orientation = exif['Orientation']
            if orientation == 1:
                # Nothing
                i = im.copy()
            elif orientation == 2:
                # Vertical Mirror
                i = im.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # Rotation 180°
                i = im.transpose(Image.ROTATE_180)
            elif orientation == 4:
                # Horizontal Mirror
                i = im.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                # Horizontal Mirror + Rotation 90° CCW
                i = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(
                    Image.ROTATE_90)
            elif orientation == 6:
                # Rotation 270°
                i = im.transpose(Image.ROTATE_270)
            elif orientation == 7:
                # Horizontal Mirror + Rotation 270°
                i = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(
                    Image.ROTATE_270)
            elif orientation == 8:
                # Rotation 90°
                i = im.transpose(Image.ROTATE_90)
            else:
                raise Exception('Invalid EXIF Orientation Value')
        else:
            i = im.copy()
        return i

    except (AttributeError, KeyError, IndexError):
        return im


def insert_image(ax, image_path, scale=1, dpi=300, expand=False, **kwargs):
    """
    Centers an image within an axes object

    Parameters
    ----------
    ax : ``matplotlib.Axes``
        the axes into which the image should be inserted.
    image_path : str
        Path to an existing image file.
    scale : float, optional
        The relative scale of the desired output.
        Values should be positive floats.
        E.g. scale = 2 will double the image's size
        relative to the given matplotlib.Axes object.
        scale = 0.5 will scale the image to half of the
        given matplotlib.Axes object.
    dpi : int, optonal (default=300)
        The Dots (pixel) Per Inch of the image.
    expand : bool, optional (default=False)
        If true, the image will expand to fill the axes
        in which it is embedded. Use expand = True if the
        boundary of the enclosing axes is the desired crop boundary.
        Use expand = False if the image should be scaled in-place
        with it's original aspect ratio. This option only affects
        images that have been zoomed (scale > 1).
    kwargs : keyword arguments to pass to the figure.add_axes()
        constructor.

    Returns
    -------
    ax : matplotlib.Axes

    Notes
    -----
    Use scale parameter to zoom image relative to axes boundary.

    Examples
    --------

    Images are inserted centered, scaled, and filling the parent
    axes object.

    Zoomed out 2x with ``scale=0.5``. Note that the enclosing axes is
    square, and that the inserted axes is a landscape rectangle that
    matches the shape of the source file.

    .. plot::
        :context: reset
        :include-source: True

        >>> import matplotlib.pyplot as plt
        >>> from mpl_template import insert_image
        >>> file = "img/polar_bar_demo.png"
        >>> fig, ax = plt.subplots(figsize=(3, 3))
        >>> img_ax = insert_image(ax, file, scale=0.5)

    Zoomed in 2x with ``scale=2``. Note that the use of the ``expand``
    kwarg causes the zoomed image to fill the enclosing square axes object.

    .. plot::
        :context: reset
        :include-source: True

        >>> import matplotlib.pyplot as plt
        >>> from mpl_template import insert_image
        >>> file = "img/polar_bar_demo.png"
        >>> fig, ax = plt.subplots(figsize=(3, 3))
        >>> img_ax = insert_image(ax, file, scale=2, expand=True)
    """
    Image = _import_PIL_Image()

    if 'xticks' not in kwargs:
        kwargs['xticks'] = []
    if 'yticks' not in kwargs:
        kwargs['yticks'] = []
    if 'zorder' not in kwargs:
        kwargs['zorder'] = 1

    imgaxes = ax.figure.add_axes(ax.get_position(), **kwargs)
    bbox = ax.get_window_extent().transformed(
        ax.get_figure().dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= dpi
    height *= dpi
    img_fp_or_obj = _image_path_or_url(image_path)

    with Image.open(img_fp_or_obj) as image:

        image = _apply_exif_rotation(image)
        image = image.convert('RGBA')
        wpx, hpx = image.size
        aspect_im = wpx / hpx
        aspect_ax = width / height
        adjy = (hpx / scale) / 2
        adjx = (wpx / scale) / 2

        if scale > 1:
            if expand and (aspect_im < aspect_ax):
                adjx = (width / height) * adjy
            if expand and (aspect_im > aspect_ax):
                adjy = (height / width) * adjx

            image = image.crop(
                (int(wpx / 2 - adjx),
                 int(hpx / 2 - adjy),
                 int(wpx / 2 + adjx),
                 int(hpx / 2 + adjy)
                 )
            )

            if expand:
                image = image.resize((int(width), int(height)), Image.BICUBIC)

            else:
                if width >= height:
                    width = int(wpx * (height / hpx))
                else:
                    height = int(hpx * (width / wpx))
                image = image.resize((int(width), int(height)), Image.BICUBIC)

        else:
            if width >= height:
                width = int(wpx * (height / hpx))
            else:
                height = int(hpx * (width / wpx))
            image = image.resize(
                (int(width * scale), int(height * scale)), Image.LANCZOS)

            imgaxes.set_xlim(_calc_extents(image.size[0], scale))
            imgaxes.set_ylim(reversed(_calc_extents(image.size[1], scale)))

    imgaxes.imshow(image, aspect='equal')

    return imgaxes


def _get_default_tb_spans():

    spans = [
        # define spans by rectangle [left, bottom, width, height], numbers
        # in inches
        {'span': [0, 0.8, 4.0, 0.8]},
        {'span': [0, 0.3, 3.2, 0.5]},
        {'span': [0,   0, 1.6, 0.3]},
        {'span': [1.6, 0, 1.6, 0.3]},
        {'span': [3.2, 0, 0.8, 0.8]},
    ]

    return spans


def _validate_margins(margins):
    if margins is None:
        margins = (.4, .4, .4, .4)
    elif len(margins) != 4:
        raise ValueError("`margins` must contain four values")
    return margins


def _list_divide(listlike1, listlike2):
    return [a / b for a, b in zip(listlike1, listlike2)]


class Template(object):
    """
    Class to construct a report figure template using matplotlib
    which includes a figure border, script path, and title block.

    Parameters
    ----------
    scriptname : str
        Path to the script or notebook that is creating the figure.
    margins : tuple of int, optional (default = (4, 4, 4, 4)
        A length-4 tuple specifying the left, right, top, and bottom
        margins of on the page, respectively
    titleblock_content : list of dicts, optional
        Title block elements where each element is itself a
        dictionary with a `span` keys that determines which rows and
        columns the each element will occupy in the titleblock.
        E.g. ::

            tbk = [
                {
                    'name': 'Title',

                    #`text` must be a dict or a list of dicts
                    'text': [
                        {
                            's': 'Figure Title',
                            'weight': 'bold',
                        },
                        {
                            's': 'Figure Subtitle',
                            'weight': 'light',
                        },
                    ],

                    #`image` must refer to dict with `path` key (required),
                    # and optional keys `scale` and `expand` which default
                    # to 1 and False, respectively.
                    'image': {
                        'path': 'img//logo.png',
                        'scale': 1,
                    },

                    #`span` is a list indicating a rectangle
                    # with [left, bottom, width, height], numbers
                    # in inches
                    'span': [0, 8, 0, 32],
                },
                {   # specify keys for next tbk element
                },
            ]
    titleblock_cols : tuple of int, optional (default=(16, 16, 8))
        The specification (in tenths of an inch) of the rulers for
        each column in the title block.
    titleblock_rows : tuple of int, optional (default=(8, 5, 3))
        The specification (in tenths of an inch) of the rulers for
        each rows in the title block.
    draft : bool, optional (default=True)
        Toggles the inclusion of a draft watermark.
    dpi : int, optional (default=300)
        Resolution of the final figure in dots per inch.
    **figkwargs
        Additional keyword arguments passed to ``plt.figure``

    Examples
    --------
    To produce an empty figure containing a border object,
    and 5 title block objects:

    .. plot::
        :context: reset
        :include-source: True

        >>> from mpl_template import Template
        >>> report_fig = Template(figsize=(8.5, 11), scriptname="path/to/script.py")
        >>> fig = report_fig.blank()


    """

    def __init__(self,
                 margins=None,
                 titleblock_content=None,
                 titleblock_loc=None,
                 scriptname=None,
                 draft=True,
                 dpi=300,
                 **figkwargs):

        if scriptname is None:
            raise Exception('Must enter name of calling script for footnote')
        self.script_name = scriptname

        self._margins = _validate_margins(margins)
        self.left, self.right, self.top, self.bottom = self.margins

        self._default_spans = None
        self.is_draft = draft

        self._fig = None
        self._gsfig = None
        self._watermark = None
        self._path_text = None
        self._fig_options = figkwargs
        self._fig_options['dpi'] = dpi
        self._titleblock_content = titleblock_content
        self._titleblock_loc = titleblock_loc
        self._titleblock_axes = None
        self._div = None

    @property
    def margins(self):
        return self._margins

    @margins.setter
    def margins(self, value):
        self._margins = _validate_margins(value)
        self.left, self.right, self.top, self.bottom = self._margins

    @property
    def titleblock_content(self):
        if self._titleblock_content is None:
            self._titleblock_content = self.default_spans
        return self._titleblock_content

    @titleblock_content.setter
    def titleblock_content(self, value):
        self._titleblock_content = value

    @property
    def fig(self):
        if self._fig is None:
            self._fig = plt.figure(**self._fig_options)
            if self.is_draft:
                self.add_watermark()
        return self._fig

    @property
    def default_spans(self):
        if self._default_spans is None:
            self._default_spans = _get_default_tb_spans()
        return self._default_spans

    @property
    def titleblock_loc(self):
        if self._titleblock_loc is None:
            w = self.fig.get_figwidth()
            self._titleblock_loc = (w - 4 - self.right, self.bottom)
        return self._titleblock_loc

    @titleblock_loc.setter
    def titleblock(self, value):
        self._titleblock_loc = value

    @property
    def div(self):
        if self._div is None:
            w, h = self.fig.get_size_inches()
            self._div = [w, h, w, h]
        return self._div

    @property
    def watermark(self):
        if self._watermark is None:
            self._watermark = self.add_watermark()
        return self._watermark

    @watermark.setter
    def watermark(self, value):
        self._watermark = value

    @property
    def path_text(self):
        if self._path_text is None:
            self._path_text = os.path.join(os.getcwd(), self.script_name)
        return self._path_text

    @path_text.setter
    def path_text(self, value):
        self._path_text = value

    def add_frame(self):
        _left = self.left / self.fig.get_figwidth()
        _right = self.right / self.fig.get_figwidth()
        _bottom = self.bottom / self.fig.get_figheight()
        _top = self.top / self.fig.get_figheight()
        rect = [_left, _bottom, 1 - (_left + _right), 1 - (_bottom + _top)]

        frame = self.fig.add_axes(rect, zorder=100, facecolor='none',
                                  xticks=[], yticks=[], label='frame')
        return frame

    def add_watermark(self, text=None):
        if text is None:
            text = 'DRAFT'
        x = .5 / self.fig.get_figwidth()
        y = .4 / self.fig.get_figheight()
        watermark = self.fig.text(x, 1 - y, text, fontsize=24,
                                  color='r', fontname='Arial',
                                  fontweight='bold', zorder=1000,
                                  horizontalalignment='left',
                                  verticalalignment='center')
        self.watermark = watermark
        return self.watermark

    @property
    def titleblock_axes(self):
        return self._titleblock_axes

    def add_titleblock(self):
        self._titleblock_axes = []
        l_off, b_off = self.titleblock_loc

        for i, dct in enumerate(self.titleblock_content):

            if 'span' in list(dct.keys()):
                l, b, w, h = dct['span']
            else:
                l, b, w, h = self.default_spans[i]['span']

            if 'name' in list(dct.keys()):
                label = dct['name']
            else:
                label = 'b_{}'.format(i)

            rect = _list_divide([l + l_off, b + b_off, w, h], self.div)

            ax = self.fig.add_axes(rect, label=label,
                                   zorder=100, facecolor='none',
                                   xticks=[], yticks=[], aspect='equal',
                                   adjustable='datalim')
            self._titleblock_axes.append(ax)

        return self.titleblock_axes

    def add_page(self):
        ax = self.fig.add_axes([0, 0, 1, 1], zorder=1000, facecolor='none',
                               xticks=[], yticks=[], label='page')
        return ax

    def add_path_text(self):
        x = self.left / self.fig.get_figwidth()
        y = .15 / self.fig.get_figheight()
        text = 'Source:   ' + self.path_text
        textobj = self.fig.text(x, y, text, fontsize=5,
                                horizontalalignment='left',
                                verticalalignment='center')

        return textobj

    def populate_titleblock(self):
        for i, (ax, dct) in enumerate(zip(self.titleblock_axes, self.titleblock_content)):
            content = dct.get('text')
            image = dct.get('image')
            if content is not None:
                if isinstance(content, dict):
                    content = [content]
                if isinstance(content, list):
                    for elem in content:
                        kwargs = copy.deepcopy(elem)
                        if 'transform' not in kwargs:
                            kwargs['transform'] = ax.transAxes
                        ax.text(**kwargs)
                else:
                    raise ValueError(
                        '`text` key must map to dict or list of dicts')
            if image is not None:

                scale = image.get('scale', 1)
                expand = image.get('expand', False)
                img_ax = insert_image(ax, image['path'],
                                      scale=scale,
                                      dpi=ax.get_figure().get_dpi(),
                                      expand=expand)
                img_ax.set_label('img_b_{}'.format(i))
                img_ax.axis('off')

    def setup_figure(self):

        frame = self.add_frame()
        block = self.add_titleblock()
        path = self.add_path_text()
        self.populate_titleblock()

        return self.fig

    def add_axes(self, *args, **kwargs):
        rect = _list_divide(args[0], self.div)

        return self.fig.add_axes(rect, *args[1:], **kwargs)

    def blank(self):

        self.add_frame()
        for ax in self.add_titleblock():
            ax.text(0.5, 0.5, '"{}"'.format(ax.get_label()),
                    va="center", ha="center", size=12)
        self.watermark.remove()
        return self.fig
