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

class Results:
  """ this class can be used for collecting data of
  
      a) the existing timestamp/probleminstance/cas tuples for the constraints
         specified at initialization ( see get_info() )

      b) the timings obtained by SD Eval ( see get_timings() )

      c) the results obtained by the compare subcommand of SD After Eval
         (not implemented yet)

      these results will be collected from the xml files created by SD Eval or
      the compare subcommand.

      the constraints that were mentioned above are constraints to the
      timestamps/probleminstances/cas provided for the __init__() function.
  """
  def __init__(self, exportdirs, timestamps, probleminstances, cas):
    """ initialization

        Args:
            exportdirs (set):
                set of pathes to the SD Eval EXPORTFOLDER directories

            timestamps (set or None):
                set of the timestamps for which data shall be collected or
                None, if data shall be collected for all timestamps. the
                timestamps will be compared to the timestamps from the
                proceedings.xml files created by SD Eval. timestamps are strings
                of the form 'YYYY_MM_DD_hh_mm_ss'.

            probleminstances (set or None):
                set of the probleminstances for which data shall be collected
                or None, if data shall be collected for all probleminstances

            cas (set or None):
                set of the cas for which data shall be collected, or
                None, if data shall be collected for all cas
    """
    self.exportdirs = set(exportdirs)
    self.timestamps = set(timestamps)
    self.probleminstances = set(probleminstances)
    self.cas = set(cas)

  def get_timestamp(self, results_subdir):
    """ for the given subdirectory of results_dir, obtain the timestamp
    
    Args:
        results_subdir:
            the directory where proceedings.xml is located

    Returns:
        the timestamp as 'YYYY_MM_DD_hh_mm_ss' on success,
        None, on error

    Remark:
        sets self.xml_proceedings to the xml-ElementTree of proceedings.xml
    """
    try:
      self.xml_proceedings = ET.parse(results_subdir + '/proceedings.xml')
      return xmltree.find(".//timestamp").text.strip()
    except Exception as e:
      error = "Error: Could not parse information from:\n{}"
      print( error.format(resdir) )
      print( str(e) + '\n' )
      return None

  def parse_timestamp(self, timestamp):
    """ convert timestamp from string to list
    
    Args:
        timestamp:
            the timestamp as 'YYYY_MM_DD_hh_mm_ss' string

    Returns:
        the timestamp as [ YYYY, MM, DD, hh, mm, ss ]'
    """
    return timestamp.strip().split('_')

  def get_probleminstances(self, xml_proceedings, xml_timings):
    """ get some info about timings/proceedings

        Args:
            xml_proceedings:
                an xml element tree for the proceedings.xml file

            xml_timings:
                an xml element tree for the resultedTimings.xml file of None, if
                no timings shall be retrieved

        Returns:
            a dictionary of the form depicted below
                {
                    name_of_the_probleminstance:{
                        name_of_the_cas:{
                            status: waiting/running/completed
                            timings: [ real, sys, user ]
                        }
                    }
                }
            if no timings exists for a given probleminstance/cas pair (or if
            None was passed for xml_timings), then the timings key will not
            exist for that pair.

        Notice:
            filters the timings/proceedings to retrieve in the manner described
            in the description of __init__() (d.i. only timings/proceedings for
            the specified cas/probleminstances will be retrieved), except for,
            that the timestamp and the exportdir will not be checked.
    """
    probleminstances = {}

    # not yet completed calculations (dont have timings)
    for status in ['waiting', 'running']:
      for entry in xml_proceedings.findall(".//entry/" + status):
        probleminstance = entry.find("./probleminstance").text.strip()
        if probleminstance in self.probleminstances:
          probleminstance = probleminstances.setdefault(probleminstance, {})
          cas = entry.find("./computeralgebrasystem").text.strip()
          if cas in self.cas: probleminstance[cas] = { 'status':status }

    # completed calculations (should have timings)
    for entry in xml_timings.findall(".//entry/completed"):
      probleminstance = entry.find("./probleminstance").text.strip()
      if probleminstance in self.probleminstances:
        probleminstance = probleminstances.setdefault(probleminstance, {})

        cas = entry.find("./computeralgebrasystem").text.strip()
        if cas in self.cas:
          probleminstance[cas] = { 'status':'completed' }

          timings = entry.find("./timings")
          real = timings.find("./real").text.strip()
          sys  = timings.find("./sys").text.strip()
          user = timings.find("./user").text.strip()
          probleminstance[cas]['timings'] = [ real, sys, user ]

  def get_timings_xml(self, results_subdir):
    try:
      return ET.parse(results_subdir + '/resultedTimings.xml')
    except:
      return None

  def get_timings(self):
    """ get the info about the timings/proceedings

        Returns:
            a dictionary of the form depicted below
                {
                    name_of_exportfolder: [
                        timestamp: [YYYY, MM, DD, hh, mm, ss]
                        probleminstances: {
                            name_of_the_probleminstance:{
                                name_of_the_cas:{
                                    status: waiting/running/completed
                                    timings: [ real, sys, user ]
                                }
                            }
                        }
                    ]
                }
            if no timings exists for a given probleminstance/cas pair, then the
            timings key will not exist for that pair.

        Notice:
            returned results underly the constraints described at the __init__()
            function.
    """
    timings = {}
    for timestamp, xml_proceedings, xml_timings in self.get_result_iterator():
      entry = []
      entry['timestamp'] = self.parse_timestamp(timestamp)
      entry['probleminstances'] = self.get_probleminstances(
          self.xml_proceedings, self.get_timings_xml()
      )
      timings.append(entry)
    return timings

  def get_info(self):
    pass # TODO: missing implementation

  def get_result_iterator(self):
    """ generates an iterator, for iterating over the associated results
    
        the iterator iterates over all [timestamp, xml_proceedings, xml_timings]
        tuples for the exportdirs and constraints specified at initialization.
        (see description of this class for the description of these constraints)
        xml_proceedings is an xml-ElementTree of proceedings.xml and xml_timings
        is an xml-ElementTree of resultedTimings.xml, if that file exists, or
        None otherwise. the timestamp is a string in form 'YYYY_MM_DD_hh_mm_ss'.

        Returns:
            the iterator
    """
    for edir in self.exportdirs:
      edir = edir.rstrip('/') + '/'
      resdir = edir + "results/"
      if os.path.isdir(resdir):
        for subdir in os.walk(resdir).__next__()[1]:
          if os.isdir(subdir):
            timestamp = self.get_timestamp(subdir)
            if timestamp in self.timestamps:
              yield [ timestamp, self.xml_proceedings, self.get_timings_xml() ]



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
            error = "Error: Could not parse information from:\n{}"
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
          error = "Error: Could not parse information from:\n{}\n"
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

  #def list()
