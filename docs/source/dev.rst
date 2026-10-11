Develop
=======

If you would like to participate in the development of this project or create your own fork, you can read this page to learn how to use `uv <https://docs.astral.sh/uv>`__ to manage the development environment.

Download the code
-----------------

Clone the code to your local develop environment by the command:

.. code-block:: shell

   git clone https://github.com/Mooling0602/mcdr-devtools.git

Or if SSH configured fine:

.. code-block:: shell

   git clone git@github.com:Mooling0602/mcdr-devtools.git

Sync the uv environment
-----------------------

If you just want to do tests, use:

.. code-block:: shell

   uv sync

Then, activate the virtual environment managed by uv:

.. code-block:: shell

   source .venv/bin/<activate_script>

.. note::

   If you are using `bash <https://www.gnu.org/software/bash>`__ , the script is named ``activate``;

   If you are using `fish <https://fishshell.com>`__ , the script is named ``activate.fish``;

   If you are using `zsh <https://www.zsh.org>`__ , the script is named ``activate.zsh``.

Now you can do any test you like.

If you want to run the tests built-in, execute:

.. code-block:: shell

   python -m unittest discover tests

or:

.. code-block:: shell

   uv run python -m unittest discover tests

if outside the uv environment.

Build the docs
--------------

The docs need the packages from the ``docs`` dependency group:

.. code-block:: shell

   uv sync --group docs

Then build the HTML output into ``docs/build/html``:

.. code-block:: shell

   ./docs/build_docs.sh

To build the Chinese translation instead, pass the language code:

.. code-block:: shell

   ./docs/build_docs.sh zh_CN

For a live preview that rebuilds on every save, use:

.. code-block:: shell

   ./docs/serve_docs.sh

Finally
-------

Thanks for reading this documentation! I'll keep updating it to ensure the correctness.
