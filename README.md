### Symbolic Data After Eval (sdae)

#### DESCRIPTION

Symbolic Data After Eval is a python3 package which is supposed to be used to
evaluate and compare the CAS results/output created by SDEval.

#### INSTALLATION

To make this package usable, you have to initialize the necessary tools:

    git submodule init
    git submodule update

After that you may just run it from the root directory of this git repository
(the directory this README is contained in) by issuing the following command:

    python -m sdae

This will emit the help message. It will not know the command right command line
invokation of sdae at this time - don't be irritated by that.

If you want to install sdae systemwide - TODO

#### LICENSE

'Symbolic Data After Eval' (sdae) is licensed under version 3 of the GNU General
Public License.

#### CONTACT

Benjamin Schnitzler <benjaminschnitzler@googlemail.com>

#### FUTURE VISIONS

- the info command should be able to output more infos (machinesettings, name of
  the task, ...)
- the info command should optionally display a tree, itemizing which
  exportfolders contain which results for which cas and probleminstances ...
