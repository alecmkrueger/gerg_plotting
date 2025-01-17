"""
Test Example
===================================

Test the sphinx-gallery build using only matplotlib

.. image:: ../../example_plots/plot_test_example.png
    :alt: Pre-generated image for this example

"""

import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
plt.savefig('example_plots/plot_test_example.png')