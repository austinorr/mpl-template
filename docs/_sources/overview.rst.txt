
Purpose of ``mpl-template``
===========================

``matplotlib`` is ubiquitous in the industries of science and engineering as the open source goto package for making publication quality figures.

At my company in the consulting engineering industry, we'd commonly produce nice plots in our analysis scripts and insert those plots into a word document or appendix figure template.

However, this rapidly becomes tedious if there are many figures to insert into the company's template.

This module builds on the ``figure``, ``axes``, and ``gridspec`` paradigms built by ``matplotlib`` to create a very capable and flexible API for using matplotlib to include a figure's titleblock, metadata such as the filepath, neatline, inset images/figures, logo, figure numbering, etc., all entirely with matplotlib.

Users of the ``Template`` class can specify the paper size (inches), margins (tenths), and titleblock specifications (list of dictionaries) of the final figure.

The module also includes ``insert_image``, a helper function to aid in embedding inset images, logos, or any other raster data easily and efficiently.
