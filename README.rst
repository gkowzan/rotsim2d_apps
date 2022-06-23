.. |LETTER| replace:: G.\ Kowzan, T. K. Allison, Controlling rotationally-resolved two-dimensional infrared spectra with polarization, arXiv:2206.10492 [physics.optics], (2022).

.. |THEORY| replace:: G.\ Kowzan, T. K. Allison, Theory of rotationally-resolved two-dimensional infrared spectroscopy, arXiv:2206.10488 [physics.optics], (2022).

.. |HAPI| replace:: R.V. Kochanov, I.E. Gordon, L.S. Rothman, P. Wcisło, C. Hill, J.S. Wilzewski, HITRAN Application Programming Interface (HAPI): A comprehensive approach to working with spectroscopic data, J. Quant. Spectrosc. Radiat. Transfer 177, 15-30 (2016).

This package contains several GUI applications using features of the `rotsim2d <https://github.com/gkowzan/rotsim2d>`_ library.
These include:

- `rotsim2d_polarizations`, shows values of all 7 R-factors in the high-J limit
  as a function of polarization angles. To reduce dimensionality, the first
  angle is always set to zero and the user can select which of the remaining
  three angles is fixed. The dependence on the last two angles is shown as 2D
  images.
- `rotsim2d_peak_picker`, shows scatter plot of third-order pathway intensities, clicking on a peak will print out information about pathways contributing to the peak.
- `rotsim2d_waiting_time`, investigate waiting time dependence.

Installation
============
Install the package with::

  pip install rotsim2d_apps

Documentation
=============
For documentation see: `rotsim2d_apps documentation <https://rotsim2d.readthedocs.io/en/latest/getting-started/gui-applications.html>`_.

Citations
=========
Please cite the following articles when publishing the results of using this library:

1. |LETTER|
2. |THEORY|
3. |HAPI|

License
=======
rotsim2d is available under the open source `MIT license <https://opensource.org/licenses/MIT>`_.

Funding
=======
.. list-table::
   :widths: auto
   :header-rows: 0

   * - .. image:: docs/images/flag_yellow_low.jpg
          :width: 200px
     - This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No 101028278.
