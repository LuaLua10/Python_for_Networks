# Nornir

* Nornir is a pure Python automation framework intented to be used directly from Python. While most automation frameworks use their own Domain Specific Language (DSL) which you use to describe what you want to have done, Nornir lets you control everything from Python.

* One of the benefits we want to highlight with this approach is the ease of troubleshooting, if something goes wrong you can just use your existing debug tools directly from Python (just add a line of import pdb & pdb.set_trace() and you're good to go). Doing the same using a DSL can be quite time consuming.

* What Nornir brings to the table is that it takes care of dealing with your inventory and manages the job of dispatching the tasks you want to run against your nodes and devices. The framework provides a very simple way to write plugins if you aren't happy with the ones we ship. Of course if you have written a plugin you think can be useful to others, please send us your code and test cases as a pull request.
