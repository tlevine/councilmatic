import datetime
import time
import httplib
import logging
import re
import urllib2
import utils
import urlparse
from collections import defaultdict
import pdb

from legistar.scraper import LegistarScraper
from legistar.config import Config, DEFAULT_CONFIG

log = logging.getLogger(__name__)


class HostedLegistarSiteWrapper (object):
    """
    A generic facade over hosted legistar site data scraper.
    It is responsible for interpreting data scraped out of the site by LegistarScraper.
    The main external point of interaction is scrape_legis_file.
    NOTE that this is a superclass that will not run by itself and isn't
    meant to be; you are expected to run a subclass that implements
    some functions with names starting with "pluck".

    requires: BeautifulSoup, mechanize
    """

    def __init__(self, **options):
        self.scraper = LegistarScraper(options)
        self.legislation_summaries =  self.scraper.searchLegislation('')

    def scrape_legis_file(self, key, summary):
        '''Extract a record from the given document (soup). The key is for the
           sake of record-keeping.  It is the key passed to the site URL.'''

        while True :
            try:
                legislation_attrs, legislation_history = self.scraper.expandLegislationSummary(summary)
                break
            except urllib2.URLError as e:
                print e
                print 'skipping to next leg record'
            except AttributeError as e :
                print e
                print 'skipping to next leg record'
            while True :
                try:
                    summary = self.legislation_summaries.next()
                    break
                except urllib2.URLError as e:
                    print e
                    print 'sleeping for five minutes'
                    time.sleep('360')

        parsed_url = urlparse.urlparse(summary['URL'])
        key = urlparse.parse_qs(parsed_url.query)['ID'][0]
        
        record = self.pluck_record(key, summary, legislation_attrs)

        attachments = self.pluck_attachments(key, legislation_attrs)

        actions = []
        for act in legislation_history :
            try:
                act_details, act_votes = self.scraper.expandHistorySummary(act)
            except (KeyError, AttributeError) as e:
                print e
                print summary

            try:
                action = self.pluck_action(key, act)
            except TypeError as e:
                print e
                print summary
                continue
            actions.append(action)

        # we should probably remove this from the model since the hosted
        # legistar does not have minutes
        minutes = []

        log.info('Scraped legfile with key %r' % (key,))
        log.debug("%r %r %r %r" % (record, attachments, actions, minutes))

        return record, attachments, actions, minutes

    def convert_date(self, orig_date):
        if orig_date:
            return datetime.datetime.strptime(orig_date, '%m/%d/%Y').date()
        else:
            return ''


    def check_for_new_content(self, last_key):
        '''Grab the next legislation summary row. Doesn't use the last_key
           parameter; just starts at the beginning for each instance of the
           scraper.
        '''
        try:
            print 'next leg record'
            next_summary = self.legislation_summaries.next()
            return 0, next_summary
        except StopIteration:
            return None, None

    def init_pdf_cache(self, pdf_mapping) :
        pass
        
    
