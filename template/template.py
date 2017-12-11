# -*- coding: utf-8 -*-

from __future__ import division

__all__ = ["insert_image", "Template"]

import os
import io
import copy

import requests
from PIL import Image
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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

    if ('http' in path):
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
    try:
        exif = {TAGS.get(tag): value for tag, value in im._getexif().items()}

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
    ax : matplotlib.Axes
    image_path : str
        Path to an existing image file.
    scale : float, optional
        The relative scale of the desired output.
        Values should be positive floats.
        E.g. scale = 2 will double the image's size
        relative to the given matplotlib.Axes object.
        scale = 0.5 will scale the image to half of the
        given matplotlib.Axes object.
    dpi : int, optonal (default = 300)
        The Dots (pixel) Per Inch of the image.
    expand : bool, option (default = False)
        If true, the image will expand to fill the axes
        in which it is embedded. Use expand = True if the
        boundary of the enclosing axes is the desired crop boundary.
        Use expand = False if the image should be scaled in-place
        with it's original aspect ratio. This option only affects
        images that have been zoomed (scale>1).
    kwargs : keyword arguments to pass to the figure.add_axes()
        constructor.

    Notes
    -----
    Use scale parameter to zoom image relative to axes boundary.
    """
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


def _get_default_tb_spans(rows, cols):

    spans = [
        {'span': [0, rows[0], 0, sum(cols)]},
        {'span': [rows[0], rows[0] + rows[1], 0, cols[0] + cols[1]]},
        {'span': [rows[0] + rows[1], sum(rows), 0, cols[0]]},
        {'span': [rows[0] + rows[1], sum(rows), cols[0], cols[0] + cols[1]]},
        {'span': [rows[0], sum(rows), cols[0] + cols[1], sum(cols)]},
    ]
    return spans


def _validate_margins(margins):
    if margins is None:
        margins = (4, 4, 4, 4)
    elif (len(margins) != 4 or not all(isinstance(x, int) for x in margins)):
        raise ValueError("`margins` must contain four integers")
    return margins


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

            tbk = [{
                    'name' : 'Title',

                            #`text` must be a dict or a list of dicts
                    'text' : [{
                                's' : 'Figure Title',
                                'weight' : 'bold',
                                },
                              {
                                's' : 'Figure Subtitle',
                                'weight' : 'light',
                                },
                        ],

                            #`image` must refer to dict with `path` key (required),
                            # and optional keys `scale` and `expand` which default
                            # to 1 and False, respectively.
                    'image': {
                        'path':'img//logo.png',
                        'scale': 1,
                        },

                            #`span` must be a list of integers for the
                            # gridspec columns that the titleblock element will
                            # span in tenths of an inch. The following span
                            # will give a titleblock element that is 0.8 inches tall
                            # and 3.2 inches wide. It will be the top left element
                            # of the block because its height and width begin at zero.
                    'span' : [0,8,0,32],
                    },
                   {...#specify keys for next tbk element
                    },

                    ]

    titleblock_cols : tuple of int, optional (default = (16, 16, 8))
        The specification (in tenths of an inch) of the rulers for
        each column in the title block.
    titleblock_rows : tuple of int, optional (default = (8, 5, 3))
        The specification (in tenths of an inch) of the rulers for
        each rows in the title block.
    draft : bool, optional (default = True)
        Toggles the inclusion of a draft watermark.
    dpi : int, optional (default = 300)
        Resolution of the final figure in dots per inch.
    **figkwargs
        Additional keyword arguments passed to ``plt.figure``

    Examples
    --------
    To produce an empty figure containing a border object,
    and 5 title block objects:

    >>> from template import Template
    >>> t = Template(figsize(8.5,11),scriptpath = "path//to//script.py"
    >>> fig = t.setup_figure()
    >>> fig.show()
    <matplotlib figure object>
    """

    def __init__(self,
                 margins=None,
                 titleblock_content=None,
                 titleblock_cols=None,
                 titleblock_rows=None,
                 scriptname=None,
                 draft=True,
                 dpi=300,
                 **figkwargs):

        if scriptname is None:
            raise Exception('Must enter name of calling script for footnote')
        self.script_name = scriptname

        self._margins = _validate_margins(margins)
        self.left, self.right, self.top, self.bottom = self.margins

        if titleblock_cols is None:
            titleblock_cols = (16, 16, 8)

        if titleblock_rows is None:
            titleblock_rows = (8, 5, 3)

        self.default_spans = _get_default_tb_spans(
            titleblock_rows, titleblock_cols)

        self.t_w = sum(titleblock_cols)
        self.t_h = sum(titleblock_rows)
        self.is_draft = draft

        self._fig = None
        self._gsfig = None
        self._watermark = None
        self._path_text = None
        self._gstitleblock = None
        self._gstitleblock_subspec = None
        self._fig_options = figkwargs
        self._fig_options['dpi'] = dpi
        self._titleblock_content = titleblock_content

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
            self.fig = plt.figure(**self._fig_options)
            if self.is_draft:
                self.add_watermark()
        return self._fig

    @fig.setter
    def fig(self, value):
        self._fig = value

    @property
    def gsfig(self):
        if self._gsfig is None:
            row = int(self.fig.get_figheight() * 10)
            col = int(self.fig.get_figwidth() * 10)
            self._gsfig = gridspec.GridSpec(row, col, left=0, right=1, bottom=0,
                                            top=1, wspace=0, hspace=0)
        return self._gsfig

    @gsfig.setter
    def gsfig(self, value):
        self._gsfig = value

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

    @property
    def gstitleblock(self):
        if self._gstitleblock is None:
            self._gstitleblock = self.gsfig[-(self.bottom + self.t_h) or None:-self.bottom or None,
                                            -(self.right + self.t_w) or None:-self.right or None]
        return self._gstitleblock

    @gstitleblock.setter
    def gstitleblock(self, value):
        self._gstitleblock = value
        self._gstitleblock_subspec = None

    @property
    def gstitleblock_subspec(self):
        if self._gstitleblock_subspec is None:
            self._gstitleblock_subspec = gridspec.GridSpecFromSubplotSpec(
                self.t_h, self.t_w, self.gstitleblock, wspace=0.0, hspace=0.0,
            )
        return self._gstitleblock_subspec

    @gstitleblock_subspec.setter
    def gstitleblock_subspec(self, value):
        self._gstitleblock_subspec = value

    def add_frame(self):
        _left = self.left / (10. * self.fig.get_figwidth())
        _right = self.right / (10. * self.fig.get_figwidth())
        _bottom = self.bottom / (10. * self.fig.get_figheight())
        _top = self.top / (10. * self.fig.get_figheight())
        rect = [_left, _bottom, 1 - (_left + _right), 1 - (_bottom + _top)]

        frame = self.fig.add_axes(rect, zorder=100, facecolor='none',
                                  xticks=[], yticks=[], label='frame')
        return frame

    def add_watermark(self, text=None):
        if text is None:
            text = 'DRAFT'
        x = 5 / (10. * self.fig.get_figwidth())
        y = 1 - self.top / (10. * self.fig.get_figheight())
        watermark = self.fig.text(x, y, text, fontsize=24,
                                  color='r', fontname='Arial',
                                  fontweight='bold', zorder=1000,
                                  horizontalalignment='left',
                                  verticalalignment='center')
        self.watermark = watermark
        return self.watermark

    def add_titleblock(self):
        axlist = []
        for i, dct in enumerate(self.titleblock_content):

            if 'span' in list(dct.keys()):
                r0, r, c0, c = dct['span']
            else:
                r0, r, c0, c = self.default_spans[i]['span']

            if 'name' in list(dct.keys()):
                label = dct['name']
            else:
                label = 'b_{}'.format(i)

            ax = self.fig.add_subplot(self.gstitleblock_subspec[r0:r, c0:c],
                                      label=label, zorder=100, facecolor='none',
                                      xticks=[], yticks=[], aspect='equal',
                                      adjustable='datalim')
            axlist.append(ax)

        return axlist

    def add_page(self):
        ax = self.fig.add_axes([0, 0, 1, 1], zorder=1000, facecolor='none',
                               xticks=[], yticks=[], label='page')
        return ax

    def add_path_text(self):
        x = self.left / (10. * self.fig.get_figwidth())
        y = abs((self.bottom - 1.5) / (10 * self.fig.get_figheight()))
        text = 'Source:   ' + self.path_text
        textobj = self.fig.text(x, y, text, fontsize=5,
                                horizontalalignment='left',
                                verticalalignment='center')

        return textobj

    def populate_titleblock(self):
        for ax in self.fig.get_axes():
            label = ax.get_label()
            for i, dct in enumerate(self.titleblock_content):
                name = dct.get('name')
                content = dct.get('text')
                image = dct.get('image')
                if name == label:
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

    def blank(self):

        self.add_frame()
        for ax in self.add_titleblock():
            ax.text(0.5, 0.5, '"{}"'.format(ax.get_label()),
                    va="center", ha="center", size=12)
        self.watermark.remove()
        return self.fig
