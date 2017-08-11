"""
Used for creating and writing files
"""

def bold_and_underlined(string):
    return '<strong style="text-decoration: underline">{}</strong>'.format(string)

def print_short_info(club):
    return "- " + club.club_name + " (" + club.club_id + ")"

def print_long_info(club):
    return "- " + club.club_name + " (" + club.club_id + \
        ")\n\s\sAdmin: " + club.admin_name + " (" + club.email + ")"

def loop_list(club_list, print_type, delimiter='\n'):
    return_string = ""
    
    for club in club_list:
        return_string += print_type(club) + delimiter

    return return_string

def generate_summary(pending_list, trial_list, display_type, html):

    if html:
        heading = lambda x: bold_and_underlined(x)
        delimiter = "<br>"
    else:
        heading = lambda x: x
        delimiter = "\n"

    return_string = heading("Pending Account Notices Sent:") + delimiter
    return_string += loop_list(pending_list, display_type, delimiter)
    return_string += delimiter + heading("Trial Account Notices Sent:") + delimiter
    return_string += loop_list(trial_list, display_type, delimiter)

    return return_string

def write_report(file_dest, pending_list, trial_list, verbose=False, html=False):
    """Write all of the pending and trial accounts into a report"""

    if verbose:
        summary = generate_summary(pending_list, trial_list, print_long_info, html)
    else:
        summary = generate_summary(pending_list, trial_list, print_short_info, html)
    
    with open(file_dest, 'a') as file:
        file.write(summary)
