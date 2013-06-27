
from hosted_legistar_scraper import HostedLegistarSiteWrapper

class ChicagoHostedLegistarSiteWrapper (HostedLegistarSiteWrapper):
    """
    A facade over the hosted legistar site data scraper, tuned for
    the legistar site as configured for Chicago.
    """

    def pluck_record(self, summary, legislation_attrs):
        # re-order the sponsor name by '[First] [Last]' instead of '[Last], [First]'
        sponsors = legislation_attrs['Sponsors']
        first_name_first_sponsors = []
        for sponsor in sponsors :
            if ',' in sponsor :
                name_list = sponsor.rsplit(',', 1)
                name_list.reverse()
                sponsor = ' '.join(name_list).strip().replace(',', '')
            first_name_first_sponsors.append(sponsor)

        record = {
            'key' : key,
            'id' : summary['Record #'],
            'url' : summary['URL'],
            'type' : summary['Type'],
            'status' : summary['Status'],
            'title' : summary['Title'],
            'controlling_body' : legislation_attrs['Current Controlling Legislative Body'],
            'intro_date' : self.convert_date(summary['Intro Date']),
            'final_date' : self.convert_date(summary.setdefault('Final Date', '')),
            'version' : summary.setdefault('Version', ''),
            #'contact' : None,
            'sponsors' : first_name_first_sponsors,
            # probably remove this from the model as well
            'minutes_url'  : None
        }
        return record

    def pluck_attachments(self, legislation_attrs):
        try:
            attachments = legislation_attrs['Attachments']
            for attachment in attachments:
                attachment['key'] = key
                attachment['file'] = attachment['label']
                attachment['description'] = attachment['label']
                del attachment['label']
        except KeyError:
            attachments = []

        return attachments

    def pluck_action(self, key, action):
        act = {
            'key' : key,
            'date_taken' : self.convert_date(action['Date']),
            'acting_body' : action['Action By']['label'],
            'motion' : action['Result'],
            'description' : action['Status'],
            'notes' : ''
        }
        return act
