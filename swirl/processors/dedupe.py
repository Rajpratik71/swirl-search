'''
@author:     Sid Probstein
@contact:    sid@swirl.today
'''

from swirl.processors.processor import *
from django.conf import settings
from swirl.spacy import nlp

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


#############################################
#############################################

SWIRL_DEDUPE_FIELD = 'resource.conversationId'
SWIRL_DEDUPE_SIMILARITY_FIELDS = getattr(settings, 'SWIRL_DEDUPE_SIMILARITY_FIELDS', ['title', 'body'])
SWIRL_DEDUPE_SIMILARITY_MINIMUM = getattr(settings, 'SWIRL_DEDUPE_SIMILARITY_MINIMUM', 0.95)

class DedupeByFieldPostResultProcessor(PostResultProcessor):

    type="DedupeByFieldPostResultProcessor"

    def _get_dedup_field_value_from_rec_or_payload(self, rec, fname):
        if fname in rec:
            return rec[fname]
        elif fname in rec.get('payload',[]):
            return rec['payload'][fname]
        else:
            return None

    def process(self):

        dupes = 0
        dedupe_key_dict = {}
        log.info('DNDEBUG trace DedupeByFieldPostResultProcessor')
        for result in self.results:
            deduped_item_list = []
            for item in result.json_results:
                log.info(f'DNDEBUG {SWIRL_DEDUPE_FIELD} in item:{item} truth:{SWIRL_DEDUPE_FIELD in item}')
                dd_value = self._get_dedup_field_value_from_rec_or_payload(item, SWIRL_DEDUPE_FIELD)

                if dd_value:
                    if dd_value:
                        if dd_value in dedupe_key_dict:
                            # dupe
                            dupes = dupes + 1
                            continue
                        else:
                            # not dupe
                            dedupe_key_dict[dd_value] = 1
                    else:
                        # dedupe key blank
                        # logger.info(f"{self}: Ignoring result {item}, {SWIRL_DEDUPE_FIELD} is blank")
                        pass
                else:
                    # dedupe key missing
                    # self.warning(f"Ignoring result {item}, {SWIRL_DEDUPE_FIELD} is missing")
                    pass
                # end if
                deduped_item_list.append(item)
            # end for
            result.json_results = deduped_item_list
            result.save()
        # end for

        self.results_updated = dupes
        return self.results_updated

#############################################

class DedupeBySimilarityPostResultProcessor(PostResultProcessor):

    type="DedupeBySimilarityPostResultProcessor"

    def process(self):

        dupes = 0
        nlp_list = []
        for result in self.results:
            deduped_item_list = []
            for item in result.json_results:
                content = ""
                for field in SWIRL_DEDUPE_SIMILARITY_FIELDS:
                    if field in item:
                        if field:
                            content = content + ' ' + item[field].strip()
                        # end if
                # end for
                content = content.strip()
                nlp_content = nlp(content)
                dupe = False
                max_sim = 0.0
                for n in nlp_list:
                    sim = nlp_content.similarity(n)
                    if sim > SWIRL_DEDUPE_SIMILARITY_MINIMUM:
                        # similar
                        dupe = True
                        dupes = dupes + 1
                        break
                    else:
                        if sim > max_sim:
                            max_sim = sim
                    # end if
                # end for
                if not dupe:
                    nlp_list.append(nlp_content)
                    deduped_item_list.append(item)
                # end if
            # end for
            result.json_results = deduped_item_list
            logger.info(f"{self}: result.save()")
            result.save()
        # end for

        self.results_updated = dupes
        return self.results_updated