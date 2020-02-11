=====
Usage
=====

To use Data Extractor Utils in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dataextractor.apps.DataExtractorConfig',
        ...
    )

Add Data Extractor Utils's URL patterns:

.. code-block:: python

    from dataextractor import urls as dataextractor_urls


    urlpatterns = [
        ...
        url(r'^', include(dataextractor_urls)),
        ...
    ]
