# Copyright 2014 Benjamin Schnitzler <benjaminschnitzler@googlemail.com>

# This file is part of 'Symbolic Data After Eval'.
# 
# 'Symbolic Data After Eval' is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# 'Symbolic Data After Eval' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# 'Symbolic Data After Eval'. If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from tools.help_text.help_text import HelpText

class Main:
  def __init__(self, argv):
    self.data_path = os.path.dirname(os.path.abspath(__file__)) + "/data"
    self.init_argument_parser(argv)
    self.execute()

  def init_argument_parser(self, argv):
    """ set handles for the subcommands of sdae
    """
    self.args_parser = HelpText(
        help_file=self.data_path + "/help.json",
        argv=argv,
        convert_from=self.data_path + "/help.yaml"
    )
    self.args_parser.set_handle( self.dummy, "list" )

  def dummy(self, args):
    print("This command is not implemented yet!")

  def execute(self):
    self.args_parser.parse_and_exec()

if __name__ == "__main__":
  Main(sys.argv)
