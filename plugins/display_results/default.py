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
