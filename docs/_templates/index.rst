API Reference
=============

.. toctree::
   :titlesonly:

   {% for page in pages|selectattr("is_top_level_object") %}
   {{ page.include_path }}
   {% endfor %}


Examples
=============

.. toctree::
   :titlesonly:
   {% for page in pages|selectattr("is_example") %}
   {{ page.include_path }}
   {% endfor %}