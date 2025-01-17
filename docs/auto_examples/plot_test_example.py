"""
Test Example
===================================

Test the sphinx-gallery build using only matplotlib

.. image:: ../examples/example_plots/test_example.png
    :alt: Pre-generated image for this example

"""

import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.savefig('example_plots/test_example.png')
plt.show()