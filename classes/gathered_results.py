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
import xml.etree.ElementTree as ET

class GatheredResults:
  """ this class is used for collecting all data from every exportfolder
      specified at the command line.
  """
  def __init__(self, exportdirs):
    """ initialization

        Args:
            exportdirs:
                a list of the exportfolders to consider, when collecting results
                or information
    """
    self.exportdirs = exportdirs

  def info(self, about=None):
    """ display info about the used cas/timestamps/probleminstances and provide
        shortcuts for them.

        Args:
            about:
                None or list of restrictions for what info shall be given. list
                may contain 'cas', 'probleminstances' or 'timestamps'
    """
    if about == None: about = ['cas', 'probleminstances', 'timestamps']

    info = {
        'cas' : {'display':'Computeralgebrasystems:', 'list':set()},
        'probleminstances' : {'display':'Probleminstances:', 'list':set()},
        'timestamps' : {'display':'Timestamps:', 'list':set()}
    }

    for edir in self.exportdirs:
      edir = edir.rstrip('/') + '/'
      resdir = edir + "results/"
      have_results = True
      if os.path.isdir(resdir):
        for result in os.walk(resdir).__next__()[1]:
          try:
            xmltree = ET.parse(resdir + result + '/proceedings.xml')

            timestamp = xmltree.find(".//timestamp").text
            info['timestamps']['list'].add(timestamp)

            entries = xmltree.findall(".//entry")
            for entry in entries:
              probleminstance = entry.find("./probleminstance").text
              info['probleminstances']['list'].add( probleminstance )

              cas = entry.find("./computeralgebrasystem").text
              info['cas']['list'].add(cas)
          except Exception as e:
            error = "Error: Could not parse information from:\n{}";
            print( error.format(resdir) )
            print( str(e) + '\n' )
      else:
        print("No results found in: \n" + edir + "\n")
        try:
          xmltree = ET.parse(edir + "taskInfo.xml")

          findcas = ".//computeralgebrasystems/computeralgebrasystem"
          for cas in xmltree.findall(findcas):
            info['cas']['list'].add(cas.text)

          findprobleminstances = ".//probleminstance/probleminstances"
          for probleminstance in xmltree.findall(findprobleminstances):
            info['probleminstances']['list'].add(probleminstance.text)
        except Exception as e:
          error = "Error: Could not parse information from:\n{}\n";
          print( error.format(edir) )
          print( str(e) + '\n' )

    output=""
    for category in about:
      num_entries = len(info[category]['list'])
      if num_entries > 0:
        padding = str(len(str(num_entries-1)))
        output += info[category]['display'] + "\n"
        i = 0
        for entry in sorted(info[category]['list']):
          output += ("  " + "{:>"+padding+"} " + entry.strip() + "\n").format(i)
          i += 1
        output += "\n"
    print(output.rstrip())
