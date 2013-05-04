
from hosted_legistar_scraper import HostedLegistarSiteWrapper

class OaklandHostedLegistarSiteWrapper (HostedLegistarSiteWrapper):
    """
    A facade over the hosted legistar site data scraper, tuned for
    the legistar site as configured for Oakland.
    """

    # TODO: following implemenations are for Chicago.
    # they need to be updated for oakland


    # summary:  {u'Status': u'To be Scheduled', u'Title': u'Subject:\tFiscal Year 2011-2012 WIA Funds Reallocation\r\nFrom:\t\tOffice Of Economic And Workforce Development\r\nRecommendation:  Adopt A Resolution Authorizing The City Administrator 1) To Reallocate Fiscal Year 2011-2012 Workforce Investment Act Formula Funds That Are At Risk Of De-Obligation, With The Approval Of The Workforce Investment Board, Without Returning To City Council; And 2) To Amend The Comprehensive One Stop Career Center Contract With The Oakland Private Industry Council, Inc. To Include An Additional $200,000 In Fiscal Year 2011-2012 Workforce Investment Act Dislocated Worker Fund', 'URL': u'http://oakland.legistar.com/LegislationDetail.aspx?ID=1344903&GUID=F202C67A-EE66-4270-97C9-CB73370D4E07', u'File #': u'12-0422', u'Final Action': u'', u'Type': u'City Resolution', u'File Created': u'4/8/2013'}
    # leg_attrs:  {u'Status': u'To be Scheduled', u'On agenda': u'', u'Name': u'Fiscal Year 2011-2012 WIA Funds Reallocation', u'File #': u'12-0422', u'In control': u'Concurrent Meeting of the Oakland Redevelopment Agency / City Council', u'Title': u'Subject:\tFiscal Year 2011-2012 WIA Funds Reallocation\r\nFrom:\t\tOffice Of Economic And Workforce Development\r\nRecommendation:  Adopt A Resolution Authorizing The City Administrator 1) To Reallocate Fiscal Year 2011-2012 Workforce Investment Act Formula Funds That Are At Risk Of De-Obligation, With The Approval Of The Workforce Investment Board, Without Returning To City Council; And 2) To Amend The Comprehensive One Stop Career Center Contract With The Oakland Private Industry Council, Inc. To Include An Additional $200,000 In Fiscal Year 2011-2012 Workforce Investment Act Dislocated Worker Funds For Training Services For Dislocated Workers Effective April 1, 2013 To June 30, 2013; On The April 23, 2013 Community & Economic Development Committee Agenda', u'Sponsors': [], u'Version': u'1', u'Final action': u'', u'Type': u'City Resolution', u'File created': u'4/8/2013'}

    def pluck_record(self, key, summary, legislation_attrs):
        record = {
            'key' : key,
            'id' : summary['File #'],
            'url' : summary['URL'],
            'type' : summary['Type'],
            'status' : summary['Status'],
            'title' : summary['Title'],
            'controlling_body' : legislation_attrs['In control'],
            'intro_date' : self.convert_date(legislation_attrs['File created']),
            'final_date' : self.convert_date(summary.setdefault('Final Action', '')),
            'version' : summary.setdefault('Version', ''),  # TODO: can't find this field in chicago or oakland
            # 'contact' : None,
            'sponsors' : legislation_attrs.get('Sponsors', ''),  # TODO: Oakland doesn't seem to enter sponsor info at this time
            # probably remove this from the model as well
            'minutes_url'  : None
        }
        return record

    def pluck_attachments(self, key, legislation_attrs):
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
            'acting_body' : action['Action By'],
            'motion' : action['Result'],
            'description' : action['Action'],
            'notes' : ''
        }
        return act

