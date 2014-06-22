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

import json

class DisplayResults:
  def display_timings(self, results):
    """ display the results obtained from the Results.get_timings() function

    Args:
        a dictionary of the form as it is outputted by Results.get_timings()
    """
    print(json.dumps(results, sort_keys=True, indent=4))

  def display_info(self, info):
    """ display the results obtained from the Results.get_info() function

    Args:
        a dictionary of the form as it is outputted by Results.get_timings()
    """
    print(json.dumps(info, sort_keys=True, indent=4))
