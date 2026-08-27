"""Synchronize Aeon Timeline 2 and novelibre

Version 5.9.3
Requires Python 3.7+
Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/aeon2yw
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import argparse
import os
from pathlib import Path
import sys

import gettext
import locale

LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation(
        'nv_aeon2',
        LOCALE_PATH,
        languages=[CURRENT_LANGUAGE],
    )
    _ = t.gettext
except:

    def _(message):
        return message



from datetime import datetime
from datetime import timedelta

import codecs
from json import JSONDecodeError
import json
import zipfile



try:
    LOCALE_PATH
except NameError:
    locale.setlocale(locale.LC_TIME, "")
    LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
    try:
        CURRENT_LANGUAGE = locale.getlocale()[0][:2]
    except:
        CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
    try:
        t = gettext.translation(
            'novelibre',
            LOCALE_PATH,
            languages=[CURRENT_LANGUAGE],
        )
        _ = t.gettext
    except:

        def _(message):
            return message


ROOT_PREFIX = 'rt'
CHAPTER_PREFIX = 'ch'
PLOT_LINE_PREFIX = 'ac'
SECTION_PREFIX = 'sc'
PLOT_POINT_PREFIX = 'ap'
CHARACTER_PREFIX = 'cr'
LOCATION_PREFIX = 'lc'
ITEM_PREFIX = 'it'
PRJ_NOTE_PREFIX = 'pn'
CH_ROOT = f'{ROOT_PREFIX}{CHAPTER_PREFIX}'
PL_ROOT = f'{ROOT_PREFIX}{PLOT_LINE_PREFIX}'
CR_ROOT = f'{ROOT_PREFIX}{CHARACTER_PREFIX}'
LC_ROOT = f'{ROOT_PREFIX}{LOCATION_PREFIX}'
IT_ROOT = f'{ROOT_PREFIX}{ITEM_PREFIX}'
PN_ROOT = f'{ROOT_PREFIX}{PRJ_NOTE_PREFIX}'

BRF_SYNOPSIS_SUFFIX = '_brf_synopsis'
CHAPTERLIST_SUFFIX = '_chapterlist_tmp'
CHAPTERS_SUFFIX = '_chapters_tmp'
CHAPTER_BOARD_SUFFFIX = '_sectioncards'
CHARACTERS_SUFFIX = '_characters_tmp'
CHARACTER_REPORT_SUFFIX = '_character_report'
CHARLIST_SUFFIX = '_charlist_tmp'
DATA_SUFFIX = '_data'
ELEMENT_NOTES_SUFFIX = '_element_note_report',
FULL_MANUSCRIPT_SUFFIX = '_full_tmp'
GRID_REPORT_SUFFIX = '_grid_report'
GRID_SUFFIX = '_grid_tmp'
ITEMLIST_SUFFIX = '_itemlist_tmp'
ITEMS_SUFFIX = '_items_tmp'
ITEM_REPORT_SUFFIX = '_item_report'
LOCATIONS_SUFFIX = '_locations_tmp'
LOCATION_REPORT_SUFFIX = '_location_report'
LOCLIST_SUFFIX = '_loclist_tmp'
MANUSCRIPT_SUFFIX = '_manuscript_tmp'
METADATA_TEXT_SUFFIX = '_metadata_text_tmp'
MINOR_MARKER = _('Minor Character')
PARTLIST_SUFFIX = '_partlist_tmp'
PARTS_SUFFIX = '_parts_tmp'
PLOTLINES_SUFFIX = '_plotlines_tmp'
PLOTLIST_SUFFIX = '_plotlist'
PLOT_LINE_BOARD_SUFFIX = '_plotcards'
PROJECTNOTES_REPORT_SUFFIX = '_projectnotes_report'
PROJECTNOTES_SUFFIX = '_projectnotes_tmp'
PROOF_SUFFIX = '_proof_tmp'
SECTIONLIST_SUFFIX = '_sectionlist'
SECTIONS_SUFFIX = '_sections_tmp'
STAGES_SUFFIX = '_structure_tmp'
STORY_STRUCT_BOARD_SUFFIX = '_stagecards'
TIMETABLE_SUFFIX = '_tt_tmp'
VIEWPOINT_BOARD_SUFFFIX = '_viewpoint_board'
XREF_SUFFIX = '_xref'

MAJOR_MARKER = _('Major Character')

NO_SCENE_FIELD_1_DEFAULT = _('Plot progress')
NO_SCENE_FIELD_2_DEFAULT = _('Characterization')
NO_SCENE_FIELD_3_DEFAULT = _('World building')
OTHER_SCENE_FIELD_1_DEFAULT = _('Opening')
OTHER_SCENE_FIELD_2_DEFAULT = _('Peak emotional moment')
OTHER_SCENE_FIELD_3_DEFAULT = _('Ending')
CR_FIELD_1_DEFAULT = _('Bio')
CR_FIELD_2_DEFAULT = _('Goals')

STATUS = [
    None,
    _('Outline'),
    _('Draft'),
    _('1st Edit'),
    _('2nd Edit'),
    _('Done')
]

SCENE = ['-', 'A', 'R', 'x']


def norm_path(path):
    if path is None:
        path = ''
    return os.path.normpath(path)


def string_to_list(text, divider=';'):
    elements = []
    try:
        tempList = text.split(divider)
        for element in tempList:
            element = element.strip()
            if element and not element in elements:
                elements.append(element)
        return elements

    except:
        return []


def list_to_string(elements, divider=';'):
    try:
        return divider.join(elements)

    except:
        return ''


def intersection(elemList, refList):
    return [elem for elem in elemList if elem in refList]


def verified_int_string(intStr):
    if intStr is not None:
        int(intStr)
    return intStr



def open_timeline(filePath):
    try:
        with zipfile.ZipFile(filePath, 'r') as myzip:
            jsonBytes = myzip.read('timeline.json')
            jsonStr = codecs.decode(jsonBytes, encoding='utf-8')
    except:
        raise RuntimeError(f'{_("Cannot read timeline data")}.')
    if not jsonStr:
        raise RuntimeError(f'{_("No JSON part found in timeline data")}.')
    try:
        jsonData = json.loads(jsonStr)
    except JSONDecodeError:
        raise RuntimeError(f'{_("Invalid JSON data in timeline")}.')
    return jsonData


def save_timeline(jsonData, filePath):
    backedUp = False
    if os.path.isfile(filePath):
        try:
            os.replace(filePath, f'{filePath}.bak')
        except:
            raise RuntimeError(
                    f'{_("Cannot overwrite file")}: '
                    f'"{norm_path(filePath)}".'
            )
        else:
            backedUp = True
    try:
        with zipfile.ZipFile(
            filePath,
            'w',
            compression=zipfile.ZIP_DEFLATED
        ) as f:
            f.writestr('timeline.json', json.dumps(jsonData))
    except:
        if backedUp:
            os.replace(f'{filePath}.bak', filePath)
        raise RuntimeError(f'{_("Cannot write file")}: "{norm_path(filePath)}".')

import uuid


class GuidGenerator:

    def __init__(self, filePath):
        self._url = f'file:///{filePath}'

    def get_guid(self, fragment):
        return str(
            uuid.uuid3(
                uuid.NAMESPACE_URL,
                f'{self._url}#{fragment}'
            )
        )


class NarrativeMissing(RuntimeError):
    pass



def new_id(elements, prefix=''):
    i = 1
    while f'{prefix}{i}' in elements:
        i += 1
    return f'{prefix}{i}'

from abc import ABC
from urllib.parse import quote



class File(ABC):
    DESCRIPTION = _('File')
    EXTENSION = None
    SUFFIX = None

    def __init__(self, filePath, **kwargs):
        self.novel = None
        self._filePath = None
        self.projectName = None
        self.projectPath = None
        self.projectStructureModified = False
        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath: str):
        filePath = filePath.replace('\\', '/')
        suffix = self.SUFFIX or ''
        if filePath.lower().endswith(f'{suffix}{self.EXTENSION}'.lower()):
            self._filePath = filePath
            try:
                head, tail = os.path.split(os.path.realpath(filePath))
            except:
                head, tail = os.path.split(filePath)
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(
                tail.replace(f'{suffix}{self.EXTENSION}', '')
            )

    def is_locked(self):
        return False

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError



class JsonTimeline2(File):
    EXTENSION = '.aeonzip'
    DESCRIPTION = _('Aeon Timeline 2 project')
    SUFFIX = ''
    DATE_LIMIT = (datetime(1, 1, 1) - datetime.min).total_seconds()

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self._nvSvc = kwargs['nv_service']



        url = f'{self.projectName}'
        self._guidGen = GuidGenerator(url)

        self._jsonData = None

        self._entityNarrative = kwargs['narrative_arc']

        self._propertyDesc = kwargs['property_description']
        self._propertyNotes = kwargs['property_notes']
        self._propertyMoonphase = kwargs['property_moonphase']

        self._roleArc = kwargs['role_arc']
        self._rolePlotline = kwargs['role_plotline']
        self._roleCharacter = kwargs['role_character']
        self._roleLocation = kwargs['role_location']
        self._roleItem = kwargs['role_item']

        self._typeArc = kwargs['type_arc']
        self._typeCharacter = kwargs['type_character']
        self._typeLocation = kwargs['type_location']
        self._typeItem = kwargs['type_item']

        self._tplDateGuid = None
        self._typeArcGuid = None
        self._typeCharacterGuid = None
        self._typeLocationGuid = None
        self._typeItemGuid = None
        self._roleArcGuid = None
        self._rolePlotlineGuid = None
        self._roleCharacterGuid = None
        self._roleLocationGuid = None
        self._roleItemGuid = None
        self._entityNarrativeGuid = None
        self._propertyDescGuid = None
        self._propertyNotesGuid = None
        self._propertyMoonphaseGuid = None

        self.referenceDate = None
        self._addMoonphase = kwargs['add_moonphase']
        self._sectionColor = kwargs['color_section']
        self._eventColor = kwargs['color_event']
        self._timestampMax = 0
        self._displayIdMax = 0.0
        self._colors = {}
        self._arcCount = 0
        self._characterGuidsById = {}
        self._locationGuidsById = {}
        self._itemGuidsById = {}
        self._arcGuidsById = {}
        self._trashEvents = []

    def read(self):
        self._set_reference_date(self.novel)
        self._jsonData = open_timeline(self.filePath)

        self._r_fetch_color_definitions()
        self._r_fetch_date_definition()
        self._r_fetch_arc_type_and_roles_guid()
        self._r_fetch_character_type_and_roles_guid()
        self._r_fetch_location_type_and_roles_guid()
        self._r_fetch_item_type_and_roles_guid()
        self._r_fetch_property_moonphase_guid()
        self._r_fetch_property_notes_guid()
        self._r_fetch_property_desc_guid()


        self._r_check_source_characters()
        self._r_check_source_locations()
        self._r_check_source_items()
        self._r_check_source_arcs()

        targetScIdsByTitle = self._r_check_target_sections()
        targetCrIdsByTitle = self._r_check_target_characters()
        targetItIdsByTitle = self._r_check_target_items()
        targetLcIdsByTitle = self._r_check_target_locations()
        targetAcIdsByTitle = self._r_check_target_arcs()

        crIdsByGuid = self._r_fetch_character_guids_by_id(targetCrIdsByTitle)
        lcIdsByGuid = self._r_fetch_location_guids_by_id(targetLcIdsByTitle)
        itIdsByGuid = self._r_fetch_item_guids_by_id(targetItIdsByTitle)
        acIdsByGuid = self._r_fetch_arc_guids_by_id(targetAcIdsByTitle)

        if not self._entityNarrativeGuid:
            raise NarrativeMissing(
                f'{_("The selected project has no narrative arc")} '
                f'"{self._entityNarrative}".'
            )

        narrativeEvents, scIdsByDate = self._r_update_or_create_sections(
            targetScIdsByTitle,
            crIdsByGuid,
            lcIdsByGuid,
            itIdsByGuid,
            acIdsByGuid,
        )

        self._r_make_sections_deleted_in_aeon_unused(narrativeEvents)
        self._r_put_new_sections_into_new_chapter(scIdsByDate)
        self._r_adjust_timestamp()

    def write(self, source):
        self._set_reference_date(source)


        (
            relatedCharacters,
            relatedLocations,
            relatedItems,
            relatedArcs,
        ) = self._w_get_related_elements(source)

        self._w_check_source_characters(source, relatedCharacters)
        self._w_check_source_locations(source, relatedLocations)
        self._w_check_source_items(source, relatedItems)
        self._w_check_source_arcs(source, relatedArcs)

        srcScnTitles = self._w_check_source_sections(source)
        self._w_collect_trashed_sections(srcScnTitles)

        scIdsByTitle = self._w_check_target_sections()
        crIdsByTitle = self._w_check_target_characters()
        lcIdsByTitle = self._w_check_target_locations()
        itIdsByTitle = self._w_check_target_items()
        acIdsByTitle = self._w_check_target_arcs()

        self._w_create_json_type_character_if_missing()
        self._w_create_json_type_location_if_missing()
        self._w_create_json_type_item_if_missing()
        self._w_create_json_type_arc_if_missing()
        self._w_create_json_role_arc_if_missing()
        self._w_create_json_role_character_if_missing()
        self._w_create_json_role_location_if_missing()
        self._w_create_json_role_item_if_missing()
        self._w_create_json_role_plotline_if_missing()
        self._w_create_json_property_notes_if_missing()
        self._w_create_json_property_desc_if_missing()
        self._w_create_json_property_moonphase_if_missing()

        crIdsBySrcId = self._w_update_characters_from_source(
            source,
            crIdsByTitle,
            relatedCharacters,
        )
        lcIdsBySrcId = self._w_update_locations_from_source(
            source,
            lcIdsByTitle,
            relatedLocations,
        )
        itIdsBySrcId = self._w_update_items_from_source(
            source,
            itIdsByTitle,
            relatedItems,
        )
        acIdsBySrcId = self._w_update_arcs_from_source(
            source,
            acIdsByTitle,
            relatedArcs,
        )
        self._w_update_sections_from_source(
            source,
            scIdsByTitle,
            crIdsBySrcId,
            lcIdsBySrcId,
            itIdsBySrcId,
            acIdsBySrcId,
        )


        self._w_create_json_narrative_arc_if_missing()
        self._w_update_json_events_from_sections(scIdsByTitle)
        self._w_delete_trashed_events(scIdsByTitle)

        save_timeline(self._jsonData, self.filePath)

    def _r_adjust_timestamp(self):
        if self._timestampMax == 0:
            self._timestampMax = (
                (self.referenceDate - datetime.min).total_seconds()
            )

    def _r_check_source_arcs(self):
        arcNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] == self._typeArcGuid:
                if entity['name'] in arcNames:
                    raise RuntimeError(
                        _('Ambiguous Aeon arc "{}".').format(
                            entity['name'])
                    )

                arcNames.append(entity['name'])

    def _r_check_source_characters(self):
        characterNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] == self._typeCharacterGuid:
                if entity['name'] in characterNames:
                    raise RuntimeError(
                        _('Ambiguous Aeon character "{}".').format(
                            entity['name'])
                    )

                characterNames.append(entity['name'])

    def _r_check_source_items(self):
        itemNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] == self._typeItemGuid:
                if entity['name'] in itemNames:
                    raise RuntimeError(
                        _('Ambiguous Aeon item "{}".').format(
                            entity['name'])
                    )

                itemNames.append(entity['name'])

    def _r_check_source_locations(self):
        locationNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] == self._typeLocationGuid:
                if entity['name'] in locationNames:
                    raise RuntimeError(
                        _('Ambiguous Aeon location "{}".').format(
                            entity['name'])
                    )

                locationNames.append(entity['name'])

    def _r_check_target_arcs(self):
        targetAcIdsByTitle = {}
        for acId in self.novel.plotLines:
            title = self.novel.plotLines[acId].title
            if title:
                if title in targetAcIdsByTitle:
                    raise RuntimeError(
                        _('Ambiguous novelibre plot line "{}".').format(
                            title)
                    )

                targetAcIdsByTitle[title] = acId
        return targetAcIdsByTitle

    def _r_check_target_characters(self):
        targetCrIdsByTitle = {}
        for crId in self.novel.characters:
            title = self.novel.characters[crId].title
            if title:
                if title in targetCrIdsByTitle:
                    raise RuntimeError(
                        _('Ambiguous novelibre character "{}".').format(
                            title)
                    )

                targetCrIdsByTitle[title] = crId
        return targetCrIdsByTitle

    def _r_check_target_items(self):
        targetItIdsByTitle = {}
        for itId in self.novel.items:
            title = self.novel.items[itId].title
            if title:
                if title in targetItIdsByTitle:
                    raise RuntimeError(
                        _('Ambiguous novelibre item "{}".').format(
                            title)
                    )

                targetItIdsByTitle[title] = itId
        return targetItIdsByTitle

    def _r_check_target_locations(self):
        targetLcIdsByTitle = {}
        for lcId in self.novel.locations:
            title = self.novel.locations[lcId].title
            if title:
                if title in targetLcIdsByTitle:
                    raise RuntimeError(
                        _('Ambiguous novelibre location "{}".').format(
                            title)
                    )

                targetLcIdsByTitle[title] = lcId
        return targetLcIdsByTitle

    def _r_check_target_sections(self):
        targetScIdsByTitle = {}
        for scId in self.novel.sections:
            title = self.novel.sections[scId].title
            if title:
                if title in targetScIdsByTitle:
                    raise RuntimeError(
                        _('Ambiguous novelibre section title "{}".').format(
                            title)
                    )

                targetScIdsByTitle[title] = scId
        return targetScIdsByTitle

    def _r_fetch_arc_guids_by_id(self, targetAcIdsByTitle):
        acIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeArcGuid:
                continue

            if entity['name'] in targetAcIdsByTitle:
                plId = targetAcIdsByTitle[entity['name']]
            elif entity['name'] != self._entityNarrative:

                plId = new_id(self.novel.plotLines, prefix=PLOT_LINE_PREFIX)
                self.novel.plotLines[plId] = self._nvSvc.new_plot_line(
                    title=entity['name'],
                    shortName=entity['name']
                )
                self.novel.tree.append(PL_ROOT, plId)
            if entity['name'] == self._entityNarrative:
                self._entityNarrativeGuid = entity['guid']
            else:
                acIdsByGuid[entity['guid']] = plId
                self._arcGuidsById[plId] = entity['guid']
                self._arcCount += 1
        return acIdsByGuid

    def _r_fetch_arc_type_and_roles_guid(self):
        for tplTyp in self._jsonData['template']['types']:
            if tplTyp['name'] == self._typeArc:
                self._typeArcGuid = tplTyp['guid']
                for tplTypRol in tplTyp['roles']:
                    if tplTypRol['name'] == self._roleArc:
                        self._roleArcGuid = tplTypRol['guid']
                    elif tplTypRol['name'] == self._rolePlotline:
                        self._rolePlotlineGuid = tplTypRol['guid']

    def _r_fetch_character_guids_by_id(self, targetCrIdsByTitle):
        crIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeCharacterGuid:
                continue

            if entity['name'] in targetCrIdsByTitle:
                crId = targetCrIdsByTitle[entity['name']]
            else:
                crId = new_id(self.novel.characters, prefix=CHARACTER_PREFIX)
                self.novel.characters[crId] = self._nvSvc.new_character(
                    title=entity['name']
                )
                self.novel.tree.append(CR_ROOT, crId)
            crIdsByGuid[entity['guid']] = crId
            self._characterGuidsById[crId] = entity['guid']
            if entity['notes']:
                self.novel.characters[crId].notes = entity['notes']
            else:
                entity['notes'] = ''
            createRangePosition = entity.get('createRangePosition', None)
            if createRangePosition:
                timestamp = createRangePosition['timestamp']
                if timestamp >= self.DATE_LIMIT:
                    birthDate = datetime.min + timedelta(seconds=timestamp)
                    self.novel.characters[crId].birthDate = (
                        birthDate.isoformat().split('T')[0]
                    )
            destroyRangePosition = entity.get('destroyRangePosition', None)
            if destroyRangePosition:
                timestamp = destroyRangePosition['timestamp']
                if timestamp >= self.DATE_LIMIT:
                    deathDate = datetime.min + timedelta(seconds=timestamp)
                    self.novel.characters[crId].deathDate = (
                        deathDate.isoformat().split('T')[0]
                    )
        return crIdsByGuid

    def _r_fetch_character_type_and_roles_guid(self):
        for tplTyp in self._jsonData['template']['types']:
            if tplTyp['name'] == self._typeCharacter:
                self._typeCharacterGuid = tplTyp['guid']
                for tplTypRol in tplTyp['roles']:
                    if tplTypRol['name'] == self._roleCharacter:
                        self._roleCharacterGuid = tplTypRol['guid']
                        break

    def _r_fetch_color_definitions(self):
        for tplCol in self._jsonData['template']['colors']:
            self._colors[tplCol['name']] = tplCol['guid']

    def _r_fetch_date_definition(self):
        for tplRgp in self._jsonData['template']['rangeProperties']:
            if tplRgp['type'] == 'date':
                for tplRgpCalEra in tplRgp['calendar']['eras']:
                    if tplRgpCalEra['name'] == 'AD':
                        self._tplDateGuid = tplRgp['guid']
                        break

        if self._tplDateGuid is None:
            raise RuntimeError(_('"AD" era is missing in the calendar.'))

    def _r_fetch_item_guids_by_id(self, targetItIdsByTitle):
        itIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeItemGuid:
                continue

            if entity['name'] in targetItIdsByTitle:
                itId = targetItIdsByTitle[entity['name']]
            else:
                itId = new_id(self.novel.items, prefix=ITEM_PREFIX)
                self.novel.items[itId] = self._nvSvc.new_world_element()
                self.novel.items[itId].title = entity['name']
                self.novel.tree.append(IT_ROOT, itId)  # Create a new item.
            itIdsByGuid[entity['guid']] = itId
            self._itemGuidsById[itId] = entity['guid']
        return itIdsByGuid

    def _r_fetch_item_type_and_roles_guid(self):
        for tplTyp in self._jsonData['template']['types']:
            if tplTyp['name'] == self._typeItem:
                self._typeItemGuid = tplTyp['guid']
                for tplTypRol in tplTyp['roles']:
                    if tplTypRol['name'] == self._roleItem:
                        self._roleItemGuid = tplTypRol['guid']
                        break

    def _r_fetch_location_guids_by_id(self, targetLcIdsByTitle):
        lcIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeLocationGuid:
                continue

            if entity['name'] in targetLcIdsByTitle:
                lcId = targetLcIdsByTitle[entity['name']]
            else:
                lcId = new_id(self.novel.locations, prefix=LOCATION_PREFIX)
                self.novel.locations[lcId] = self._nvSvc.new_world_element()
                self.novel.locations[lcId].title = entity['name']
                self.novel.tree.append(LC_ROOT, lcId)  # Create a new location.
            lcIdsByGuid[entity['guid']] = lcId
            self._locationGuidsById[lcId] = entity['guid']
        return lcIdsByGuid

    def _r_fetch_location_type_and_roles_guid(self):
        for tplTyp in self._jsonData['template']['types']:
            if tplTyp['name'] == self._typeLocation:
                self._typeLocationGuid = tplTyp['guid']
                for tplTypRol in tplTyp['roles']:
                    if tplTypRol['name'] == self._roleLocation:
                        self._roleLocationGuid = tplTypRol['guid']
                        break

    def _r_fetch_property_desc_guid(self):
        for tplPrp in self._jsonData['template']['properties']:
            if tplPrp['name'] == self._propertyDesc:
                self._propertyDescGuid = tplPrp['guid']
                return

    def _r_fetch_property_moonphase_guid(self):
        for tplPrp in self._jsonData['template']['properties']:
            if tplPrp['name'] == self._propertyMoonphase:
                self._propertyMoonphaseGuid = tplPrp['guid']
                return

    def _r_fetch_property_notes_guid(self):
        for tplPrp in self._jsonData['template']['properties']:
            if tplPrp['name'] == self._propertyNotes:
                self._propertyNotesGuid = tplPrp['guid']
                return

    def _r_make_sections_deleted_in_aeon_unused(self, narrativeEvents):
        for scId in self.novel.sections:
            if not scId in narrativeEvents:
                if self.novel.sections[scId].scType == 0:
                    self.novel.sections[scId].scType = 1

    def _r_put_new_sections_into_new_chapter(self, scIdsByDate):
        sectionsInChapters = []
        for chId in self.novel.tree.get_children(CH_ROOT):
            sectionsInChapters.extend(self.novel.tree.get_children(chId))

        newChapterId = new_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
        newChapter = self._nvSvc.new_chapter(title=_('New sections'), chType=0)
        srtSections = sorted(scIdsByDate.items())
        for __, scList in srtSections:
            for scId in scList:
                if not scId in sectionsInChapters:
                    if not newChapterId in self.novel.tree.get_children(
                        CH_ROOT
                    ):
                        self.novel.chapters[newChapterId] = newChapter
                        self.novel.tree.append(CH_ROOT, newChapterId)
                    self.novel.tree.append(newChapterId, scId)

    def _r_update_or_create_sections(
            self,
            targetScIdsByTitle,
            crIdsByGuid,
            lcIdsByGuid,
            itIdsByGuid,
            acIdsByGuid
    ):
        scIdsByDate = {}
        scnTitles = []
        narrativeEvents = []
        for event in self._jsonData['events']:

            isNarrative = False
            for evtRel in event['relationships']:
                if evtRel['role'] == self._roleArcGuid:
                    if evtRel['entity'] == self._entityNarrativeGuid:
                        isNarrative = True
                        break

            eventTitle = event['title'].strip()
            if eventTitle in scnTitles:
                raise RuntimeError(
                    _('Ambiguous Aeon event title "{}".').format(eventTitle)
                )

            scnTitles.append(eventTitle)

            if eventTitle in targetScIdsByTitle:
                scId = targetScIdsByTitle[eventTitle]
            elif isNarrative:
                scId = new_id(self.novel.sections, prefix=SECTION_PREFIX)
                self.novel.sections[scId] = self._nvSvc.new_section(
                    title=eventTitle,
                    status=1,
                    scType=0,
                    scene=0,
                )
            else:
                continue

            narrativeEvents.append(scId)
            displayId = float(event['displayId'])
            if displayId > self._displayIdMax:
                self._displayIdMax = displayId

            hasDescription = False
            hasNotes = False
            for evtVal in event['values']:

                if evtVal['property'] == self._propertyDescGuid:
                    hasDescription = True
                    if evtVal['value']:
                        self.novel.sections[scId].desc = evtVal['value']

                elif evtVal['property'] == self._propertyNotesGuid:
                    hasNotes = True
                    if evtVal['value']:
                        self.novel.sections[scId].notes = evtVal['value']

            if not hasDescription:
                event['values'].append({
                    'property': self._propertyDescGuid,
                    'value': ''
                })
            if not hasNotes:
                event['values'].append({
                    'property': self._propertyNotesGuid,
                    'value': ''
                })

            if event['tags']:
                self.novel.sections[scId].tags = []
                for evtTag in event['tags']:
                    self.novel.sections[scId].tags.append(evtTag)

            timestamp = 0
            for evtRgv in event['rangeValues']:
                if evtRgv['rangeProperty'] == self._tplDateGuid:
                    timestamp = evtRgv['position']['timestamp']
                    if timestamp >= self.DATE_LIMIT:
                        sectionStart = (
                            datetime.min + timedelta(seconds=timestamp)
                        )
                        startDateTime = sectionStart.isoformat().split('T')

                        if self.novel.sections[scId].day is not None:
                            sectionDelta = sectionStart - self.referenceDate
                            self.novel.sections[scId].day = str(
                                sectionDelta.days
                            )
                        elif (
                            self.novel.sections[scId].time is not None
                            and self.novel.sections[scId].date is None
                        ):
                            self.novel.sections[scId].day = '0'
                        else:
                            self.novel.sections[scId].date = startDateTime[0]
                        self.novel.sections[scId].time = startDateTime[1]

                        if (
                            'years' in evtRgv['span']
                            or 'months' in evtRgv['span']
                        ):
                            endYear = sectionStart.year
                            endMonth = sectionStart.month
                            if 'years' in evtRgv['span']:
                                endYear += evtRgv['span']['years']
                            if 'months' in evtRgv['span']:
                                endMonth += evtRgv['span']['months']
                                while endMonth > 12:
                                    endMonth -= 12
                                    endYear += 1
                            sectionEnd = datetime(
                                endYear,
                                endMonth,
                                sectionStart.day
                            )
                            sectionDuration = sectionEnd - datetime(
                                sectionStart.year,
                                sectionStart.month,
                                sectionStart.day,
                            )
                            lastsDays = sectionDuration.days
                            lastsHours = sectionDuration.seconds // 3600
                            lastsMinutes = (
                                (sectionDuration.seconds % 3600) // 60
                            )
                        else:
                            lastsDays = 0
                            lastsHours = 0
                            lastsMinutes = 0
                        if 'weeks' in evtRgv['span']:
                            lastsDays += evtRgv['span']['weeks'] * 7
                        if 'days' in evtRgv['span']:
                            lastsDays += evtRgv['span']['days']
                        if 'hours' in evtRgv['span']:
                            lastsDays += evtRgv['span']['hours'] // 24
                            lastsHours += evtRgv['span']['hours'] % 24
                        if 'minutes' in evtRgv['span']:
                            lastsHours += evtRgv['span']['minutes'] // 60
                            lastsMinutes += evtRgv['span']['minutes'] % 60
                        if 'seconds' in evtRgv['span']:
                            lastsMinutes += evtRgv['span']['seconds'] // 60
                        lastsHours += lastsMinutes // 60
                        lastsMinutes %= 60
                        lastsDays += lastsHours // 24
                        lastsHours %= 24
                        self.novel.sections[scId].lastsDays = str(
                            lastsDays
                        )
                        self.novel.sections[scId].lastsHours = str(
                            lastsHours
                        )
                        self.novel.sections[scId].lastsMinutes = str(
                            lastsMinutes
                        )
                    break

            if not timestamp in scIdsByDate:
                scIdsByDate[timestamp] = []
            scIdsByDate[timestamp].append(scId)

            self.novel.sections[scId].scType = 1
            scCharacters = []
            scLocations = []
            scItems = []
            for evtRel in event['relationships']:

                if evtRel['role'] == self._roleArcGuid:
                    if evtRel['entity'] == self._entityNarrativeGuid:
                        self.novel.sections[scId].scType = 0
                        if timestamp > self._timestampMax:
                            self._timestampMax = timestamp

                elif evtRel['role'] == self._roleCharacterGuid:
                    crId = crIdsByGuid[evtRel['entity']]
                    scCharacters.append(crId)

                elif evtRel['role'] == self._roleLocationGuid:
                    lcId = lcIdsByGuid[evtRel['entity']]
                    scLocations.append(lcId)

                elif evtRel['role'] == self._roleItemGuid:
                    itId = itIdsByGuid[evtRel['entity']]
                    scItems.append(itId)

                elif evtRel['role'] == self._rolePlotlineGuid:
                    acId = acIdsByGuid[evtRel['entity']]
                    self.novel.sections[scId].scPlotLines.append(acId)

                    acSections = self.novel.plotLines[acId].sections
                    if acSections is None:
                        acSections = []
                    acSections.append(scId)
                    self.novel.plotLines[acId].sections = acSections

            if scCharacters:
                self.novel.sections[scId].characters = scCharacters
            if scLocations:
                self.novel.sections[scId].locations = scLocations
            if scItems:
                self.novel.sections[scId].items = scItems
        return narrativeEvents, scIdsByDate

    def _set_reference_date(self, novel):
        self.referenceDate = datetime.today()
        if novel.referenceDate:
            defaultDateTime = f'{novel.referenceDate} 00:00:00'
            try:
                self.referenceDate = datetime.fromisoformat(defaultDateTime)
            except ValueError:
                pass

    def _w_check_source_arcs(self, source, relatedArcs):
        srcArcTitles = []
        for acId in source.plotLines:
            if acId in relatedArcs:
                if source.plotLines[acId].title in srcArcTitles:
                    raise RuntimeError(
                        _('Ambiguous novelibre plot line "{}".').format(
                            source.plotLines[acId].title)
                    )

                srcArcTitles.append(source.plotLines[acId].title)

    def _w_check_source_characters(self, source, relatedCharacters):
        srcChrNames = []
        for crId in source.characters:
            if crId in relatedCharacters:
                if source.characters[crId].title in srcChrNames:
                    raise RuntimeError(
                        _('Ambiguous novelibre character "{}".').format(
                            source.characters[crId].title)
                    )

                srcChrNames.append(source.characters[crId].title)

    def _w_check_source_locations(self, source, relatedLocations):
        srcLocTitles = []
        for lcId in source.locations:
            if lcId in relatedLocations:
                if source.locations[lcId].title in srcLocTitles:
                    raise RuntimeError(
                        _('Ambiguous novelibre location "{}".').format(
                            source.locations[lcId].title)
                    )

                srcLocTitles.append(source.locations[lcId].title)

    def _w_check_source_items(self, source, relatedItems):
        srcItmTitles = []
        for itId in source.items:
            if itId in relatedItems:
                if source.items[itId].title in srcItmTitles:
                    raise RuntimeError(
                        _('Ambiguous novelibre item "{}".').format(
                            source.items[itId].title)
                    )

                srcItmTitles.append(source.items[itId].title)

    def _w_check_source_sections(self, source):
        srcScnTitles = []
        for chId in source.chapters:
            if source.chapters[chId].isTrash:
                continue

            for scId in source.tree.get_children(chId):
                if source.sections[scId].title in srcScnTitles:
                    raise RuntimeError(
                        _('Ambiguous novelibre section title "{}".').format(
                            source.sections[scId].title)
                    )

                srcScnTitles.append(source.sections[scId].title)
        return srcScnTitles

    def _w_check_target_arcs(self):
        acIdsByTitle = {}
        for acId in self.novel.plotLines:
            if self.novel.plotLines[acId].title in acIdsByTitle:
                raise RuntimeError(
                    _('Ambiguous Aeon arc "{}".').format(
                        self.novel.plotLines[acId].title)
                )

            acIdsByTitle[self.novel.plotLines[acId].title] = acId
        return acIdsByTitle

    def _w_check_target_characters(self):
        crIdsByTitle = {}
        for crId in self.novel.characters:
            if self.novel.characters[crId].title in crIdsByTitle:
                raise RuntimeError(
                    _('Ambiguous Aeon character "{}".').format(
                        self.novel.characters[crId].title)
                )

            crIdsByTitle[self.novel.characters[crId].title] = crId
        return crIdsByTitle

    def _w_check_target_items(self):
        itIdsByTitle = {}
        for itId in self.novel.items:
            if self.novel.items[itId].title in itIdsByTitle:
                raise RuntimeError(
                    _('Ambiguous Aeon item "{}".').format(
                        self.novel.items[itId].title)
                )

            itIdsByTitle[self.novel.items[itId].title] = itId
        return itIdsByTitle

    def _w_check_target_locations(self):
        lcIdsByTitle = {}
        for lcId in self.novel.locations:
            if self.novel.locations[lcId].title in lcIdsByTitle:
                raise RuntimeError(
                    _('Ambiguous Aeon location "{}".').format(
                        self.novel.locations[lcId].title)
                )

            lcIdsByTitle[self.novel.locations[lcId].title] = lcId
        return lcIdsByTitle

    def _w_check_target_sections(self):
        scIdsByTitle = {}
        for scId in self.novel.sections:
            if self.novel.sections[scId].title in scIdsByTitle:

                raise RuntimeError(
                    _('Ambiguous Aeon event title "{}".').format(
                        self.novel.sections[scId].title)
                )
            scIdsByTitle[self.novel.sections[scId].title] = scId
        return scIdsByTitle

    def _w_collect_trashed_sections(self, srcScnTitles):
        for scId in self.novel.sections:
            if self.novel.sections[scId].title in srcScnTitles:
                continue

            if self.novel.sections[scId].scType == 1:
                continue

            self._trashEvents.append(scId)

    def _w_create_json_narrative_arc_if_missing(self):
        if self._entityNarrativeGuid is not None:
            return

        self._entityNarrativeGuid = self._guidGen.get_guid(
            'entityNarrativeGuid'
        )
        self._jsonData['entities'].append(
            {
                'entityType':self._typeArcGuid,
                'guid':self._entityNarrativeGuid,
                'icon':'book',
                'name':self._entityNarrative,
                'notes':'',
                'sortOrder':self._arcCount,
                'swatchColor':'orange'
                }
            )
        self._arcCount += 1

    def _w_create_json_property_desc_if_missing(self):
        if self._propertyDescGuid is not None:
            return

        n = len(self._jsonData['template']['properties'])
        self._propertyDescGuid = self._guidGen.get_guid('_propertyDescGuid')
        self._jsonData['template']['properties'].append(
            {
                'calcMode':'default',
                'calculate':False,
                'fadeEvents':False,
                'guid':self._propertyDescGuid,
                'icon':'tag',
                'isMandatory':False,
                'name':self._propertyDesc,
                'sortOrder':n,
                'type':'multitext'
            }
        )

    def _w_create_json_property_moonphase_if_missing(self):
        if self._propertyMoonphaseGuid is not None:
            return

        if not self._addMoonphase:
            return

        n = len(self._jsonData['template']['properties'])
        self._propertyMoonphaseGuid = self._guidGen.get_guid(
            '_propertyMoonphaseGuid'
        )
        self._jsonData['template']['properties'].append(
            {
                'calcMode':'default',
                'calculate':False,
                'fadeEvents':False,
                'guid':self._propertyMoonphaseGuid,
                'icon':'flag',
                'isMandatory':False,
                'name':self._propertyMoonphase,
                'sortOrder':n,
                'type':'text'
            }
        )

    def _w_create_json_property_notes_if_missing(self):
        if self._propertyNotesGuid is not None:
            return

        for tplPrp in self._jsonData['template']['properties']:
            tplPrp['sortOrder'] += 1

        self._propertyNotesGuid = self._guidGen.get_guid('_propertyNotesGuid')
        self._jsonData['template']['properties'].insert(
            0,
            {
                'calcMode':'default',
                'calculate':False,
                'fadeEvents':False,
                'guid':self._propertyNotesGuid,
                'icon':'tag',
                'isMandatory':False,
                'name':self._propertyNotes,
                'sortOrder':0,
                'type':'multitext'
            }
        )

    def _w_create_json_role_arc_if_missing(self):
        if self._roleArcGuid is not None:
            return

        for entityType in self._jsonData['template']['types']:
            if entityType['name'] == self._typeArc:
                self._roleArcGuid = self._guidGen.get_guid('_roleArcGuid')
                entityType['roles'].append(
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleArcGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._roleArc,
                        'sortOrder':0})
                return

    def _w_create_json_role_character_if_missing(self):
        if self._roleCharacterGuid is not None:
            return

        for entityType in self._jsonData['template']['types']:
            if entityType['name'] == self._typeCharacter:
                self._roleCharacterGuid = self._guidGen.get_guid(
                    '_roleCharacterGuid'
                )
                entityType['roles'].append(
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleCharacterGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._roleCharacter,
                        'sortOrder':0
                    }
                )
                return

    def _w_create_json_role_item_if_missing(self):
        if self._roleItemGuid is not None:
            return

        for entityType in self._jsonData['template']['types']:
            if entityType['name'] == self._typeItem:
                self._roleItemGuid = self._guidGen.get_guid('_roleItemGuid')
                entityType['roles'].append(
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleItemGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._roleItem,
                        'sortOrder':0
                    }
                )
                return

    def _w_create_json_role_location_if_missing(self):
        if self._roleLocationGuid is not None:
            return

        for entityType in self._jsonData['template']['types']:
            if entityType['name'] == self._typeLocation:
                self._roleLocationGuid = self._guidGen.get_guid(
                    '_roleLocationGuid'
                )
                entityType['roles'].append(
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleLocationGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._roleLocation,
                        'sortOrder':0
                    }
                )
                return

    def _w_create_json_role_plotline_if_missing(self):
        if self._rolePlotlineGuid is not None:
            return

        for entityType in self._jsonData['template']['types']:
            if entityType['name'] == self._typeArc:
                self._rolePlotlineGuid = self._guidGen.get_guid(
                    '_roleStorylineGuid'
                )
                entityType['roles'].append(
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._rolePlotlineGuid,
                        'icon':'circle filled text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._rolePlotline,
                        'sortOrder':0
                    }
                )
                return

    def _w_create_json_type_arc_if_missing(self):
        if self._typeArcGuid is not None:
            return

        self._typeArcGuid = self._guidGen.get_guid('typeArcGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append(
            {
                'color':'iconYellow',
                'guid':self._typeArcGuid,
                'icon':'book',
                'name':self._typeArc,
                'persistent':True,
                'roles':[],
                'sortOrder':typeCount
            }
        )

    def _w_create_json_type_character_if_missing(self):
        if self._typeCharacterGuid is not None:
            return

        self._typeCharacterGuid = self._guidGen.get_guid('_typeCharacterGuid')
        self._roleCharacterGuid = self._guidGen.get_guid('_roleCharacterGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append(
            {
                'color':'iconRed',
                'guid':self._typeCharacterGuid,
                'icon':'person',
                'name':self._typeCharacter,
                'persistent':False,
                'roles':[],
                'sortOrder':typeCount
            }
        )

    def _w_create_json_type_item_if_missing(self):
        if self._typeItemGuid is not None:
            return

        self._typeItemGuid = self._guidGen.get_guid('_typeItemGuid')
        self._roleItemGuid = self._guidGen.get_guid('_roleItemGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append(
            {
                'color':'iconPurple',
                'guid':self._typeItemGuid,
                'icon':'cube',
                'name':self._typeItem,
                'persistent':True,
                'roles':[],
                'sortOrder':typeCount
            }
        )

    def _w_create_json_type_location_if_missing(self):
        if self._typeLocationGuid is not None:
            return

        self._typeLocationGuid = self._guidGen.get_guid('_typeLocationGuid')
        self._roleLocationGuid = self._guidGen.get_guid('_roleLocationGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append(
            {
                'color':'iconOrange',
                'guid':self._typeLocationGuid,
                'icon':'map',
                'name':self._typeLocation,
                'persistent':True,
                'roles':[],
                'sortOrder':typeCount
            }
        )

    def _w_delete_trashed_events(self, scIdsByTitle):
        jEvents = []
        for jEvent in self._jsonData['events']:
            jTitle = jEvent['title']
            if jTitle in scIdsByTitle:
                scId = scIdsByTitle[jTitle]
                if not scId in self._trashEvents:
                    jEvents.append(jEvent)
            else:
                jEvents.append(jEvent)
        self._jsonData['events'] = jEvents

    def _w_get_json_character_date(self, isoDate):
        charaDate = datetime.fromisoformat(isoDate)
        timestamp = int((charaDate - datetime.min).total_seconds())
        return {
            "precision": "day",
            "rangePropertyGuid": self._tplDateGuid,
            "timestamp": timestamp
        }

    def _w_get_display_id(self):
        self._displayIdMax += 1
        return str(int(self._displayIdMax))

    def _w_get_new_json_event(self, section):
        event = {
            'attachments': [],
            'color': '',
            'displayId': self._w_get_display_id(),
            'guid': self._guidGen.get_guid(f'section{section.title}'),
            'links': [],
            'locked': False,
            'priority': 500,
            'rangeValues': [
                {
                    'minimumZoom':-1,
                    'position': {
                        'precision': 'minute',
                        'timestamp': self.DATE_LIMIT
                    },
                    'rangeProperty': self._tplDateGuid,
                    'span': {},
                }
            ],
            'relationships': [],
            'tags': [],
            'title': section.title,
            'values': [
                {
                    'property': self._propertyNotesGuid,
                    'value': ''
                },
                {
                    'property': self._propertyDescGuid,
                    'value': ''
                }
            ],
        }
        if section.scType == 0:
            event['color'] = self._colors[self._sectionColor]
        else:
            event['color'] = self._colors[self._eventColor]
        return event

    def _w_get_related_elements(self, source):
        relatedCharacters = []
        relatedLocations = []
        relatedItems = []
        relatedArcs = []
        for chId in source.chapters:
            if source.chapters[chId].isTrash:
                continue

            for scId in source.tree.get_children(chId):
                if source.sections[scId].characters:
                    relatedCharacters = list(set(
                        relatedCharacters + source.sections[scId].characters
                    ))
                if source.sections[scId].locations:
                    relatedLocations = list(set(
                            relatedLocations + source.sections[scId].locations
                    ))
                if source.sections[scId].items:
                    relatedItems = list(set(
                        relatedItems + source.sections[scId].items
                    ))
                if source.sections[scId].scPlotLines:
                    relatedArcs = list(set(
                        relatedArcs + source.sections[scId].scPlotLines
                    ))
        return relatedCharacters, relatedLocations, relatedItems, relatedArcs

    def _w_get_span(self, section):
        span = {}
        if section.lastsDays:
            lastsDays = int(section.lastsDays)
            if lastsDays:
                span['days'] = lastsDays
        if section.lastsHours:
            lastsHours = int(section.lastsHours)
            if lastsHours:
                span['hours'] = lastsHours
        if section.lastsMinutes:
            lastsMinutes = int(section.lastsMinutes)
            if lastsMinutes:
                span['minutes'] = lastsMinutes
        return span

    def _w_get_timestamp(self, section):
        self._timestampMax += 1
        timestamp = int(self._timestampMax)
        try:
            if section.date:
                isoDt = section.date
                if section.time:
                    isoDt = (f'{isoDt} {section.time}')
            timestamp = int(
                (datetime.fromisoformat(isoDt) - datetime.min).total_seconds()
            )
        except:
            pass
        return timestamp

    def _w_update_arcs_from_source(self, source, acIdsByTitle, linkedArcs):
        arcCount = len(self.novel.plotLines)
        acIdsBySrcId = {}
        for srcAcId in source.plotLines:
            if source.plotLines[srcAcId].title in acIdsByTitle:
                acIdsBySrcId[srcAcId] = (
                    acIdsByTitle[source.plotLines[srcAcId].title]
                )
            elif srcAcId in linkedArcs:

                acId = new_id(self.novel.plotLines, prefix=PLOT_LINE_PREFIX)
                acIdsBySrcId[srcAcId] = acId
                self.novel.plotLines[acId] = source.plotLines[srcAcId]
                arcName = self.novel.plotLines[acId].title
                newGuid = self._guidGen.get_guid(f'{acId}{arcName}')
                self._arcGuidsById[acId] = newGuid
                self._jsonData['entities'].append({
                    'entityType':self._typeArcGuid,
                    'guid':newGuid,
                    'icon':'book',
                    'name':arcName,
                    'notes':'',
                    'sortOrder':self._arcCount,
                    'swatchColor':'orange'
                })
                arcCount += 1
        return acIdsBySrcId

    def _w_update_characters_from_source(
            self,
            source,
            crIdsByTitle,
            linkedCharacters
        ):
        chrCount = len(self.novel.characters)
        crIdsBySrcId = {}
        srcIdsbyCrId = {}
        for srcCrId in source.characters:
            if source.characters[srcCrId].title in crIdsByTitle:
                crId = crIdsByTitle[source.characters[srcCrId].title]
                crIdsBySrcId[srcCrId] = crId
                srcIdsbyCrId[crId] = srcCrId
            elif srcCrId in linkedCharacters:

                crId = new_id(self.novel.characters, prefix=CHARACTER_PREFIX)
                crIdsBySrcId[srcCrId] = crId
                srcIdsbyCrId[crId] = srcCrId
                self.novel.characters[crId] = source.characters[srcCrId]
                newGuid = self._guidGen.get_guid(
                    f'{crId}{self.novel.characters[crId].title}'
                )
                self._characterGuidsById[crId] = newGuid
                jsonCharacter = {}
                birthDate = self.novel.characters[crId].birthDate
                if birthDate:
                    jsonCharacter['createRangePosition'] = (
                        self._w_get_json_character_date(birthDate)
                    )
                deathDate = self.novel.characters[crId].deathDate
                if deathDate:
                    jsonCharacter['destroyRangePosition'] = (
                        self._w_get_json_character_date(deathDate)
                    )
                jsonCharacter['entityType'] = self._typeCharacterGuid
                jsonCharacter['guid'] = newGuid
                jsonCharacter['icon'] = 'person'
                jsonCharacter['name'] = self.novel.characters[crId].title
                jsonCharacter['notes'] = ''
                jsonCharacter['sortOrder'] = chrCount
                jsonCharacter['swatchColor'] = 'darkPink'
                self._jsonData['entities'].append(jsonCharacter)
                chrCount += 1

        for entity in self._jsonData['entities']:
            if not entity['entityType'] == self._typeCharacterGuid:
                continue

            if not entity['name'] in crIdsByTitle:
                continue

            crId = crIdsByTitle[entity['name']]
            srcCrId = srcIdsbyCrId[crId]
            birthDate = source.characters[srcCrId].birthDate
            if birthDate:
                entity['createRangePosition'] = (
                    self._w_get_json_character_date(birthDate)
                )
            elif 'createRangePosition' in entity:
                    del entity['createRangePosition']
            deathDate = source.characters[srcCrId].deathDate
            if deathDate:
                entity['destroyRangePosition'] = (
                    self._w_get_json_character_date(deathDate)
                )
            elif 'destroyRangePosition' in entity:
                    del entity['destroyRangePosition']

        return crIdsBySrcId

    def _w_update_json_events_from_sections(self, scIdsByTitle):
        for jEvent in self._jsonData['events']:
            if not jEvent['title'] in scIdsByTitle:
                continue

            scId = scIdsByTitle[jEvent['title']]

            if (
                jEvent['rangeValues'][0]['position']['timestamp']
                >= self.DATE_LIMIT
            ):
                jEvent['rangeValues'][0]['span'] = (
                    self._w_get_span(self.novel.sections[scId])
                )
                jEvent['rangeValues'][0]['position']['timestamp'] = (
                    self._w_get_timestamp(self.novel.sections[scId])
                )

            if self._propertyMoonphaseGuid is not None:
                eventMoonphase = self._nvSvc.get_moon_phase_str(
                    self.novel.sections[scId].date
                )
            else:
                eventMoonphase = ''

            hasMoonphase = False
            for evtVal in jEvent['values']:

                if evtVal['property'] == self._propertyDescGuid:
                    if self.novel.sections[scId].desc:
                        evtVal['value'] = self.novel.sections[scId].desc

                elif evtVal['property'] == self._propertyNotesGuid:
                    if self.novel.sections[scId].notes:
                        evtVal['value'] = self.novel.sections[scId].notes

                elif evtVal['property'] == self._propertyMoonphaseGuid:
                        evtVal['value'] = eventMoonphase
                        hasMoonphase = True

            if not hasMoonphase and self._propertyMoonphaseGuid is not None:
                jEvent['values'].append(
                    {
                        'property': self._propertyMoonphaseGuid,
                        'value': eventMoonphase
                    }
                )

            if self.novel.sections[scId].tags:
                jEvent['tags'] = self.novel.sections[scId].tags


            newRel = []
            for evtRel in jEvent['relationships']:
                if evtRel['role'] == self._roleCharacterGuid:
                    continue

                elif evtRel['role'] == self._roleLocationGuid:
                    continue

                elif evtRel['role'] == self._roleItemGuid:
                    continue

                elif evtRel['role'] == self._roleArcGuid:
                    continue

                else:
                    newRel.append(evtRel)

            if self.novel.sections[scId].characters:
                for crId in self.novel.sections[scId].characters:
                    newRel.append(
                        {
                        'entity': self._characterGuidsById[crId],
                        'percentAllocated': 1,
                        'role': self._roleCharacterGuid,
                        })

            if self.novel.sections[scId].locations:
                for lcId in self.novel.sections[scId].locations:
                    newRel.append(
                        {
                        'entity': self._locationGuidsById[lcId],
                        'percentAllocated': 1,
                        'role': self._roleLocationGuid,
                        })

            if self.novel.sections[scId].items:
                for itId in self.novel.sections[scId].items:
                    newRel.append(
                        {
                        'entity': self._itemGuidsById[itId],
                        'percentAllocated': 1,
                        'role': self._roleItemGuid,
                        })

            if self.novel.sections[scId].scType == 0:
                newRel.append(
                    {
                    'entity': self._entityNarrativeGuid,
                    'percentAllocated': 1,
                    'role': self._roleArcGuid,
                    })

                if self.novel.sections[scId].scPlotLines:
                    for acId in self.novel.sections[scId].scPlotLines:
                        newRel.append(
                            {
                            'entity': self._arcGuidsById[acId],
                            'percentAllocated': 1,
                            'role': self._rolePlotlineGuid,
                            })

            jEvent['relationships'] = newRel

    def _w_update_items_from_source(self, source, itIdsByTitle, linkedItems):
        itmCount = len(self.novel.items)
        itIdsBySrcId = {}
        for srcItId in source.items:
            if source.items[srcItId].title in itIdsByTitle:
                itIdsBySrcId[srcItId] = (
                    itIdsByTitle[source.items[srcItId].title]
                )
            elif srcItId in linkedItems:

                itId = new_id(self.novel.items, prefix=ITEM_PREFIX)
                itIdsBySrcId[srcItId] = itId
                self.novel.items[itId] = source.items[srcItId]
                newGuid = self._guidGen.get_guid(
                    f'{itId}{self.novel.items[itId].title}'
                )
                self._itemGuidsById[itId] = newGuid
                self._jsonData['entities'].append({
                        'entityType':self._typeItemGuid,
                        'guid':newGuid,
                        'icon':'cube',
                        'name':self.novel.items[itId].title,
                        'notes':'',
                        'sortOrder':itmCount,
                        'swatchColor':'denim'})
                itmCount += 1
        return itIdsBySrcId

    def _w_update_locations_from_source(
            self,
            source,
            lcIdsByTitle,
            linkedLocations
    ):
        locCount = len(self.novel.locations)
        lcIdsBySrcId = {}
        for srcLcId in source.locations:
            if source.locations[srcLcId].title in lcIdsByTitle:
                lcIdsBySrcId[srcLcId] = (
                    lcIdsByTitle[source.locations[srcLcId].title]
                )
            elif srcLcId in linkedLocations:

                lcId = new_id(self.novel.locations, prefix=LOCATION_PREFIX)
                lcIdsBySrcId[srcLcId] = lcId
                self.novel.locations[lcId] = source.locations[srcLcId]
                newGuid = self._guidGen.get_guid(
                    f'{lcId}{self.novel.locations[lcId].title}'
                )
                self._locationGuidsById[lcId] = newGuid
                self._jsonData['entities'].append({
                        'entityType':self._typeLocationGuid,
                        'guid':newGuid,
                        'icon':'map',
                        'name':self.novel.locations[lcId].title,
                        'notes':'',
                        'sortOrder':locCount,
                        'swatchColor':'orange'})
                locCount += 1

        return lcIdsBySrcId

    def _w_update_sections_from_source(
            self,
            source,
            scIdsByTitle,
            crIdsBySrcId,
            lcIdsBySrcId,
            itIdsBySrcId,
            acIdsBySrcId
    ):
        for srcId in source.sections:
            if source.sections[srcId].scType != 0:
                if source.sections[srcId].title in scIdsByTitle:
                    scId = scIdsByTitle[source.sections[srcId].title]
                    self.novel.sections[scId].scType = 1
                continue

            if source.sections[srcId].title in scIdsByTitle:
                scId = scIdsByTitle[source.sections[srcId].title]
            else:
                scId = new_id(self.novel.sections, prefix=SECTION_PREFIX)
                self.novel.sections[scId] = self._nvSvc.new_section(
                    title=source.sections[srcId].title,
                    scType=source.sections[srcId].scType,
                    scene=source.sections[srcId].scene
                    )
                scIdsByTitle[self.novel.sections[scId].title] = scId
                newEvent = self._w_get_new_json_event(self.novel.sections[scId])
                self._jsonData['events'].append(newEvent)
            self.novel.sections[scId].status = source.sections[srcId].status

            if source.sections[srcId].scType is not None:
                self.novel.sections[scId].scType = source.sections[srcId].scType

            if source.sections[srcId].tags is not None:
                self.novel.sections[scId].tags = source.sections[srcId].tags

            if source.sections[srcId].desc is not None:
                self.novel.sections[scId].desc = source.sections[srcId].desc

            if source.sections[srcId].characters is not None:
                scCharacters = []
                for crId in source.sections[srcId].characters:
                    if crId in crIdsBySrcId:
                        scCharacters.append(crIdsBySrcId[crId])
                self.novel.sections[scId].characters = scCharacters

            if source.sections[srcId].locations is not None:
                scLocations = []
                for lcId in source.sections[srcId].locations:
                    if lcId in lcIdsBySrcId:
                        scLocations.append(lcIdsBySrcId[lcId])
                self.novel.sections[scId].locations = scLocations

            if source.sections[srcId].items is not None:
                scItems = []
                for itId in source.sections[srcId].items:
                    if itId in itIdsBySrcId:
                        scItems.append(itIdsBySrcId[itId])
                self.novel.sections[scId].items = scItems

            if source.sections[srcId].scPlotLines is not None:
                scArcs = []
                for acId in source.sections[srcId].scPlotLines:
                    if acId in acIdsBySrcId:
                        scArcs.append(acIdsBySrcId[acId])
                self.novel.sections[scId].scPlotLines = scArcs

            if source.sections[srcId].time is not None:
                self.novel.sections[scId].time = source.sections[srcId].time

            if source.sections[srcId].day is not None:
                dayInt = int(source.sections[srcId].day)
                sectionDelta = timedelta(days=dayInt)
                self.novel.sections[scId].date = (
                    self.referenceDate
                    +sectionDelta
                ).isoformat().split('T')[0]
            elif source.sections[srcId].date is None:
                self.novel.sections[scId].date = (
                    self.referenceDate.isoformat().split('T')[0]
                )
            else:
                self.novel.sections[scId].date = source.sections[srcId].date

            if source.sections[srcId].lastsMinutes is None:
                self.novel.sections[scId].lastsMinutes = '0'
            else:
                self.novel.sections[scId].lastsMinutes = (
                    source.sections[srcId].lastsMinutes
                )
            if source.sections[srcId].lastsHours is None:
                self.novel.sections[scId].lastsHours = '0'
            else:
                self.novel.sections[scId].lastsHours = (
                    source.sections[srcId].lastsHours
                )
            if source.sections[srcId].lastsDays is None:
                self.novel.sections[scId].lastsDays = '0'
            else:
                self.novel.sections[scId].lastsDays = (
                    source.sections[srcId].lastsDays
                )


from configparser import ConfigParser

from abc import ABC, abstractmethod


class ConfigurationBase(ABC):

    def __init__(self, settings=None, options=None, filePath=None):
        self.settings = None
        self.options = None
        self.filePath = filePath
        self.strLabel = 'SETTINGS'
        self.boolLabel = 'OPTIONS'
        self.set(
            settings=settings,
            options=options,
        )

    @abstractmethod
    def read(self):
        pass

    def set(self, settings=None, options=None):
        self.settings = (settings or {}).copy()
        self.options = (options or {}).copy()

    @abstractmethod
    def write(self):
        pass



class Configuration(ConfigurationBase):

    def read(self, filePath=None):
        self.filePath = filePath or self.filePath

        config = ConfigParser()
        config.read(self.filePath, encoding='utf-8')
        if self.strLabel in config:
            section = config[self.strLabel]
            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)
        if self.boolLabel in config:
            section = config[self.boolLabel]
            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.getboolean(option, fallback)

    def write(self, filePath=None):
        self.filePath = self.filePath or filePath

        config = ConfigParser()
        if self.settings:
            config.add_section(self.strLabel)
            for settingId in self.settings:
                config.set(
                    self.strLabel,
                    settingId,
                    str(self.settings[settingId]),
                )
        if self.options:
            config.add_section(self.boolLabel)
            for settingId in self.options:
                if self.options[settingId]:
                    config.set(self.boolLabel, settingId, 'Yes')
                else:
                    config.set(self.boolLabel, settingId, 'No')
        with open(self.filePath, 'w', encoding='utf-8') as f:
            config.write(f)


class BasicElement:

    def __init__(
        self,
        on_element_change=None,
        title=None,
        desc=None,
        links=None,
        fields=None,
        color=None,
    ):
        self.on_element_change = on_element_change or self.do_nothing
        self._title = title
        self._desc = desc
        self._color = color
        self._links = links or {}
        self._fields = fields or {}

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._title != newVal:
            self._title = newVal
            self.on_element_change()

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._desc != newVal:
            self._desc = newVal
            self.on_element_change()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._color != newVal:
            self._color = newVal
            self.on_element_change()

    @property
    def links(self):
        try:
            return self._links.copy()
        except AttributeError:
            return None

    @links.setter
    def links(self, newVal):
        if newVal is not None:
            for elem in newVal:
                val = newVal[elem]
                if val is not None:
                    assert type(val) is str
        if self._links != newVal:
            self._links = newVal
            self.on_element_change()

    @property
    def fields(self):
        return self._fields.copy()

    @fields.setter
    def fields(self, newVal):
        if self._fields != newVal:
            self._fields = newVal
            self.on_element_change()

    def do_nothing(self):
        pass




class BasicElementNotes(BasicElement):

    def __init__(
        self,
        notes=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._notes = notes

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._notes != newVal:
            self._notes = newVal
            self.on_element_change()



class Chapter(BasicElementNotes):

    def __init__(
        self,
        chLevel=None,
        chType=None,
        noNumber=None,
        isTrash=None,
        hasEpigraph=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._chLevel = chLevel
        self._chType = chType
        self._noNumber = noNumber
        self._isTrash = isTrash
        self._hasEpigraph = hasEpigraph

    @property
    def chLevel(self):
        return self._chLevel

    @chLevel.setter
    def chLevel(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._chLevel != newVal:
            self._chLevel = newVal
            self.on_element_change()

    @property
    def chType(self):
        return self._chType

    @chType.setter
    def chType(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._chType != newVal:
            self._chType = newVal
            self.on_element_change()

    @property
    def noNumber(self):
        return self._noNumber

    @noNumber.setter
    def noNumber(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._noNumber != newVal:
            self._noNumber = newVal
            self.on_element_change()

    @property
    def isTrash(self):
        return self._isTrash

    @isTrash.setter
    def isTrash(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._isTrash != newVal:
            self._isTrash = newVal
            self.on_element_change()

    @property
    def hasEpigraph(self):
        return self._hasEpigraph

    @hasEpigraph.setter
    def hasEpigraph(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._hasEpigraph != newVal:
            self._hasEpigraph = newVal
            self.on_element_change()



class BasicElementTags(BasicElementNotes):

    def __init__(
        self,
        tags=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._tags = tags or []

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._tags != newVal:
            self._tags = newVal
            self.on_element_change()



class WorldElement(BasicElementTags):

    def __init__(
        self,
        aka=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._aka = aka

    @property
    def aka(self):
        return self._aka

    @aka.setter
    def aka(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._aka != newVal:
            self._aka = newVal
            self.on_element_change()



class Character(WorldElement):

    def __init__(
        self,
        bio=None,
        goals=None,
        fullName=None,
        isMajor=None,
        birthDate=None,
        deathDate=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._bio = bio
        self._goals = goals
        self._fullName = fullName
        self._isMajor = isMajor
        self._birthDate = birthDate
        self._deathDate = deathDate

    @property
    def bio(self):
        return self._bio

    @bio.setter
    def bio(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._bio != newVal:
            self._bio = newVal
            self.on_element_change()

    @property
    def goals(self):
        return self._goals

    @goals.setter
    def goals(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._goals != newVal:
            self._goals = newVal
            self.on_element_change()

    @property
    def fullName(self):
        return self._fullName

    @fullName.setter
    def fullName(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._fullName != newVal:
            self._fullName = newVal
            self.on_element_change()

    @property
    def isMajor(self):
        return self._isMajor

    @isMajor.setter
    def isMajor(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._isMajor != newVal:
            self._isMajor = newVal
            self.on_element_change()

    @property
    def birthDate(self):
        return self._birthDate

    @birthDate.setter
    def birthDate(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._birthDate != newVal:
            self._birthDate = newVal
            self.on_element_change()

    @property
    def deathDate(self):
        return self._deathDate

    @deathDate.setter
    def deathDate(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._deathDate != newVal:
            self._deathDate = newVal
            self.on_element_change()

import re

from calendar import isleap, day_name, month_name
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta



class PyCalendar:

    DATE_FORMAT = _("YYYY-MM-DD")
    TIME_FORMAT = _("hh:mm")
    WEEKDAYS = day_name
    MONTHS = month_name
    min = date.min.isoformat()
    max = date.max.isoformat()

    @classmethod
    def age(cls, nowIso, birthDateIso, deathDateIso):
        now = datetime.fromisoformat(nowIso)
        if deathDateIso:
            deathDate = datetime.fromisoformat(deathDateIso)
            if now > deathDate:
                yearsDead = cls._difference_in_years(deathDate, now)
                daysDead = cls._difference_in_days(deathDate, now)
                if birthDateIso:
                    birthDate = datetime.fromisoformat(birthDateIso)
                    yearsOld = cls._difference_in_years(birthDate, deathDate)
                else:
                    yearsOld = None
                return yearsOld, yearsDead, None, daysDead

        if birthDateIso:
            birthDate = datetime.fromisoformat(birthDateIso)
            yearsOld = cls._difference_in_years(birthDate, now)
            daysOld = cls._difference_in_days(birthDate, now)
        return yearsOld, None, daysOld, None

    @classmethod
    def dt_disp(cls, day, dateStr, timeIso):
        dt = []
        if day:
            dt.append(f'{_("Day")} {day}')
        if dateStr:
            dt.append(dateStr)
        if timeIso:
            dt.append(cls.time_disp(timeIso))
        return ' '.join(dt)

    @classmethod
    def duration(cls, startDateIso, startTimeIso, endDateIso, endTimeIso):
        StartDateTime = datetime.fromisoformat(
            f'{startDateIso}T{startTimeIso}'
        )
        endDateTime = datetime.fromisoformat(f'{endDateIso}T{endTimeIso}')
        durationTimedelta = endDateTime - StartDateTime
        lastsHours = durationTimedelta.seconds // 3600
        lastsMinutes = (durationTimedelta.seconds % 3600) // 60
        if durationTimedelta.days:
            daysStr = str(durationTimedelta.days)
        else:
            daysStr = None
        if lastsHours:
            hoursStr = str(lastsHours)
        else:
            hoursStr = None
        if lastsMinutes:
            minutesStr = str(lastsMinutes)
        else:
            minutesStr = None
        return daysStr, hoursStr, minutesStr

    @classmethod
    def duration_disp(cls, lastsDays, lastsHours, lastsMinutes):
        duration = []
        if lastsDays and lastsDays != '0':
            duration.append(f"{lastsDays}{_('d')}")
        if lastsHours and lastsHours != '0':
            duration.append(f"{lastsHours}{_('h')}")
        if lastsMinutes and lastsMinutes != '0':
            duration.append(f"{lastsMinutes}{_('min')}")
        return ' '.join(duration)

    @classmethod
    def get_duration_str(cls, section):
        return cls.duration_disp(
            section.lastsDays,
            section.lastsHours,
            section.lastsMinutes
        )

    @classmethod
    def get_end_date_time(cls, section):
        sectionStart = datetime.fromisoformat(
            f'{section.date} {section.time}'
        )
        sectionEnd = sectionStart + cls._get_duration(section)
        return sectionEnd.isoformat().split('T')

    @classmethod
    def get_end_day_time(cls, section):
        if section.day:
            dayInt = int(section.day)
        else:
            dayInt = 0
        virtualStartDate = (date.min + timedelta(days=dayInt)).isoformat()
        virtualSectionStart = datetime.fromisoformat(
            f'{virtualStartDate} {section.time}'
        )
        virtualSectionEnd = virtualSectionStart + cls._get_duration(section)
        virtualEndDate, endTime = virtualSectionEnd.isoformat().split('T')
        endDay = str((date.fromisoformat(virtualEndDate) - date.min).days)
        return (endDay, endTime)

    @classmethod
    def get_end_time(cls, section):
        virtualSectionStart = datetime.fromisoformat(
            f'{cls.min} {section.time}'
        )
        virtualSectionEnd = virtualSectionStart + cls._get_duration(section)
        return virtualSectionEnd.isoformat().split('T')[1]

    @classmethod
    def get_locale_date(cls, isoDate, localize):
        if localize:
            try:
                localeDateStr = cls.locale_date(isoDate)
            except:
                localeDateStr = ''
            return localeDateStr

        else:
            return isoDate

    @classmethod
    def get_timestamp(cls, section, refIso):
        if not section.time and not section.date and not section.day:
            return

        timeStr = section.time
        if not timeStr:
            timeStr = '00:00'
        if section.date:
            try:
                sectionStart = datetime.fromisoformat(
                    f'{section.date} {timeStr}'
                )
            except:
                return
        else:
            try:
                if section.day:
                    dayInt = int(section.day)
                else:
                    dayInt = 0
                startDate = (
                    date.fromisoformat(refIso) + timedelta(days=dayInt)
                ).isoformat()
                sectionStart = datetime.fromisoformat(f'{startDate} {timeStr}')
            except:
                return

        return int((sectionStart - datetime.min).total_seconds())

    @classmethod
    def h_m_s_str(cls, timeIso):
        return timeIso.split(':')

    @classmethod
    def locale_date(cls, dateIso):
        return date.fromisoformat(dateIso).strftime('%x')

    @classmethod
    def specific_date(cls, dayStr, refIso):
        refDate = date.fromisoformat(refIso)
        return date.isoformat(refDate + timedelta(days=int(dayStr)))

    @classmethod
    def time_disp(cls, timeIso):
        h, m, __ = cls.verified_time(timeIso).split(':')
        return f'{h}:{m}'

    @classmethod
    def unspecific_date(cls, dateIso, refIso):
        refDate = date.fromisoformat(refIso)
        return str((date.fromisoformat(dateIso) - refDate).days)

    @classmethod
    def verified_date(cls, dateIso):
        if dateIso is not None:
            date.fromisoformat(dateIso)
        return dateIso

    @classmethod
    def verified_time(cls, timeIso):
        if  timeIso is not None:
            time.fromisoformat(timeIso)
            while timeIso.count(':') < 2:
                timeIso = f'{timeIso}:00'
        return timeIso

    @classmethod
    def weekday(cls, dateIso):
        return date.fromisoformat(dateIso).weekday()

    @classmethod
    def weekday_str(cls, timestamp):
        return (datetime.min + timedelta(seconds=timestamp)).strftime('%A')

    @classmethod
    def y_m_d_str(cls, dateIso):
        return dateIso.split('-')

    @classmethod
    def _difference_in_years(cls, startDate, endDate):
        diffyears = endDate.year - startDate.year
        difference = endDate - startDate.replace(endDate.year)
        days_in_year = isleap(endDate.year) and 366 or 365
        years = diffyears + (
            difference.days + difference.seconds / 86400.0
            ) / days_in_year
        return int(years)

    @classmethod
    def _difference_in_days(cls, startDate, endDate):
        return (endDate - startDate).days

    @classmethod
    def _get_duration(cls, section):
        if section.lastsDays:
            lastsDays = int(section.lastsDays)
        else:
            lastsDays = 0
        if section.lastsHours:
            lastsSeconds = int(section.lastsHours) * 3600
        else:
            lastsSeconds = 0
        if section.lastsMinutes:
            lastsSeconds += int(section.lastsMinutes) * 60
        return timedelta(days=lastsDays, seconds=lastsSeconds)


LANGUAGE_TAG = re.compile(r'\<(p|span|h.) xml\:lang=\"(.*?)\".*?\>')


class Novel(BasicElement):

    def __init__(
        self,
        authorName=None,
        wordTarget=None,
        wordCountStart=None,
        languageCode=None,
        countryCode=None,
        renumberChapters=None,
        renumberParts=None,
        renumberWithinParts=None,
        romanChapterNumbers=None,
        romanPartNumbers=None,
        saveWordCount=None,
        workPhase=None,
        chapterHeadingPrefix=None,
        chapterHeadingSuffix=None,
        partHeadingPrefix=None,
        partHeadingSuffix=None,
        noSceneField1=None,
        noSceneField2=None,
        noSceneField3=None,
        otherSceneField1=None,
        otherSceneField2=None,
        otherSceneField3=None,
        crField1=None,
        crField2=None,
        referenceDate=None,
        tree=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._authorName = authorName
        self._wordTarget = wordTarget
        self._wordCountStart = wordCountStart
        self._languageCode = languageCode
        self._countryCode = countryCode
        self._renumberChapters = renumberChapters
        self._renumberParts = renumberParts
        self._renumberWithinParts = renumberWithinParts
        self._romanChapterNumbers = romanChapterNumbers
        self._romanPartNumbers = romanPartNumbers
        self._saveWordCount = saveWordCount
        self._workPhase = workPhase
        self._chapterHeadingPrefix = chapterHeadingPrefix
        self._chapterHeadingSuffix = chapterHeadingSuffix
        self._partHeadingPrefix = partHeadingPrefix
        self._partHeadingSuffix = partHeadingSuffix
        self._noSceneField1 = noSceneField1
        self._noSceneField2 = noSceneField2
        self._noSceneField3 = noSceneField3
        self._otherSceneField1 = otherSceneField1
        self._otherSceneField2 = otherSceneField2
        self._otherSceneField3 = otherSceneField3
        self._crField1 = crField1
        self._crField2 = crField2

        self.chapters = {}
        self.sections = {}
        self.plotPoints = {}
        self.languages = None
        self.plotLines = {}
        self.locations = {}
        self.items = {}
        self.characters = {}
        self.projectNotes = {}
        try:
            self.referenceWeekDay = PyCalendar.weekday(referenceDate)
            self._referenceDate = referenceDate
        except:
            self.referenceWeekDay = None
            self._referenceDate = None
        self.tree = tree
        self.elementsByPrefix = {
            CHAPTER_PREFIX: self.chapters,
            CHARACTER_PREFIX: self.characters,
            ITEM_PREFIX: self.items,
            LOCATION_PREFIX: self.locations,
            PLOT_LINE_PREFIX: self.plotLines,
            PLOT_POINT_PREFIX: self.plotPoints,
            PRJ_NOTE_PREFIX: self.projectNotes,
            SECTION_PREFIX: self.sections,
        }

    @property
    def authorName(self):
        return self._authorName

    @authorName.setter
    def authorName(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._authorName != newVal:
            self._authorName = newVal
            self.on_element_change()

    @property
    def wordTarget(self):
        return self._wordTarget

    @wordTarget.setter
    def wordTarget(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._wordTarget != newVal:
            self._wordTarget = newVal
            self.on_element_change()

    @property
    def wordCountStart(self):
        return self._wordCountStart

    @wordCountStart.setter
    def wordCountStart(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._wordCountStart != newVal:
            self._wordCountStart = newVal
            self.on_element_change()

    @property
    def languageCode(self):
        return self._languageCode

    @languageCode.setter
    def languageCode(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._languageCode != newVal:
            self._languageCode = newVal
            self.on_element_change()

    @property
    def countryCode(self):
        return self._countryCode

    @countryCode.setter
    def countryCode(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._countryCode != newVal:
            self._countryCode = newVal
            self.on_element_change()

    @property
    def renumberChapters(self):
        return self._renumberChapters

    @renumberChapters.setter
    def renumberChapters(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._renumberChapters != newVal:
            self._renumberChapters = newVal
            self.on_element_change()

    @property
    def renumberParts(self):
        return self._renumberParts

    @renumberParts.setter
    def renumberParts(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._renumberParts != newVal:
            self._renumberParts = newVal
            self.on_element_change()

    @property
    def renumberWithinParts(self):
        return self._renumberWithinParts

    @renumberWithinParts.setter
    def renumberWithinParts(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._renumberWithinParts != newVal:
            self._renumberWithinParts = newVal
            self.on_element_change()

    @property
    def romanChapterNumbers(self):
        return self._romanChapterNumbers

    @romanChapterNumbers.setter
    def romanChapterNumbers(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._romanChapterNumbers != newVal:
            self._romanChapterNumbers = newVal
            self.on_element_change()

    @property
    def romanPartNumbers(self):
        return self._romanPartNumbers

    @romanPartNumbers.setter
    def romanPartNumbers(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._romanPartNumbers != newVal:
            self._romanPartNumbers = newVal
            self.on_element_change()

    @property
    def saveWordCount(self):
        return self._saveWordCount

    @saveWordCount.setter
    def saveWordCount(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._saveWordCount != newVal:
            self._saveWordCount = newVal
            self.on_element_change()

    @property
    def workPhase(self):
        return self._workPhase

    @workPhase.setter
    def workPhase(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._workPhase != newVal:
            self._workPhase = newVal
            self.on_element_change()

    @property
    def chapterHeadingPrefix(self):
        return self._chapterHeadingPrefix

    @chapterHeadingPrefix.setter
    def chapterHeadingPrefix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._chapterHeadingPrefix != newVal:
            self._chapterHeadingPrefix = newVal
            self.on_element_change()

    @property
    def chapterHeadingSuffix(self):
        return self._chapterHeadingSuffix

    @chapterHeadingSuffix.setter
    def chapterHeadingSuffix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._chapterHeadingSuffix != newVal:
            self._chapterHeadingSuffix = newVal
            self.on_element_change()

    @property
    def partHeadingPrefix(self):
        return self._partHeadingPrefix

    @partHeadingPrefix.setter
    def partHeadingPrefix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._partHeadingPrefix != newVal:
            self._partHeadingPrefix = newVal
            self.on_element_change()

    @property
    def partHeadingSuffix(self):
        return self._partHeadingSuffix

    @partHeadingSuffix.setter
    def partHeadingSuffix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._partHeadingSuffix != newVal:
            self._partHeadingSuffix = newVal
            self.on_element_change()

    @property
    def noSceneField1(self):
        return self._noSceneField1

    @noSceneField1.setter
    def noSceneField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noSceneField1 != newVal:
            self._noSceneField1 = newVal
            self.on_element_change()

    @property
    def noSceneField2(self):
        return self._noSceneField2

    @noSceneField2.setter
    def noSceneField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noSceneField2 != newVal:
            self._noSceneField2 = newVal
            self.on_element_change()

    @property
    def noSceneField3(self):
        return self._noSceneField3

    @noSceneField3.setter
    def noSceneField3(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noSceneField3 != newVal:
            self._noSceneField3 = newVal
            self.on_element_change()

    @property
    def otherSceneField1(self):
        return self._otherSceneField1

    @otherSceneField1.setter
    def otherSceneField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherSceneField1 != newVal:
            self._otherSceneField1 = newVal
            self.on_element_change()

    @property
    def otherSceneField2(self):
        return self._otherSceneField2

    @otherSceneField2.setter
    def otherSceneField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherSceneField2 != newVal:
            self._otherSceneField2 = newVal
            self.on_element_change()

    @property
    def otherSceneField3(self):
        return self._otherSceneField3

    @otherSceneField3.setter
    def otherSceneField3(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherSceneField3 != newVal:
            self._otherSceneField3 = newVal
            self.on_element_change()

    @property
    def crField1(self):
        return self._crField1

    @crField1.setter
    def crField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._crField1 != newVal:
            self._crField1 = newVal
            self.on_element_change()

    @property
    def crField2(self):
        return self._crField2

    @crField2.setter
    def crField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._crField2 != newVal:
            self._crField2 = newVal
            self.on_element_change()

    @property
    def referenceDate(self):
        return self._referenceDate

    @referenceDate.setter
    def referenceDate(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._referenceDate != newVal:
            if not newVal:
                self._referenceDate = None
                self.referenceWeekDay = None
                self.on_element_change()
            else:
                try:
                    self.referenceWeekDay = PyCalendar.weekday(newVal)
                except:
                    pass
                else:
                    self._referenceDate = newVal
                    self.on_element_change()

    def check_locale(self):
        if not self._languageCode:
            try:
                sysLng, sysCtr = locale.getlocale()[0].split('_')
            except:
                sysLng, sysCtr = locale.getdefaultlocale()[0].split('_')
            self.languageCode = sysLng
            self.countryCode = sysCtr
            return

        if len(self._languageCode) != 2:
            self.languageCode = 'zxx'
            self.countryCode = None
            return

        if self._countryCode and len(self._countryCode) != 2:
            self.countryCode = None

    def get_languages(self):

        def languages(text):
            m = LANGUAGE_TAG.search(text)
            while m:
                text = text[m.span()[1]:]
                yield m.group(2)
                m = LANGUAGE_TAG.search(text)

        self.languages = []
        for scId in self.sections:
            text = self.sections[scId].sectionContent
            if text:
                for language in languages(text):
                    if not language in self.languages:
                        self.languages.append(language)

    def get_tags(self):
        tags = {}
        for elements in [
            self.sections,
            self.characters,
            self.locations,
            self.items,
        ]:
            for elemId in elements:
                for tag in elements[elemId].tags:
                    if not tag in tags:
                        tags[tag] = [elemId]
                    else:
                        tags[tag].append(elemId)
        return tags

    def update_plot_lines(self):
        for scId in self.sections:
            self.sections[scId].scPlotPoints = {}
            self.sections[scId].scPlotLines = []
            for plId in self.plotLines:
                if scId in self.plotLines[plId].sections:
                    self.sections[scId].scPlotLines.append(plId)
                    for ppId in self.tree.get_children(plId):
                        if self.plotPoints[ppId].sectionAssoc == scId:
                            self.sections[scId].scPlotPoints[ppId] = plId
                            break



class NvTree:

    def __init__(self):
        self.roots = {
            CH_ROOT:[],
            PL_ROOT:[],
            CR_ROOT:[],
            LC_ROOT:[],
            IT_ROOT:[],
            PN_ROOT:[],
        }
        self.srtSections = {}
        self.srtPlotPoints = {}

    def append(self, parent, iid):
        if parent in self.roots:
            self.roots[parent].append(iid)
            if parent == CH_ROOT:
                self.srtSections[iid] = []
            elif parent == PL_ROOT:
                self.srtPlotPoints[iid] = []
            return

        if parent.startswith(CHAPTER_PREFIX):
            if parent in self.srtSections:
                self.srtSections[parent].append(iid)
            else:
                self.srtSections[parent] = [iid]
            return

        if parent.startswith(PLOT_LINE_PREFIX):
            if parent in self.srtPlotPoints:
                self.srtPlotPoints[parent].append(iid)
            else:
                self.srtPlotPoints[parent] = [iid]

    def delete(self, *items):
        raise NotImplementedError

    def delete_children(self, parent):
        if parent in self.roots:
            self.roots[parent] = []
            if parent == CH_ROOT:
                self.srtSections.clear()
                return

            if parent == PL_ROOT:
                self.srtPlotPoints.clear()
            return

        if parent.startswith(CHAPTER_PREFIX):
            self.srtSections[parent] = []
            return

        if parent.startswith(PLOT_LINE_PREFIX):
            self.srtPlotPoints[parent] = []

    def get_children(self, item):
        if item in self.roots:
            return self.roots[item]

        if item.startswith(CHAPTER_PREFIX):
            return self.srtSections.get(item, [])

        if item.startswith(PLOT_LINE_PREFIX):
            return self.srtPlotPoints.get(item, [])

    def index(self, item):
        raise NotImplementedError

    def insert(self, parent, index, iid):
        if parent in self.roots:
            self.roots[parent].insert(index, iid)
            if parent == CH_ROOT:
                self.srtSections[iid] = []
            elif parent == PL_ROOT:
                self.srtPlotPoints[iid] = []
            return

        if parent.startswith(CHAPTER_PREFIX):
            if parent in self.srtSections:
                self.srtSections[parent].insert(index, iid)
            else:
                self.srtSections[parent] = [iid]
            return

        if parent.startswith(PLOT_LINE_PREFIX):
            if parent in self.srtPlotPoints:
                self.srtPlotPoints[parent].insert(index, iid)
            else:
                self.srtPlotPoints[parent] = [iid]

    def move(self, item, parent, index):
        raise NotImplementedError

    def next(self, item):
        raise NotImplementedError

    def parent(self, item):
        if item.startswith(PLOT_POINT_PREFIX):
            for plId, ppIds in self.srtPlotPoints.items():
                if item in ppIds:
                    return plId

        elif item.startswith(SECTION_PREFIX):
            for chId, scIds in self.srtSections.items():
                if item in scIds:
                    return chId

        elif item in self.roots:
            return ''

        else:
            for root in self.roots:
                if item in root:
                    return root

        raise KeyError

    def prev(self, item):
        raise NotImplementedError

    def reset(self):
        for item in self.roots:
            self.roots[item] = []
        self.srtSections.clear()
        self.srtPlotPoints.clear()

    def set_children(self, item, newchildren):
        if item in self.roots:
            self.roots[item] = newchildren[:]
            if item == CH_ROOT:
                self.srtSections.clear()
                return

            if item == PL_ROOT:
                self.srtPlotPoints.clear()
            return

        if item.startswith(CHAPTER_PREFIX):
            self.srtSections[item] = newchildren[:]
            return

        if item.startswith(PLOT_LINE_PREFIX):
            self.srtPlotPoints[item] = newchildren[:]



class PlotLine(BasicElementNotes):

    def __init__(
        self,
        shortName=None,
        sections=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self._shortName = shortName
        self._sections = sections or []

    @property
    def shortName(self):
        return self._shortName

    @shortName.setter
    def shortName(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._shortName != newVal:
            self._shortName = newVal
            self.on_element_change()

    @property
    def sections(self):
        try:
            return self._sections[:]
        except TypeError:
            return None

    @sections.setter
    def sections(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._sections != newVal:
            self._sections = newVal
            self.on_element_change()



class PlotPoint(BasicElementNotes):

    def __init__(
        self,
        sectionAssoc=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self._sectionAssoc = sectionAssoc

    @property
    def sectionAssoc(self):
        return self._sectionAssoc

    @sectionAssoc.setter
    def sectionAssoc(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._sectionAssoc != newVal:
            self._sectionAssoc = newVal
            self.on_element_change()




class WordCounter:

    IGNORE_PATTERN = re.compile(
        r'\<note\>.*?\<\/note\>|\<comment\>.*?\<\/comment\>|\<.+?\>'
    )

    SEPARATOR_PATTERN = re.compile(r'—|–|\<\/p\>')

    def get_word_count(self, text):
        text = text.replace('\n', '')
        text = self.SEPARATOR_PATTERN.sub(' ', text)
        text = self.IGNORE_PATTERN.sub('', text)
        return len(text.split())


class Section(BasicElementTags):

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'

    wordCounter = WordCounter()

    def __init__(
        self,
        scType=None,
        scene=None,
        status=None,
        appendToPrev=None,
        viewpoint=None,
        goal=None,
        conflict=None,
        outcome=None,
        plotlineNotes=None,
        scDate=None,
        scTime=None,
        day=None,
        lastsMinutes=None,
        lastsHours=None,
        lastsDays=None,
        characters=None,
        locations=None,
        items=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._sectionContent = None
        self.wordCount = 0
        self._hasComment = False

        self._scType = scType
        self._scene = scene
        self._status = status
        self._appendToPrev = appendToPrev
        self._goal = goal
        self._conflict = conflict
        self._outcome = outcome
        self._plotlineNotes = plotlineNotes or {}
        try:
            self._weekDay = PyCalendar.weekday(scDate)
            self._localeDate = PyCalendar.locale_date(scDate)
            self._date = scDate
        except:
            self._weekDay = None
            self._localeDate = None
            self._date = None
        self._time = scTime
        self._day = day
        self._lastsMinutes = lastsMinutes
        self._lastsHours = lastsHours
        self._lastsDays = lastsDays
        self._viewpoint = viewpoint
        self._characters = characters or []
        self._locations = locations or []
        self._items = items or []

        self.scPlotLines = []
        self.scPlotPoints = {}

    @property
    def sectionContent(self):
        return self._sectionContent

    @sectionContent.setter
    def sectionContent(self, text):
        if text is not None:
            assert type(text) is str
        if self._sectionContent != text:
            self._sectionContent = text
            if text is not None:
                self.wordCount = self.wordCounter.get_word_count(text)
                self._hasComment = '<comment>' in self._sectionContent
            else:
                self.wordCount = 0
                self._hasComment = False
            self.on_element_change()

    @property
    def hasComment(self):
        return self._hasComment

    @property
    def scType(self):
        return self._scType

    @scType.setter
    def scType(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._scType != newVal:
            self._scType = newVal
            self.on_element_change()

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._scene != newVal:
            self._scene = newVal
            self.on_element_change()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._status != newVal:
            self._status = newVal
            self.on_element_change()

    @property
    def appendToPrev(self):
        return self._appendToPrev

    @appendToPrev.setter
    def appendToPrev(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._appendToPrev != newVal:
            self._appendToPrev = newVal
            self.on_element_change()

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._goal != newVal:
            self._goal = newVal
            self.on_element_change()

    @property
    def conflict(self):
        return self._conflict

    @conflict.setter
    def conflict(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._conflict != newVal:
            self._conflict = newVal
            self.on_element_change()

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._outcome != newVal:
            self._outcome = newVal
            self.on_element_change()

    @property
    def plotlineNotes(self):
        try:
            return dict(self._plotlineNotes)
        except TypeError:
            return None

    @plotlineNotes.setter
    def plotlineNotes(self, newVal):
        if newVal is not None:
            for elem in newVal:
                val = newVal[elem]
                if val is not None:
                    assert type(val) is str
        if self._plotlineNotes != newVal:
            self._plotlineNotes = newVal
            self.on_element_change()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._date != newVal:
            if not newVal:
                self._date = None
                self._weekDay = None
                self._localeDate = None
                self.on_element_change()
                return

            try:
                self._weekDay = PyCalendar.weekday(newVal)
            except:
                return

            try:
                self._localeDate = PyCalendar.locale_date(newVal)
            except:
                self._localeDate = newVal
            self._date = newVal
            self.on_element_change()

    @property
    def weekDay(self):
        return self._weekDay

    @property
    def localeDate(self):
        return self._localeDate

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._time != newVal:
            self._time = newVal
            self.on_element_change()

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._day != newVal:
            self._day = newVal
            self.on_element_change()

    @property
    def lastsMinutes(self):
        return self._lastsMinutes

    @lastsMinutes.setter
    def lastsMinutes(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._lastsMinutes != newVal:
            self._lastsMinutes = newVal
            self.on_element_change()

    @property
    def lastsHours(self):
        return self._lastsHours

    @lastsHours.setter
    def lastsHours(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._lastsHours != newVal:
            self._lastsHours = newVal
            self.on_element_change()

    @property
    def lastsDays(self):
        return self._lastsDays

    @lastsDays.setter
    def lastsDays(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._lastsDays != newVal:
            self._lastsDays = newVal
            self.on_element_change()

    @property
    def viewpoint(self):
        return self._viewpoint

    @viewpoint.setter
    def viewpoint(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._viewpoint != newVal:
            self._viewpoint = newVal
            self.on_element_change()

    @property
    def characters(self):
        try:
            return self._characters[:]
        except TypeError:
            return None

    @characters.setter
    def characters(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._characters != newVal:
            self._characters = newVal
            self.on_element_change()

    @property
    def locations(self):
        try:
            return self._locations[:]
        except TypeError:
            return None

    @locations.setter
    def locations(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._locations != newVal:
            self._locations = newVal
            self.on_element_change()

    @property
    def items(self):
        try:
            return self._items[:]
        except TypeError:
            return None

    @items.setter
    def items(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._items != newVal:
            self._items = newVal
            self.on_element_change()

    def day_to_date(self, referenceDate):
        if self._date:
            return True

        try:
            self.date = PyCalendar.specific_date(self._day, referenceDate)
            self._day = None
            return True

        except:
            self.date = None
            return False

    def date_to_day(self, referenceDate):
        if self._day:
            return True

        try:
            self._day = PyCalendar.unspecific_date(self._date, referenceDate)
            self.date = None
            return True

        except:
            self._day = None
            return False

    def get_end_date_time(self):
        endDate = None
        endTime = None
        endDay = None
        if self.time:
            if self.date:
                try:
                    endDate, endTime = PyCalendar.get_end_date_time(self)
                except:
                    pass
            elif self.day:
                try:
                    endDay, endTime = PyCalendar.get_end_day_time(self)
                except:
                    pass
            else:
                endTime = PyCalendar.get_end_time(self)
        return endDate, endTime, endDay

from datetime import date

import xml.etree.ElementTree as ET


class BasicElementNovx:

    def import_data(self, element, xmlElement):
        element.title = self._get_element_text(xmlElement, 'Title')
        element.desc = self._xml_element_to_text(xmlElement.find('Desc'))
        element.color = xmlElement.get('color', None)
        element.links = self._get_link_dict(xmlElement)
        element.fields = self._get_fields(xmlElement)

    def export_data(self, element, xmlElement):
        if element.title:
            ET.SubElement(xmlElement, 'Title').text = element.title
        if element.desc:
            xmlElement.append(self._text_to_xml_element('Desc', element.desc))
        if element.color:
            xmlElement.set('color', element.color)
        for path in element.links:
            xmlLink = ET.SubElement(xmlElement, 'Link')
            ET.SubElement(xmlLink, 'Path').text = path
            if element.links[path]:
                ET.SubElement(xmlLink, 'FullPath').text = element.links[path]
        for tag in element.fields:
            xmlField = ET.SubElement(xmlElement, 'Field')
            xmlField.set('tag', tag)
            xmlField.text = element.fields[tag]

    def _get_element_text(self, xmlElement, tag, default=None):
        if xmlElement.find(tag) is not None:
            return xmlElement.find(tag).text
        else:
            return default

    def _get_fields(self, xmlElement):
        fields = {}
        for xmlField in xmlElement.iterfind('Field'):
            tag = xmlField.get('tag', None)
            if tag is not None:
                fields[tag] = xmlField.text
        return fields

    def _get_link_dict(self, xmlElement):
        links = {}
        for xmlLink in xmlElement.iterfind('Link'):
            xmlPath = xmlLink.find('Path')
            if xmlPath is not None:
                path = xmlPath.text
                xmlFullPath = xmlLink.find('FullPath')
                if xmlFullPath is not None:
                    fullPath = xmlFullPath.text
                else:
                    fullPath = None
            else:
                path = xmlLink.attrib.get('path', None)
                fullPath = xmlLink.attrib.get('fullPath', None)
            if path:
                links[path] = fullPath
        return links

    def _text_to_xml_element(self, tag, text):
        xmlElement = ET.Element(tag)
        if text:
            for line in text.split('\n'):
                ET.SubElement(xmlElement, 'p').text = line
        return xmlElement

    def _xml_element_to_text(self, xmlElement):
        lines = []
        if xmlElement is not None:
            for paragraph in xmlElement.iterfind('p'):
                lines.append(''.join(t for t in paragraph.itertext()))
        return '\n'.join(lines)




class BasicElementNotesNovx(BasicElementNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.notes = self._xml_element_to_text(xmlElement.find('Notes'))

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.notes:
            xmlElement.append(self._text_to_xml_element('Notes', element.notes))



class ChapterNovx(BasicElementNotesNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        typeStr = xmlElement.get('type', '0')
        if typeStr in ('0', '1'):
            element.chType = int(typeStr)
        else:
            element.chType = 1
        chLevel = xmlElement.get('level', '2')
        if chLevel in ('1', '2'):
            element.chLevel = int(chLevel)
        else:
            element.chLevel = 2
        element.isTrash = xmlElement.get('isTrash', None) == '1'
        element.noNumber = xmlElement.get('noNumber', None) == '1'
        element.hasEpigraph = xmlElement.get('hasEpigraph', None) == '1'

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.chType:
            xmlElement.set('type', str(element.chType))
        if element.chLevel == 1:
            xmlElement.set('level', '1')
        if element.isTrash:
            xmlElement.set('isTrash', '1')
        if element.noNumber:
            xmlElement.set('noNumber', '1')
        if element.hasEpigraph:
            xmlElement.set('hasEpigraph', '1')


class BasicElementTagsNovx(BasicElementNotesNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        tags = string_to_list(self._get_element_text(xmlElement, 'Tags'))
        strippedTags = []
        for tag in tags:
            strippedTags.append(tag.strip())
        element.tags = strippedTags

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        tagStr = list_to_string(element.tags)
        if tagStr:
            ET.SubElement(xmlElement, 'Tags').text = tagStr



class WorldElementNovx(BasicElementTagsNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.aka = self._get_element_text(xmlElement, 'Aka')

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.aka:
            ET.SubElement(xmlElement, 'Aka').text = element.aka



class CharacterNovx(WorldElementNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.isMajor = xmlElement.get('major', None) == '1'
        element.fullName = self._get_element_text(xmlElement, 'FullName')
        element.bio = self._xml_element_to_text(xmlElement.find('Bio'))
        element.goals = self._xml_element_to_text(xmlElement.find('Goals'))
        element.birthDate = PyCalendar.verified_date(
            self._get_element_text(xmlElement, 'BirthDate')
        )
        element.deathDate = PyCalendar.verified_date(
            self._get_element_text(xmlElement, 'DeathDate')
        )

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.isMajor:
            xmlElement.set('major', '1')
        if element.fullName:
            ET.SubElement(xmlElement, 'FullName').text = element.fullName
        if element.bio:
            xmlElement.append(self._text_to_xml_element('Bio', element.bio))
        if element.goals:
            xmlElement.append(self._text_to_xml_element('Goals', element.goals))
        if element.birthDate:
            ET.SubElement(xmlElement, 'BirthDate').text = element.birthDate
        if element.deathDate:
            ET.SubElement(xmlElement, 'DeathDate').text = element.deathDate



class NovelNovx(BasicElementNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.renumberChapters = xmlElement.get(
            'renumberChapters', None) == '1'
        element.renumberParts = xmlElement.get(
            'renumberParts', None) == '1'
        element.renumberWithinParts = xmlElement.get(
            'renumberWithinParts', None) == '1'
        element.romanChapterNumbers = xmlElement.get(
            'romanChapterNumbers', None) == '1'
        element.romanPartNumbers = xmlElement.get(
            'romanPartNumbers', None) == '1'
        element.saveWordCount = xmlElement.get(
            'saveWordCount', None) == '1'
        workPhase = xmlElement.get('workPhase', None)
        if workPhase in ('1', '2', '3', '4', '5'):
            element.workPhase = int(workPhase)
        else:
            element.workPhase = None

        element.authorName = self._get_element_text(xmlElement, 'Author')

        element.chapterHeadingPrefix = self._get_element_text(
            xmlElement,
            'ChapterHeadingPrefix'
        )
        element.chapterHeadingSuffix = self._get_element_text(
            xmlElement,
            'ChapterHeadingSuffix'
        )

        element.partHeadingPrefix = self._get_element_text(
            xmlElement,
            'PartHeadingPrefix'
        )
        element.partHeadingSuffix = self._get_element_text(
            xmlElement,
            'PartHeadingSuffix'
        )

        element.noSceneField1 = self._get_element_text(
            xmlElement,
            'CustomPlotProgress',
            default=element.noSceneField1,
        )
        element.noSceneField2 = self._get_element_text(
            xmlElement,
            'CustomCharacterization',
            default=element.noSceneField2,
        )
        element.noSceneField3 = self._get_element_text(
            xmlElement,
            'CustomWorldBuilding',
            default=element.noSceneField3,
        )

        element.otherSceneField1 = self._get_element_text(
            xmlElement,
            'CustomGoal',
            default=element.otherSceneField1,
        )
        element.otherSceneField2 = self._get_element_text(
            xmlElement,
            'CustomConflict',
            default=element.otherSceneField2,
        )
        element.otherSceneField3 = self._get_element_text(
            xmlElement,
            'CustomOutcome',
            default=element.otherSceneField3,
        )

        element.crField1 = self._get_element_text(
            xmlElement,
            'CustomChrBio',
            default=element.crField1,
        )
        element.crField2 = self._get_element_text(
            xmlElement,
            'CustomChrGoals',
            default=element.crField2,
        )

        if xmlElement.find('WordCountStart') is not None:
            element.wordCountStart = int(
                xmlElement.find('WordCountStart').text
            )
        else:
            element.wordCountStart = 0
        if xmlElement.find('WordTarget') is not None:
            element.wordTarget = int(
                xmlElement.find('WordTarget').text
            )

        element.referenceDate = PyCalendar.verified_date(
            self._get_element_text(xmlElement, 'ReferenceDate')
        )

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.renumberChapters:
            xmlElement.set('renumberChapters', '1')
        if element.renumberParts:
            xmlElement.set('renumberParts', '1')
        if element.renumberWithinParts:
            xmlElement.set('renumberWithinParts', '1')
        if element.romanChapterNumbers:
            xmlElement.set('romanChapterNumbers', '1')
        if element.romanPartNumbers:
            xmlElement.set('romanPartNumbers', '1')
        if element.saveWordCount:
            xmlElement.set('saveWordCount', '1')
        if element.workPhase is not None:
            xmlElement.set('workPhase', str(element.workPhase))

        if element.authorName:
            ET.SubElement(
                xmlElement,
                'Author',
            ).text = element.authorName

        if element.chapterHeadingPrefix:
            ET.SubElement(
                xmlElement,
                'ChapterHeadingPrefix',
            ).text = element.chapterHeadingPrefix
        if element.chapterHeadingSuffix:
            ET.SubElement(
                xmlElement,
                'ChapterHeadingSuffix',
            ).text = element.chapterHeadingSuffix

        if element.partHeadingPrefix:
            ET.SubElement(
                xmlElement,
                'PartHeadingPrefix',
            ).text = element.partHeadingPrefix
        if element.partHeadingSuffix:
            ET.SubElement(
                xmlElement,
                'PartHeadingSuffix',
            ).text = element.partHeadingSuffix

        if element.noSceneField1:
            ET.SubElement(
                xmlElement,
                'CustomPlotProgress',
            ).text = element.noSceneField1
        if element.noSceneField2:
            ET.SubElement(
                xmlElement,
                'CustomCharacterization',
            ).text = element.noSceneField2
        if element.noSceneField3:
            ET.SubElement(
                xmlElement,
                'CustomWorldBuilding',
            ).text = element.noSceneField3

        if element.otherSceneField1:
            ET.SubElement(
                xmlElement,
                'CustomGoal',
            ).text = element.otherSceneField1
        if element.otherSceneField2:
            ET.SubElement(
                xmlElement,
                'CustomConflict',
            ).text = element.otherSceneField2
        if element.otherSceneField3:
            ET.SubElement(
                xmlElement,
                'CustomOutcome',
            ).text = element.otherSceneField3

        if element.crField1:
            ET.SubElement(
                xmlElement,
                'CustomChrBio',
            ).text = element.crField1
        if element.crField2:
            ET.SubElement(
                xmlElement,
                'CustomChrGoals',
            ).text = element.crField2

        if element.wordCountStart:
            ET.SubElement(
                xmlElement,
                'WordCountStart',
            ).text = str(element.wordCountStart)
        if element.wordTarget:
            ET.SubElement(
                xmlElement,
                'WordTarget',
            ).text = str(element.wordTarget)

        if element.referenceDate:
            ET.SubElement(
                xmlElement,
                'ReferenceDate',
            ).text = element.referenceDate



class NovxOpener:

    @classmethod
    def get_xml_root(cls, filePath, majorVersion, minorVersion):
        try:
            xmlTree = ET.parse(filePath)
        except Exception as ex:
            normPath = norm_path(filePath)
            raise RuntimeError(
                f'{_("Cannot process file")}: "{normPath}" - {str(ex)}'
            )

        xmlRoot = xmlTree.getroot()
        if xmlRoot.tag != 'novx':
            msg = _("No valid xml root element found in file")
            raise RuntimeError(f'{msg}: "{norm_path(filePath)}".')

        fileMajorVersion, fileMinorVersion = cls._get_file_version(
            xmlRoot,
            filePath,
        )
        fileMajorVersion, fileMinorVersion = cls._upgrade_file_version(
            xmlRoot,
            fileMajorVersion,
            fileMinorVersion,
        )
        cls._check_version(
            fileMajorVersion,
            fileMinorVersion,
            filePath,
            majorVersion,
            minorVersion,
        )
        return xmlRoot

    @classmethod
    def _check_version(
            cls,
            fileMajorVersion,
            fileMinorVersion,
            filePath,
            majorVersion,
            minorVersion,
    ):
        if fileMajorVersion > majorVersion:
            msg = _('The project "{}" was created with a newer novelibre version.')
            raise RuntimeError(msg.format(norm_path(filePath)))

        if fileMajorVersion < majorVersion:
            msg = _('The project "{}" was created with an outdated novelibre version.')
            raise RuntimeError(msg.format(norm_path(filePath)))

        if fileMinorVersion > minorVersion:
            msg = _('The project "{}" was created with a newer novelibre version.')
            raise RuntimeError(msg.format(norm_path(filePath)))

    @classmethod
    def _upgrade_file_version(
            cls,
            xmlRoot,
            fileMajorVersion,
            fileMinorVersion,
    ):
        if fileMajorVersion == 1 and fileMinorVersion < 7:
            cls._upgrade_to_1_7(xmlRoot)
            fileMinorVersion = 7
        if fileMajorVersion == 1 and fileMinorVersion < 8:
            cls._upgrade_to_1_8(xmlRoot)
            fileMinorVersion = 8
        return fileMajorVersion, fileMinorVersion

    @classmethod
    def _get_file_version(cls, xmlRoot, filePath):
        try:
            (
                fileMajorVersionStr,
                fileMinorVersionStr
            ) = xmlRoot.attrib['version'].split('.')
            fileMajorVersion = int(fileMajorVersionStr)
            fileMinorVersion = int(fileMinorVersionStr)
        except (KeyError, ValueError):
            msg = _("No valid version found in file")
            raise RuntimeError(msg.format(norm_path(filePath)))

        return fileMajorVersion, fileMinorVersion

    @classmethod
    def _upgrade_to_1_7(cls, xmlRoot):
        for xmlSection in xmlRoot.iter('SECTION'):
            xmlCharacters = xmlSection.find('Characters')
            if xmlCharacters is not None:
                crIds = xmlCharacters.get('ids', None)
                if crIds is not None:
                    crId = crIds.split(' ')[0]
                    ET.SubElement(
                        xmlSection,
                        'Viewpoint',
                        attrib={'id':crId},
                    )

    @classmethod
    def _upgrade_to_1_8(cls, xmlRoot):
        allSections = []

        for xmlSection in xmlRoot.iter(tag='SECTION'):
            allSections.append(xmlSection.attrib['id'])

        xmlChapters = xmlRoot.find('CHAPTERS')
        if xmlChapters is None:
            return

        for xmlChapter in xmlChapters.iterfind('CHAPTER'):
            xmlEpigraph = xmlChapter.find('Epigraph')
            xmlEpigraphSrc = xmlChapter.find('EpigraphSrc')
            if xmlEpigraph is not None:
                xmlChapter.remove(xmlEpigraph)

                xmlChapter.set('hasEpigraph', '1')

                xmlNewSection = ET.Element('SECTION')

                newId = new_id(allSections, SECTION_PREFIX)
                allSections.append(newId)
                xmlNewSection.set('id', newId)

                ET.SubElement(xmlNewSection, 'Title').text = _('Epigraph')

                xmlNewSection.append(xmlEpigraph)
                xmlEpigraph.tag = 'Content'

                if xmlEpigraphSrc is not None:
                    xmlChapter.remove(xmlEpigraphSrc)
                    xmlNewSection.append(
                        ET.fromstring(
                           f'<Desc><p>{xmlEpigraphSrc.text}</p></Desc>'
                        )
                    )

                xmlChapter.insert(0, xmlNewSection)



class PlotLineNovx(BasicElementNotesNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.shortName = self._get_element_text(xmlElement, 'ShortName')
        plSections = []
        xmlSections = xmlElement.find('Sections')
        if xmlSections is not None:
            scIds = xmlSections.get('ids', None)
            if scIds is not None:
                for scId in string_to_list(scIds, divider=' '):
                    plSections.append(scId)
        element.sections = plSections

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.shortName:
            ET.SubElement(xmlElement, 'ShortName').text = element.shortName
        if element.sections:
            attrib = {'ids':' '.join(element.sections)}
            ET.SubElement(xmlElement, 'Sections', attrib=attrib)


class PlotPointNovx(BasicElementNotesNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        xmlSectionAssoc = xmlElement.find('Section')
        if xmlSectionAssoc is not None:
            element.sectionAssoc = xmlSectionAssoc.get('id', None)

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.sectionAssoc:
            ET.SubElement(
                xmlElement,
                'Section',
                attrib={'id': element.sectionAssoc},
            )



class SectionNovx(BasicElementTagsNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)

        typeStr = xmlElement.get('type', '0')
        if typeStr in ('0', '1', '2', '3'):
            element.scType = int(typeStr)
        else:
            element.scType = 1
        status = xmlElement.get('status', '1')
        if status in ('1', '2', '3', '4', '5'):
            element.status = int(status)
        else:
            element.status = 1
        scene = xmlElement.get('scene', '0')
        if scene in ('0', '1', '2', '3'):
            element.scene = int(scene)
        else:
            element.scene = 0

        if not element.scene:
            sceneKind = xmlElement.get('pacing', None)
            if sceneKind in ('1', '2'):
                element.scene = int(sceneKind) + 1

        element.appendToPrev = xmlElement.get('append', None) == '1'

        xmlViewpoint = xmlElement.find('Viewpoint')
        if xmlViewpoint is not None:
            element.viewpoint = xmlViewpoint.get('id', None)

        element.goal = self._xml_element_to_text(xmlElement.find('Goal'))
        element.conflict = self._xml_element_to_text(xmlElement.find('Conflict'))
        element.outcome = self._xml_element_to_text(xmlElement.find('Outcome'))

        xmlPlotlineNotes = xmlElement.find('PlotNotes')
        if xmlPlotlineNotes is None:
            xmlPlotlineNotes = xmlElement
        plotlineNotes = {}
        for xmlPlotlineNote in xmlPlotlineNotes.iterfind('PlotlineNotes'):
            plId = xmlPlotlineNote.get('id', None)
            plotlineNotes[plId] = self._xml_element_to_text(xmlPlotlineNote)
        element.plotlineNotes = plotlineNotes

        if xmlElement.find('Date') is not None:
            element.date = PyCalendar.verified_date(xmlElement.find('Date').text)
        elif xmlElement.find('Day') is not None:
            element.day = verified_int_string(xmlElement.find('Day').text)

        if xmlElement.find('Time') is not None:
            element.time = PyCalendar.verified_time(xmlElement.find('Time').text)

        element.lastsDays = verified_int_string(
            self._get_element_text(xmlElement, 'LastsDays')
        )
        element.lastsHours = verified_int_string(
            self._get_element_text(xmlElement, 'LastsHours')
        )
        element.lastsMinutes = verified_int_string(
            self._get_element_text(xmlElement, 'LastsMinutes')
        )

        def get_references(tag):
            scReferences = []
            xmlReferences = xmlElement.find(tag)
            if xmlReferences is not None:
                refIds = xmlReferences.get('ids', None)
                if refIds is not None:
                    for refId in string_to_list(refIds, divider=' '):
                        scReferences.append(refId)
            return scReferences

        element.characters = get_references('Characters')
        element.locations = get_references('Locations')
        element.items = get_references('Items')

        xmlContent = xmlElement.find('Content')
        if xmlContent is not None:
            xmlStr = ET.tostring(
                xmlContent,
                encoding='utf-8',
                short_empty_elements=False
                ).decode('utf-8')
            xmlStr = xmlStr.replace('<Content>', '').replace('</Content>', '')

            lines = xmlStr.split('\n')
            newlines = []
            for line in lines:
                newlines.append(line.strip())
            xmlStr = ''.join(newlines)
            if xmlStr:
                element.sectionContent = xmlStr
            else:
                element.sectionContent = '<p></p>'
        elif element.scType < 2:
            element.sectionContent = '<p></p>'

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.scType:
            xmlElement.set('type', str(element.scType))
        if element.status > 1:
            xmlElement.set('status', str(element.status))
        if element.scene > 0:
            xmlElement.set('scene', str(element.scene))
        if element.appendToPrev:
            xmlElement.set('append', '1')

        if element.viewpoint:
            ET.SubElement(
                xmlElement,
                'Viewpoint',
                attrib={'id':element.viewpoint},
            )

        if element.goal:
            xmlElement.append(
                self._text_to_xml_element('Goal', element.goal)
            )
        if element.conflict:
            xmlElement.append(
                self._text_to_xml_element('Conflict', element.conflict)
            )
        if element.outcome:
            xmlElement.append(
                self._text_to_xml_element('Outcome', element.outcome)
            )

        if element.plotlineNotes:
            for plId in element.plotlineNotes:
                if not plId in element.scPlotLines:
                    continue

                if not element.plotlineNotes[plId]:
                    continue

                xmlPlotlineNotes = self._text_to_xml_element(
                    'PlotlineNotes', element.plotlineNotes[plId]
                )
                xmlPlotlineNotes.set('id', plId)
                xmlElement.append(xmlPlotlineNotes)

        if element.date:
            ET.SubElement(xmlElement, 'Date').text = element.date
        elif element.day:
            ET.SubElement(xmlElement, 'Day').text = element.day
        if element.time:
            ET.SubElement(xmlElement, 'Time').text = element.time

        if element.lastsDays and element.lastsDays != '0':
            ET.SubElement(xmlElement, 'LastsDays').text = element.lastsDays
        if element.lastsHours and element.lastsHours != '0':
            ET.SubElement(xmlElement, 'LastsHours').text = element.lastsHours
        if element.lastsMinutes and element.lastsMinutes != '0':
            ET.SubElement(xmlElement, 'LastsMinutes').text = element.lastsMinutes

        if element.characters:
            ET.SubElement(
                xmlElement,
                'Characters',
                attrib={'ids':' '.join(element.characters)},
            )

        if element.locations:
            ET.SubElement(
                xmlElement,
                'Locations',
                attrib={'ids':' '.join(element.locations)},
            )

        if element.items:
            ET.SubElement(
                xmlElement,
                'Items',
                attrib={'ids':' '.join(element.items)},
            )

        sectionContent = element.sectionContent
        if sectionContent:
            if not sectionContent in ('<p></p>', '<p />'):
                xmlElement.append(
                    ET.fromstring(f'<Content>{sectionContent}</Content>')
                )


def strip_illegal_characters(text):
    return re.sub('[\x00-\x08|\x0b-\x0c|\x0e-\x1f]', '', text)



def indent(elem, level=0):
    PARAGRAPH_LEVEL = 5

    i = f'\n{level * "  "}'
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = f'{i}  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        if level < PARAGRAPH_LEVEL:
            for elem in elem:
                indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class NovxFile(File):
    DESCRIPTION = _('novelibre project')
    EXTENSION = '.novx'

    MAJOR_VERSION = 1
    MINOR_VERSION = 10

    XML_HEADER = (
        f'<?xml version="1.0" encoding="utf-8"?>\n'
        f'<!DOCTYPE novx SYSTEM "novx_{MAJOR_VERSION}_{MINOR_VERSION}.dtd">\n'
        '<?xml-stylesheet href="novx.css" type="text/css"?>\n'
    )

    fileOpener = NovxOpener

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath)
        self.xmlTree = None

        self.wcLog = {}

        self.wcLogUpdate = {}

        self.timestamp = None

        self.basicElementCnv = BasicElementNovx()
        self.chapterCnv = ChapterNovx()
        self.characterCnv = CharacterNovx()
        self.novelCnv = NovelNovx()
        self.plotLineCnv = PlotLineNovx()
        self.plotPointCnv = PlotPointNovx()
        self.sectionCnv = SectionNovx()
        self.worldElementCnv = WorldElementNovx()

    def adjust_section_types(self):
        partType = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chLevel == 1:
                partType = self.novel.chapters[chId].chType
            elif partType != 0 and not self.novel.chapters[chId].isTrash:
                self.novel.chapters[chId].chType = partType
            for scId in self.novel.tree.get_children(chId):
                if (self.novel.sections[scId].scType
                        < self.novel.chapters[chId].chType
                ):
                    self.novel.sections[scId].scType = (
                        self.novel.chapters[chId].chType
                    )

    def count_words(self):
        count = 0
        totalCount = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if not self.novel.chapters[chId].isTrash:
                for scId in self.novel.tree.get_children(chId):
                    if self.novel.sections[scId].scType < 2:
                        totalCount += self.novel.sections[scId].wordCount
                        if self.novel.sections[scId].scType == 0:
                            count += self.novel.sections[scId].wordCount
        return count, totalCount

    def read(self):

        xmlRoot = self.fileOpener.get_xml_root(
            self.filePath,
            self.MAJOR_VERSION,
            self.MINOR_VERSION,
        )
        try:
            locale = (
                xmlRoot.attrib['{http://www.w3.org/XML/1998/namespace}lang']
            )
        except KeyError:
            pass
        else:
            codes = locale.split('-')
            self.novel.languageCode = codes[0]
            try:
                self.novel.countryCode = codes[1]
            except IndexError:
                self.novel.countryCode = None
        self.novel.tree.reset()
        try:
            self._read_project_data(xmlRoot)
            self._read_locations(xmlRoot)
            self._read_items(xmlRoot)
            self._read_characters(xmlRoot)
            self._read_chapters_and_sections(xmlRoot)
            self._read_plot_lines_and_points(xmlRoot)
            self._read_project_notes(xmlRoot)
            self.adjust_section_types()
            self._read_word_count_log(xmlRoot)
        except Exception as ex:
            raise RuntimeError(f"{_('Corrupt project data')} ({str(ex)})")
        self._get_timestamp()
        self._keep_word_count()

    def write(self):
        self._update_word_count_log()
        self.adjust_section_types()
        self.novel.get_languages()

        if self.novel.countryCode:
            countryCode = f'-{self.novel.countryCode}'
        else:
            countryCode = ''
        attrib = {
            'version': f'{self.MAJOR_VERSION}.{self.MINOR_VERSION}',
            'xml:lang': f'{self.novel.languageCode}{countryCode}',
        }
        xmlRoot = ET.Element('novx', attrib=attrib)
        self._build_project(xmlRoot)
        self._build_chapters_and_sections(xmlRoot)
        self._build_characters(xmlRoot)
        self._build_locations(xmlRoot)
        self._build_items(xmlRoot)
        self._build_plot_lines_and_points(xmlRoot)
        self._build_project_notes(xmlRoot)
        self._build_word_count_log(xmlRoot)

        indent(xmlRoot)

        self.xmlTree = ET.ElementTree(xmlRoot)
        self._write_element_tree(self)
        self._postprocess_xml_file(self.filePath)
        self._get_timestamp()

    def _build_project(self, root):
        xmlProject = ET.SubElement(root, 'PROJECT')
        self.novelCnv.export_data(self.novel, xmlProject)

    def _build_chapters_and_sections(self, root):
        xmlChapters = ET.SubElement(root, 'CHAPTERS')
        for chId in self.novel.tree.get_children(CH_ROOT):
            xmlChapter = ET.SubElement(
                xmlChapters, 'CHAPTER', attrib={'id': chId})
            self.chapterCnv.export_data(self.novel.chapters[chId], xmlChapter)
            for scId in self.novel.tree.get_children(chId):
                self.sectionCnv.export_data(
                    self.novel.sections[scId],
                    ET.SubElement(
                        xmlChapter,
                        'SECTION',
                        attrib={'id': scId},
                    )
                )

    def _build_characters(self, root):
        xmlCharacters = ET.SubElement(root, 'CHARACTERS')
        for crId in self.novel.tree.get_children(CR_ROOT):
            self.characterCnv.export_data(
                self.novel.characters[crId],
                ET.SubElement(
                    xmlCharacters,
                    'CHARACTER',
                    attrib={'id': crId},
                )
            )

    def _build_locations(self, root):
        xmlLocations = ET.SubElement(root, 'LOCATIONS')
        for lcId in self.novel.tree.get_children(LC_ROOT):
            self.worldElementCnv.export_data(
                self.novel.locations[lcId],
                ET.SubElement(
                    xmlLocations,
                    'LOCATION',
                    attrib={'id': lcId},
                )
            )

    def _build_items(self, root):
        xmlItems = ET.SubElement(root, 'ITEMS')
        for itId in self.novel.tree.get_children(IT_ROOT):
            self.worldElementCnv.export_data(
                self.novel.items[itId],
                ET.SubElement(
                    xmlItems,
                    'ITEM',
                    attrib={'id': itId},
                )
            )

    def _build_plot_lines_and_points(self, root):
        xmlPlotLines = ET.SubElement(root, 'ARCS')
        for plId in self.novel.tree.get_children(PL_ROOT):
            xmlPlotLine = ET.SubElement(
                xmlPlotLines,
                'ARC',
                attrib={'id': plId},
            )
            self.plotLineCnv.export_data(self.novel.plotLines[plId], xmlPlotLine)
            for ppId in self.novel.tree.get_children(plId):
                self.plotPointCnv.export_data(
                    self.novel.plotPoints[ppId],
                    ET.SubElement(
                        xmlPlotLine,
                        'POINT',
                        attrib={'id': ppId},
                    )
                )

    def _build_project_notes(self, root):
        xmlProjectNotes = ET.SubElement(root, 'PROJECTNOTES')
        for pnId in self.novel.tree.get_children(PN_ROOT):
            self.basicElementCnv.export_data(
                self.novel.projectNotes[pnId],
                ET.SubElement(
                    xmlProjectNotes,
                    'PROJECTNOTE',
                    attrib={'id': pnId},
                )
            )

    def _build_word_count_log(self, root):
        if not self.wcLog:
            return

        xmlWcLog = ET.SubElement(root, 'PROGRESS')
        wcLastCount = None
        wcLastTotalCount = None
        for wc in self.wcLog:
            wcCount, wcTotalCount = self.wcLog[wc]
            if self.novel.saveWordCount:
                if (
                    wcCount == wcLastCount
                    and wcTotalCount == wcLastTotalCount
                ):
                    continue

                wcLastCount = wcCount
                wcLastTotalCount = wcTotalCount
            xmlWc = ET.SubElement(xmlWcLog, 'WC')
            ET.SubElement(xmlWc, 'Date').text = wc
            ET.SubElement(xmlWc, 'Count').text = str(wcCount)
            ET.SubElement(xmlWc, 'WithUnused').text = str(wcTotalCount)

    def _check_id(self, elemId, elemPrefix):
        if not elemId.startswith(elemPrefix):
            raise RuntimeError(f"bad ID: '{elemId}'")

    def _get_timestamp(self):
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except Exception:
            self.timestamp = None

    def _keep_word_count(self):

        if not self.wcLog:
            return

        actualCount, actualTotalCount = self.count_words()
        latestDate = list(self.wcLog)[-1]
        latestCount = self.wcLog[latestDate][0]
        latestTotalCount = self.wcLog[latestDate][1]
        if (
            actualCount != latestCount
            or actualTotalCount != latestTotalCount
        ):
            try:
                fileDateIso = date.fromtimestamp(self.timestamp).isoformat()
            except Exception:
                fileDateIso = date.today().isoformat()
            self.wcLogUpdate[fileDateIso] = [actualCount, actualTotalCount]

    def _postprocess_xml_file(self, filePath):

        with open(filePath, 'r', encoding='utf-8') as f:
            text = f.read()
            text = strip_illegal_characters(text)
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(f'{self.XML_HEADER}{text}')
        except Exception as ex:
            msg = _("Cannot write file")
            msg = f'{msg}: "{norm_path(filePath)}"'
            msg = f'{msg} - {str(ex)}'
            raise RuntimeError(msg)

    def _read_chapters_and_sections(self, root):
        xmlChapters = root.find('CHAPTERS')
        if xmlChapters is None:
            return

        for xmlChapter in xmlChapters.iterfind('CHAPTER'):
            chId = xmlChapter.attrib['id']
            self._check_id(chId, CHAPTER_PREFIX)
            self.novel.chapters[chId] = Chapter()
            self.chapterCnv.import_data(self.novel.chapters[chId], xmlChapter)
            self.novel.tree.append(CH_ROOT, chId)

            for xmlSection in xmlChapter.iterfind('SECTION'):
                scId = xmlSection.attrib['id']
                self._check_id(scId, SECTION_PREFIX)
                self._read_section(xmlSection, scId)
                self.novel.tree.append(chId, scId)

    def _read_characters(self, root):
        xmlCharacters = root.find('CHARACTERS')
        if xmlCharacters is None:
            return

        for xmlCharacter in xmlCharacters.iterfind('CHARACTER'):
            crId = xmlCharacter.attrib['id']
            self._check_id(crId, CHARACTER_PREFIX)
            self.novel.characters[crId] = Character()
            self.characterCnv.import_data(
                self.novel.characters[crId],
                xmlCharacter
            )
            self.novel.tree.append(CR_ROOT, crId)

    def _read_items(self, root):
        xmlItems = root.find('ITEMS')
        if xmlItems is None:
            return

        for xmlItem in xmlItems.iterfind('ITEM'):
            itId = xmlItem.attrib['id']
            self._check_id(itId, ITEM_PREFIX)
            self.novel.items[itId] = WorldElement()
            self.worldElementCnv.import_data(self.novel.items[itId], xmlItem)
            self.novel.tree.append(IT_ROOT, itId)

    def _read_locations(self, root):
        xmlLocations = root.find('LOCATIONS')
        if xmlLocations is None:
            return

        for xmlLocation in xmlLocations.iterfind('LOCATION'):
            lcId = xmlLocation.attrib['id']
            self._check_id(lcId, LOCATION_PREFIX)
            self.novel.locations[lcId] = WorldElement()
            self.worldElementCnv.import_data(
                self.novel.locations[lcId],
                xmlLocation
            )
            self.novel.tree.append(LC_ROOT, lcId)

    def _read_plot_lines_and_points(self, root):
        xmlPlotLines = root.find('ARCS')
        if xmlPlotLines is None:
            return

        for xmlPlotLine in xmlPlotLines.iterfind('ARC'):
            plId = xmlPlotLine.attrib['id']
            self._check_id(plId, PLOT_LINE_PREFIX)
            self.novel.plotLines[plId] = PlotLine()
            self.plotLineCnv.import_data(self.novel.plotLines[plId], xmlPlotLine)
            self.novel.tree.append(PL_ROOT, plId)

            self.novel.plotLines[plId].sections = intersection(
                self.novel.plotLines[plId].sections, self.novel.sections)

            for scId in self.novel.plotLines[plId].sections:
                self.novel.sections[scId].scPlotLines.append(plId)

            for xmlPlotPoint in xmlPlotLine.iterfind('POINT'):
                ppId = xmlPlotPoint.attrib['id']
                self._check_id(ppId, PLOT_POINT_PREFIX)
                self._read_plot_point(xmlPlotPoint, ppId, plId)
                self.novel.tree.append(plId, ppId)

    def _read_plot_point(self, xmlPlotPoint, ppId, plId):
        self.novel.plotPoints[ppId] = PlotPoint()
        self.plotPointCnv.import_data(self.novel.plotPoints[ppId], xmlPlotPoint)

        scId = self.novel.plotPoints[ppId].sectionAssoc
        if scId in self.novel.sections:
            self.novel.sections[scId].scPlotPoints[ppId] = plId
        else:
            self.novel.plotPoints[ppId].sectionAssoc = None

    def _read_project_data(self, root):
        xmlProject = root.find('PROJECT')
        if xmlProject is None:
            return

        self.novelCnv.import_data(self.novel, xmlProject)

    def _read_project_notes(self, root):
        xmlProjectNotes = root.find('PROJECTNOTES')
        if xmlProjectNotes is None:
            return

        for xmlProjectNote in xmlProjectNotes.iterfind('PROJECTNOTE'):
            pnId = xmlProjectNote.attrib['id']
            self._check_id(pnId, PRJ_NOTE_PREFIX)
            self.novel.projectNotes[pnId] = BasicElement()
            self.basicElementCnv.import_data(
                self.novel.projectNotes[pnId],
                xmlProjectNote
            )
            self.novel.tree.append(PN_ROOT, pnId)

    def _read_section(self, xmlSection, scId):
        self.novel.sections[scId] = Section()
        self.sectionCnv.import_data(self.novel.sections[scId], xmlSection)

        self.novel.sections[scId].characters = intersection(
            self.novel.sections[scId].characters, self.novel.characters)
        self.novel.sections[scId].locations = intersection(
            self.novel.sections[scId].locations, self.novel.locations)
        self.novel.sections[scId].items = intersection(
            self.novel.sections[scId].items, self.novel.items)

    def _read_word_count_log(self, xmlRoot):

        def verified_date(dateStr):
            if dateStr is not None:
                date.fromisoformat(dateStr)
            return dateStr

        xmlWclog = xmlRoot.find('PROGRESS')
        if xmlWclog is None:
            return

        for xmlWc in xmlWclog.iterfind('WC'):
            try:
                wcDate = verified_date(xmlWc.find('Date').text)
                self.wcLog[wcDate] = [
                    int(xmlWc.find('Count').text),
                    int(xmlWc.find('WithUnused').text)
                ]
            except:
                pass

    def _update_word_count_log(self):

        if self.novel.saveWordCount:
            newCount, newTotalCount = self.count_words()
            todayIso = date.today().isoformat()
            self.wcLogUpdate[todayIso] = [newCount, newTotalCount]
            for wcDate in self.wcLogUpdate:
                self.wcLog[wcDate] = self.wcLogUpdate[wcDate]
        self.wcLogUpdate.clear()

    def _write_element_tree(self, xmlProject):

        backedUp = False
        if os.path.isfile(xmlProject.filePath):
            try:
                os.replace(xmlProject.filePath, f'{xmlProject.filePath}.bak')
            except Exception as ex:
                raise RuntimeError(str(ex))
            else:
                backedUp = True
        try:
            xmlProject.xmlTree.write(
                xmlProject.filePath, xml_declaration=False, encoding='utf-8')
        except Exception as ex:
            if backedUp:
                os.replace(f'{xmlProject.filePath}.bak', xmlProject.filePath)
            msg = _("Cannot write file")
            msg = f'{msg}: "{norm_path(xmlProject.filePath)}"'
            msg = f'{msg} - {str(ex)}'
            raise RuntimeError(msg)



class ZippedNovxOpener(NovxOpener):

    NOVX_EXTENSIONS = [
        '.novx',
    ]
    ZIP_EXTENSIONS = [
        '.zip',
    ]

    @classmethod
    def get_xml_root(cls, filePath, majorVersion, minorVersion):
        __, extension = os.path.splitext(filePath)
        try:
            if not extension in cls.ZIP_EXTENSIONS:
                raise RuntimeError('File type is not supported')

            with zipfile.ZipFile(filePath, 'r') as z:
                fileNames = z.namelist()
                xmlRoot = None
                for fileName in fileNames:
                    __, extension = os.path.splitext(fileName)
                    if extension in cls.NOVX_EXTENSIONS:
                        with z.open(fileName, 'r') as f:
                            xmlStr = f.read()
                        xmlRoot = ET.fromstring(xmlStr)
                        break

                if xmlRoot is None:
                    raise RuntimeError('File type is not supported')

        except Exception as ex:
            normPath = norm_path(filePath)
            raise RuntimeError(
                f'{_("Cannot process file")}: "{normPath}" - {str(ex)}'
            )

        if xmlRoot.tag != 'novx':
            msg = _("No valid xml root element found in file")
            raise RuntimeError(f'{msg}: "{norm_path(filePath)}".')

        fileMajorVersion, fileMinorVersion = cls._get_file_version(
            xmlRoot,
            filePath,
        )
        fileMajorVersion, fileMinorVersion = cls._upgrade_file_version(
            xmlRoot,
            fileMajorVersion,
            fileMinorVersion,
        )
        cls._check_version(
            fileMajorVersion,
            fileMinorVersion,
            filePath,
            majorVersion,
            minorVersion,
        )
        return xmlRoot



class ZippedNovxFile(NovxFile):

    DESCRIPTION = _('Zipped novelibre project')
    EXTENSION = '.zip'

    fileOpener = ZippedNovxOpener

    def write(self):
        raise NotImplementedError
from pathlib import Path

prefs = {}
launchers = {}

HOME_URL = 'https://github.com/peter88213/novelibre/'
NEWS_URL = 'https://github.com/peter88213/novelibre/discussions/1?sort=new'

HOME_DIR = str(Path.home()).replace('\\', '/')
INSTALL_DIR = f'{HOME_DIR}/.novx'
PROGRAM_DIR = os.path.dirname(sys.argv[0])
if not PROGRAM_DIR:
    PROGRAM_DIR = '.'
USER_STYLES_DIR = f'{INSTALL_DIR}/styles'
USER_STYLES_XML = f'{USER_STYLES_DIR}/styles.xml'

NOT_ASSIGNED = ''


def to_string(text):
    return str(text or '')



class NovxService:

    def change_word_counter(self, wordCounter):
        Section.wordCounter = wordCounter

    def get_novx_dtd_version(self):
        return (
            NovxFile.MAJOR_VERSION,
            NovxFile.MINOR_VERSION
        )

    def get_novelibre_home_url(self):
        return HOME_URL

    def get_novx_file_extension(self):
        return NovxFile.EXTENSION

    def get_word_counter(self):
        return Section.wordCounter

    def get_zipped_novx_file_extension(self):
        return ZippedNovxFile.EXTENSION

    def new_basic_element(self, **kwargs):
        return BasicElement(**kwargs)

    def new_chapter(self, **kwargs):
        return Chapter(**kwargs)

    def new_character(self, **kwargs):
        return Character(**kwargs)

    def new_novel(self, **kwargs):
        kwargs['tree'] = kwargs.get('tree', NvTree())
        return Novel(**kwargs)

    def new_novx_file(self, filePath, **kwargs):
        return NovxFile(filePath, **kwargs)

    def new_nv_tree(self, **kwargs):
        return NvTree(**kwargs)

    def new_plot_line(self, **kwargs):
        return PlotLine(**kwargs)

    def new_plot_point(self, **kwargs):
        return PlotPoint(**kwargs)

    def new_section(self, **kwargs):
        return Section(**kwargs)

    def new_world_element(self, **kwargs):
        return WorldElement(**kwargs)

    def new_zipped_novx_file(self, filePath, **kwargs):
        return ZippedNovxFile(filePath, **kwargs)

import tkinter as tk


class TooltipBase:

    def __init__(self, anchor_widget):
        self.anchor_widget = anchor_widget
        self.tipwindow = None

    def __del__(self):
        self.hidetip()

    def showtip(self):
        if self.tipwindow:
            return
        self.tipwindow = tw = tk.Toplevel(self.anchor_widget)
        tw.wm_overrideredirect(1)
        try:
            tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass

        self.position_window()
        self.showcontents()
        self.tipwindow.update_idletasks()  # Needed on MacOS -- see #34275.
        self.tipwindow.lift()  # work around bug in Tk 8.5.18+ (issue #24570)

    def position_window(self):
        x, y = self.get_position()
        root_x = self.anchor_widget.winfo_rootx() + x
        root_y = self.anchor_widget.winfo_rooty() + y
        self.tipwindow.wm_geometry("+%d+%d" % (root_x, root_y))

    def get_position(self):
        return 20, self.anchor_widget.winfo_height() + 1

    def showcontents(self):
        raise NotImplementedError

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            try:
                tw.destroy()
            except tk.TclError:  # pragma: no cover
                pass


class OnHoverTooltipBase(TooltipBase):

    def __init__(self, anchor_widget, hover_delay=1000):
        super().__init__(anchor_widget)
        self.hover_delay = hover_delay

        self._after_id = None
        self._id1 = self.anchor_widget.bind("<Enter>", self._show_event)
        self._id2 = self.anchor_widget.bind("<Leave>", self._hide_event)
        self._id3 = self.anchor_widget.bind("<Button>", self._hide_event)

    def __del__(self):
        try:
            self.anchor_widget.unbind("<Enter>", self._id1)
            self.anchor_widget.unbind("<Leave>", self._id2)  # pragma: no cover
            self.anchor_widget.unbind("<Button>", self._id3)  # pragma: no cover
        except tk.TclError:
            pass
        super().__del__()

    def _show_event(self, event=None):
        if self.hover_delay:
            self.schedule()
        else:
            self.showtip()

    def _hide_event(self, event=None):
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self._after_id = self.anchor_widget.after(self.hover_delay,
                                                  self.showtip)

    def unschedule(self):
        after_id = self._after_id
        self._after_id = None
        if after_id:
            self.anchor_widget.after_cancel(after_id)

    def hidetip(self):
        try:
            self.unschedule()
        except tk.TclError:  # pragma: no cover
            pass
        super().hidetip()


class Hovertip(OnHoverTooltipBase):
    "A tooltip that pops up when a mouse hovers over an anchor widget."

    def __init__(self, anchor_widget, text, hover_delay=1000):
        super().__init__(anchor_widget, hover_delay=hover_delay)
        self.text = text

    def showcontents(self):
        label = tk.Label(self.tipwindow, text=self.text, justify='left',
                      background="#ffffe0", relief='solid', borderwidth=1)
        label.pack()

import math


class Moon:

    @classmethod
    def get_phase_day(cls, isoDate):
        try:
            y, m, d = isoDate.split('-')
            year = int(y)
            month = int(m)
            day = int(d)
            r = year % 100
            r %= 19
            if r > 9:
                r -= 19
            r = ((r * 11) % 30) + month + day
            if month < 3:
                r += 2
            if year < 2000:
                r -= 4
            else:
                r -= 8.3
            r = math.floor(r + 0.5) % 30
            if r < 0:
                r += 30
        except:
            r = None
        return r

    @classmethod
    def get_phase_string(cls, isoDate):
        moonViews = (
            '🌑🌑🌒🌒🌒🌒🌓🌓🌓🌓🌔🌔🌔🌔🌕'
            '🌕🌕🌖🌖🌖🌖🌗🌗🌗🌗🌘🌘🌘🌘🌑'
        )
        moonFractions = '00¼¼¼¼½½½½¾¾¾¾111¾¾¾¾½½½½¼¼¼¼0'
        moonPhaseDay = cls.get_phase_day(isoDate)
        if moonPhaseDay is not None:
            display = (
                f'{moonPhaseDay} '
                f'{moonViews[moonPhaseDay]} '
                f'{moonFractions[moonPhaseDay]}'
            )
        else:
            display = ''
        return display

from string import Template

from xml import sax
from xml.etree import ElementTree as ET

from datetime import datetime
from shutil import rmtree
from string import Template
import tempfile
from xml import sax

from string import Template



class Filter:

    def accept(self, source, eId):
        return True

    def get_message(self, source):
        return ''


class FileExport(File):
    SUFFIX = ''
    _DIVIDER = ', '
    _appendedSectionTemplate = ''
    _assocSectionTemplate = ''
    _chapterEndTemplate = ''
    _chapterTemplate = ''
    _characterHeadingTemplate = ''
    _characterTemplate = ''
    _epigraphTemplate = ''
    _fileFooter = ''
    _fileHeader = ''
    _firstSectionTemplate = ''
    _itemHeadingTemplate = ''
    _itemTemplate = ''
    _locationHeadingTemplate = ''
    _locationTemplate = ''
    _partTemplate = ''
    _partEndTemplate = ''
    _plotLineHeadingTemplate = ''
    _plotLineTemplate = ''
    _plotPointTemplate = ''
    _projectNoteTemplate = ''
    _sectionDivider = ''
    _sectionTemplate = ''
    _stage1Template = ''
    _stage2Template = ''
    _unusedChapterEndTemplate = ''
    _unusedChapterTemplate = ''
    _unusedSectionTemplate = ''
    localizeDate = False

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self.sectionFilter = Filter()
        self.chapterFilter = Filter()
        self.characterFilter = Filter()
        self.locationFilter = Filter()
        self.itemFilter = Filter()
        self.arcFilter = Filter()
        self.turningPointFilter = Filter()

    def write(self):
        text = self._get_text()
        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise RuntimeError(
                    f'{_("Cannot overwrite file")}: '
                    f'"{norm_path(self.filePath)}".'
                )
            else:
                backedUp = True
        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise RuntimeError(
                f'{_("Cannot write file")}: '
                f'"{norm_path(self.filePath)}".'
            )

    def _convert_from_novx(self, text, **kwargs):
        return(text or '')

    def _get_chapterMapping(self, chId, chapterNumber):
        if chapterNumber == 0:
            chapterNumber = ''

        chapterMapping = dict(
            ID=chId,
            ChapterNumber=chapterNumber,
            Title=self._convert_from_novx(
                self.novel.chapters[chId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.chapters[chId].desc
            ),
            Notes=self._convert_from_novx(
                self.novel.chapters[chId].notes
            ),
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True
            ),
            ProjectPath=self.projectPath,
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
            ManuscriptSuffix=MANUSCRIPT_SUFFIX,
        )
        return chapterMapping

    def _get_chapters(self):
        lines = []
        partNumber = 0
        chapterNumber = 0
        sectionNumber = 0
        wordsTotal = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            dispNumber = 0
            if not self.chapterFilter.accept(self, chId):
                continue

            template = None
            if self.novel.chapters[chId].chType == 1:
                if self._unusedChapterTemplate:
                    template = Template(self._unusedChapterTemplate)
            elif (
                self.novel.chapters[chId].chLevel == 1
                and self._partTemplate
            ):
                template = Template(self._partTemplate)
                partNumber += 1
                dispNumber = partNumber
            elif (
                self.novel.chapters[chId].chLevel == 2
                and self._chapterTemplate
            ):
                template = Template(self._chapterTemplate)
                chapterNumber += 1
                dispNumber = chapterNumber
            if template is not None:
                lines.append(
                    template.safe_substitute(
                        self._get_chapterMapping(chId, dispNumber)
                    )
                )

            (
                sectionLines,
                sectionNumber,
                wordsTotal,
            ) = self._get_sections(
                chId,
                sectionNumber,
                wordsTotal,
                self.novel.chapters[chId].hasEpigraph,
            )
            lines.extend(sectionLines)

            template = None
            if self.novel.chapters[chId].chType == 1:
                if self._unusedChapterEndTemplate:
                    template = Template(self._unusedChapterEndTemplate)
            elif (
                self.novel.chapters[chId].chLevel == 1
                and self._partEndTemplate
            ):
                template = Template(self._partEndTemplate)
            elif (
                self.novel.chapters[chId].chLevel == 2
                and self._chapterEndTemplate
            ):
                template = Template(self._chapterEndTemplate)
            if template is not None:
                lines.append(
                    template.safe_substitute(
                        self._get_chapterMapping(chId, dispNumber)
                    )
                )
        return lines

    def _get_characterMapping(self, crId):
        if self.novel.characters[crId].tags is not None:
            tags = list_to_string(
                self.novel.characters[crId].tags,
                divider=self._DIVIDER
            )
        else:
            tags = ''
        if self.novel.characters[crId].isMajor:
            characterStatus = MAJOR_MARKER
        else:
            characterStatus = MINOR_MARKER
        birthDateStr = self.novel.characters[crId].birthDate
        if birthDateStr is None:
            birthDateStr = ''
        deathDateStr = self.novel.characters[crId].deathDate
        if deathDateStr is None:
            deathDateStr = ''

        (
            __, __, __, __, __, __,
            crField1,
            crField2,
        ) = self._get_field_names()

        characterMapping = dict(
            ID=crId,
            Title=self._convert_from_novx(
                self.novel.characters[crId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.characters[crId].desc,
            ),
            Tags=self._convert_from_novx(tags),
            AKA=self._convert_from_novx(
                self.novel.characters[crId].aka,
                quick=True,
            ),
            Notes=self._convert_from_novx(
                self.novel.characters[crId].notes,
            ),
            Bio=self._convert_from_novx(
                self.novel.characters[crId].bio,
            ),
            Goals=self._convert_from_novx(
                self.novel.characters[crId].goals,
            ),
            FullName=self._convert_from_novx(
                self.novel.characters[crId].fullName,
                quick=True,
            ),
            Status=characterStatus,
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            ProjectPath=self.projectPath,
            CharactersSuffix=CHARACTERS_SUFFIX,
            BirthDate=birthDateStr,
            DeathDate=deathDateStr,
            CharacterField1=crField1,
            CharacterField2=crField2,

            CustomChrBio=crField1,
            CustomChrGoals=crField2,
        )
        return characterMapping

    def _get_characters(self):
        if self._characterHeadingTemplate:
            lines = [self._characterHeadingTemplate]
        else:
            lines = []
        template = Template(self._characterTemplate)
        for crId in self.novel.tree.get_children(CR_ROOT):
            if self.characterFilter.accept(self, crId):
                lines.append(
                    template.safe_substitute(
                        self._get_characterMapping(crId)
                    )
                )
        return lines

    def _get_field_names(self):
        if self.novel.noSceneField1:
            noSceneField1 = self.novel.noSceneField1
        else:
            noSceneField1 = f"{_('Field')} 1"
        if self.novel.noSceneField2:
            noSceneField2 = self.novel.noSceneField2
        else:
            noSceneField2 = f"{_('Field')} 2"
        if self.novel.noSceneField3:
            noSceneField3 = self.novel.noSceneField3
        else:
            noSceneField3 = f"{_('Field')} 3"
        if self.novel.otherSceneField1:
            otherSceneField1 = self.novel.otherSceneField1
        else:
            otherSceneField1 = f"{_('Field')} 1"
        if self.novel.otherSceneField2:
            otherSceneField2 = self.novel.otherSceneField2
        else:
            otherSceneField2 = f"{_('Field')} 2"
        if self.novel.otherSceneField3:
            otherSceneField3 = self.novel.otherSceneField3
        else:
            otherSceneField3 = f"{_('Field')} 3"
        if self.novel.crField1:
            crField1 = self.novel.crField1
        else:
            crField1 = f"{_('Field')} 1"
        if self.novel.crField2:
            crField2 = self.novel.crField2
        else:
            crField2 = f"{_('Field')} 2"
        return (
            noSceneField1,
            noSceneField2,
            noSceneField3,
            otherSceneField1,
            otherSceneField2,
            otherSceneField3,
            crField1,
            crField2,
        )

    def _get_fileFooter(self):
        lines = []
        template = Template(self._fileFooter)
        lines.append(template.safe_substitute(self._get_fileFooterMapping()))
        return lines

    def _get_fileFooterMapping(self):
        return []

    def _get_fileHeader(self):
        lines = []
        template = Template(self._fileHeader)
        lines.append(template.safe_substitute(self._get_fileHeaderMapping()))
        return lines

    def _get_fileHeaderMapping(self):
        filterMessages = []
        expFilters = [
            self.chapterFilter,
            self.sectionFilter,
            self.characterFilter,
            self.locationFilter,
            self.itemFilter,
            self.arcFilter,
            self.turningPointFilter,
        ]
        for expFilter in expFilters:
            message = expFilter.get_message(self)
            if message:
                filterMessages.append(message)
            if filterMessages:
                filters = self._convert_from_novx('\n'.join(filterMessages))
            else:
                filters = ''
            (
                noSceneField1,
                noSceneField2,
                noSceneField3,
                otherSceneField1,
                otherSceneField2,
                otherSceneField3,
                crField1,
                crField2,
            ) = self._get_field_names()

        fileHeaderMapping = dict(
            Title=self._convert_from_novx(
                self.novel.title,
                quick=True,
            ),
            Filters=filters,
            Desc=self._convert_from_novx(self.novel.desc),
            AuthorName=self._convert_from_novx(
                self.novel.authorName,
                quick=True,
            ),
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,

            NotASceneField1=noSceneField1,
            NotASceneField2=noSceneField2,
            NotASceneField3=noSceneField3,
            OtherSceneField1=otherSceneField1,
            OtherSceneField2=otherSceneField2,
            OtherSceneField3=otherSceneField3,
            CharacterField1=crField1,
            CharacterField2=crField2,

            CustomPlotProgress=noSceneField1,
            CustomCharacterization=noSceneField2,
            CustomWorldBuilding=noSceneField3,
            CustomGoal=otherSceneField1,
            CustomConflict=otherSceneField2,
            CustomOutcome=otherSceneField3,
            CustomChrBio=crField1,
            CustomChrGoals=crField2
        )
        return fileHeaderMapping

    def _get_itemMapping(self, itId):
        if self.novel.items[itId].tags is not None:
            tags = list_to_string(
                self.novel.items[itId].tags,
                divider=self._DIVIDER
            )
        else:
            tags = ''

        itemMapping = dict(
            ID=itId,
            Title=self._convert_from_novx(
                self.novel.items[itId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.items[itId].desc,
            ),
            Notes=self._convert_from_novx(
                self.novel.items[itId].notes,
            ),
            Tags=self._convert_from_novx(
                tags,
                quick=True,
            ),
            AKA=self._convert_from_novx(
                self.novel.items[itId].aka,
                quick=True,
            ),
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            ProjectPath=self.projectPath,
            ItemsSuffix=ITEMS_SUFFIX,
        )
        return itemMapping

    def _get_items(self):
        if self._itemHeadingTemplate:
            lines = [self._itemHeadingTemplate]
        else:
            lines = []
        template = Template(self._itemTemplate)
        for itId in self.novel.tree.get_children(IT_ROOT):
            if self.itemFilter.accept(self, itId):
                lines.append(
                    template.safe_substitute(
                        self._get_itemMapping(itId)
                    )
                )
        return lines

    def _get_locationMapping(self, lcId):
        if self.novel.locations[lcId].tags is not None:
            tags = list_to_string(
                self.novel.locations[lcId].tags,
                divider=self._DIVIDER
            )
        else:
            tags = ''

        locationMapping = dict(
            ID=lcId,
            Title=self._convert_from_novx(
                self.novel.locations[lcId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.locations[lcId].desc,
            ),
            Notes=self._convert_from_novx(
                self.novel.locations[lcId].notes
            ),
            Tags=self._convert_from_novx(
                tags,
                quick=True,
            ),
            AKA=self._convert_from_novx(
                self.novel.locations[lcId].aka,
                quick=True,
            ),
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            ProjectPath=self.projectPath,
            LocationsSuffix=LOCATIONS_SUFFIX,
        )
        return locationMapping

    def _get_locations(self):
        if self._locationHeadingTemplate:
            lines = [self._locationHeadingTemplate]
        else:
            lines = []
        template = Template(self._locationTemplate)
        for lcId in self.novel.tree.get_children(LC_ROOT):
            if self.locationFilter.accept(self, lcId):
                lines.append(
                    template.safe_substitute(
                        self._get_locationMapping(lcId)
                    )
                )
        return lines

    def _get_plotLineMapping(self, plId):
        plotlineMapping = dict(
            ID=plId,
            Title=self._convert_from_novx(
                self.novel.plotLines[plId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.plotLines[plId].desc,
            ),
            Notes=self._convert_from_novx(
                self.novel.plotLines[plId].notes,
            ),
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            ProjectPath=self.projectPath,
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
        )
        return plotlineMapping

    def _get_plotlines(self):
        if self._plotLineHeadingTemplate:
            lines = [self._plotLineHeadingTemplate]
        else:
            lines = []
        for plId in self.novel.tree.get_children(PL_ROOT):
            if self.arcFilter.accept(self, plId):
                if self._plotLineTemplate:
                    template = Template(self._plotLineTemplate)
                    lines.append(
                        template.safe_substitute(
                            self._get_plotLineMapping(plId)
                        )
                    )

            for ppId in self.novel.tree.get_children(plId):
                if self._plotPointTemplate:
                    template = Template(self._plotPointTemplate)
                    plotPointMapping = self._get_plotPointMapping(ppId)
                    lines.append(
                        template.safe_substitute(
                            plotPointMapping
                        )
                    )
        return lines

    def _get_plotPointMapping(self, ppId):
        plotPointMapping = dict(
            ID=ppId,
            Title=self._convert_from_novx(
                self.novel.plotPoints[ppId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.plotPoints[ppId].desc,
            ),
            Notes=self._convert_from_novx(
                self.novel.plotPoints[ppId].notes,
            ),
            Section='',
            scID='',
            SectionTitle='',
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            ProjectPath=self.projectPath,
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
        )
        scId = self.novel.plotPoints[ppId].sectionAssoc
        if scId:
            template = Template(self._assocSectionTemplate)
            plotPointMapping['Section'] = template.safe_substitute(
                self._get_sectionAssocMapping(scId)
            )
        return plotPointMapping

    def _get_sectionAssocMapping(self, scId):
        sectionAssocMapping = dict(
            SectionTitle=self.novel.sections[scId].title,
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            scID=scId,
            ManuscriptSuffix=MANUSCRIPT_SUFFIX,
            SectionsSuffix=SECTIONS_SUFFIX,
        )
        return sectionAssocMapping

    def _get_sectionMapping(
            self,
            scId,
            sectionNumber,
            wordsTotal,
            firstInChapter=False,
            isEpigraph=False,
        ):

        if sectionNumber == 0:
            sectionNumber = ''
        if self.novel.sections[scId].tags is not None:
            tags = list_to_string(
                self.novel.sections[scId].tags, divider=self._DIVIDER
            )
        else:
            tags = ''

        if self.novel.sections[scId].viewpoint:
            viewpointChar = self.novel.characters[
                self.novel.sections[scId].viewpoint].title
        else:
            viewpointChar = ''

        if self.novel.sections[scId].characters is not None:
            sChList = []
            for crId in self.novel.sections[scId].characters:
                sChList.append(self.novel.characters[crId].title)
            sectionChars = list_to_string(sChList, divider=self._DIVIDER)

        else:
            sectionChars = ''
            viewpointChar = ''

        if self.novel.sections[scId].locations is not None:
            sLcList = []
            for lcId in self.novel.sections[scId].locations:
                sLcList.append(self.novel.locations[lcId].title)
            sectionLocs = list_to_string(sLcList, divider=self._DIVIDER)
        else:
            sectionLocs = ''

        if self.novel.sections[scId].items is not None:
            sItList = []
            for itId in self.novel.sections[scId].items:
                sItList.append(self.novel.items[itId].title)
            sectionItems = list_to_string(sItList, divider=self._DIVIDER)
        else:
            sectionItems = ''

        if (
            self.novel.sections[scId].date is not None
            and self.novel.sections[scId].date != Section.NULL_DATE
        ):
            scDay = ''
            dateStr = self.novel.sections[scId].date
            cmbDateStr = self.novel.sections[scId].localeDate
            yearStr, monthStr, dayStr = PyCalendar.y_m_d_str(dateStr)
            dtMonth = PyCalendar.MONTHS[int(monthStr)]
            dtWeekday = PyCalendar.WEEKDAYS[self.novel.sections[scId].weekDay]
        else:
            dateStr = ''
            yearStr = ''
            monthStr = ''
            dayStr = ''
            dtMonth = ''
            dtWeekday = ''
            if self.novel.sections[scId].day is not None:
                scDay = self.novel.sections[scId].day
                cmbDateStr = f'{_("Day")} {self.novel.sections[scId].day}'
            else:
                scDay = ''
                cmbDateStr = ''

        if self.novel.sections[scId].time is not None:
            scTime = PyCalendar.time_disp(self.novel.sections[scId].time)
            h, m, s = PyCalendar.h_m_s_str(self.novel.sections[scId].time)
            odsTime = f'PT{h}H{m}M{s}S'
        else:
            scTime = ''
            odsTime = ''

        if (
            self.novel.sections[scId].lastsDays is not None
            and self.novel.sections[scId].lastsDays != '0'
        ):
            lastsDays = self.novel.sections[scId].lastsDays
            days = f'{self.novel.sections[scId].lastsDays}d '
        else:
            lastsDays = ''
            days = ''

        if (
            self.novel.sections[scId].lastsHours is not None
            and self.novel.sections[scId].lastsHours != '0'
        ):
            lastsHours = self.novel.sections[scId].lastsHours
            hours = f'{self.novel.sections[scId].lastsHours}h '
        else:
            lastsHours = ''
            hours = ''

        if (
            self.novel.sections[scId].lastsMinutes is not None
            and self.novel.sections[scId].lastsMinutes != '0'
        ):
            lastsMinutes = self.novel.sections[scId].lastsMinutes
            minutes = f'{self.novel.sections[scId].lastsMinutes}min'
        else:
            lastsMinutes = ''
            minutes = ''

        duration = f'{days}{hours}{minutes}'
        (
            noSceneField1,
            noSceneField2,
            noSceneField3,
            otherSceneField1,
            otherSceneField2,
            otherSceneField3,
            __, __,
        ) = self._get_field_names()
        sectionMapping = dict(
            ID=scId,
            SectionNumber=sectionNumber,
            Title=self._convert_from_novx(
                self.novel.sections[scId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.sections[scId].desc,
                isEpigraph=isEpigraph,
                append=self.novel.sections[scId].appendToPrev,
            ),
            WordCount=str(self.novel.sections[scId].wordCount),
            WordsTotal=wordsTotal,
            Status=int(self.novel.sections[scId].status),
            SectionContent=self._convert_from_novx(
                self.novel.sections[scId].sectionContent,
                append=self.novel.sections[scId].appendToPrev,
                firstInChapter=firstInChapter,
                isEpigraph=isEpigraph,
                xml=True,
            ),
            Date=dateStr,
            Time=scTime,
            OdsTime=odsTime,
            Day=scDay,
            ScDate=cmbDateStr,
            DateYear=yearStr,
            DateMonth=monthStr,
            DateDay=dayStr,
            DateWeekday=dtWeekday,
            MonthName=dtMonth,
            LastsDays=lastsDays,
            LastsHours=lastsHours,
            LastsMinutes=lastsMinutes,
            Duration=duration,
            Scene=SCENE[self.novel.sections[scId].scene],
            Goal=self._convert_from_novx(
                self.novel.sections[scId].goal,
            ),
            Conflict=self._convert_from_novx(
                self.novel.sections[scId].conflict,
            ),
            Outcome=self._convert_from_novx(
                self.novel.sections[scId].outcome,
            ),
            Tags=self._convert_from_novx(tags, quick=True),
            Characters=sectionChars,
            Viewpoint=viewpointChar,
            Locations=sectionLocs,
            Items=sectionItems,
            Notes=self._convert_from_novx(self.novel.sections[scId].notes),
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            ProjectPath=self.projectPath,
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
            ManuscriptSuffix=MANUSCRIPT_SUFFIX,
            SectionsSuffix=SECTIONS_SUFFIX,

            NotASceneField1=noSceneField1,
            NotASceneField2=noSceneField2,
            NotASceneField3=noSceneField3,
            OtherSceneField1=otherSceneField1,
            OtherSceneField2=otherSceneField2,
            OtherSceneField3=otherSceneField3,

            CustomPlotProgress=noSceneField1,
            CustomCharacterization=noSceneField2,
            CustomWorldBuilding=noSceneField3,
            CustomGoal=otherSceneField1,
            CustomConflict=otherSceneField2,
            CustomOutcome=otherSceneField3,
        )
        return sectionMapping

    def _get_sections(
            self,
            chId,
            sectionNumber,
            wordsTotal,
            isEpigraph,
    ):
        lines = []
        firstSectionInChapter = True
        for scId in self.novel.tree.get_children(chId):
            template = None
            dispNumber = 0
            if not self.sectionFilter.accept(self, scId):
                continue

            sectionContent = self.novel.sections[scId].sectionContent
            if sectionContent is None:
                sectionContent = ''

            if self.novel.sections[scId].scType == 2:
                if self._stage1Template:
                    template = Template(self._stage1Template)
                else:
                    continue

            elif self.novel.sections[scId].scType == 3:
                if self._stage2Template:
                    template = Template(self._stage2Template)
                else:
                    continue

            elif (
                self.novel.sections[scId].scType == 1
                or self.novel.chapters[chId].chType == 1
            ):
                isEpigraph = False
                if self._unusedSectionTemplate:
                    template = Template(self._unusedSectionTemplate)
                else:
                    continue

            elif isEpigraph and not self._epigraphTemplate:
                isEpigraph = False
                continue

            else:
                sectionNumber += 1
                dispNumber = sectionNumber
                wordsTotal += self.novel.sections[scId].wordCount
                template = Template(self._sectionTemplate)
                if isEpigraph:
                    template = Template(self._epigraphTemplate)
                elif firstSectionInChapter:
                    if self._firstSectionTemplate:
                        template = Template(self._firstSectionTemplate)
                elif self.novel.sections[scId].appendToPrev:
                    if self._appendedSectionTemplate:
                        template = Template(self._appendedSectionTemplate)

            if not (
                isEpigraph
                or firstSectionInChapter
                or self.novel.sections[scId].appendToPrev
                or self.novel.sections[scId].scType > 1
            ):
                lines.append(self._sectionDivider)

            tempEpigraph = False
            tempFirstSection = firstSectionInChapter
            if template is not None:
                if self.novel.sections[scId].scType == 0:
                    if isEpigraph:
                        tempEpigraph = True
                        tempFirstSection = False
                lines.append(
                    template.safe_substitute(
                        self._get_sectionMapping(
                            scId, dispNumber,
                            wordsTotal,
                            firstInChapter=tempFirstSection,
                            isEpigraph=tempEpigraph,
                        )
                    )
                )
            if self.novel.sections[scId].scType < 2:
                isEpigraph = False
            if self.novel.sections[scId].scType == 0 and tempFirstSection:
                firstSectionInChapter = False

        return lines, sectionNumber, wordsTotal

    def _get_prjNoteMapping(self, pnId):
        noteMapping = dict(
            ID=pnId,
            Title=self._convert_from_novx(
                self.novel.projectNotes[pnId].title,
                quick=True,
            ),
            Desc=self._convert_from_novx(
                self.novel.projectNotes[pnId].desc,
            ),
            ProjectName=self._convert_from_novx(
                self.projectName,
                quick=True,
            ),
            ProjectPath=self.projectPath,
        )
        return noteMapping

    def _get_projectNotes(self):
        lines = []
        template = Template(self._projectNoteTemplate)
        for pnId in self.novel.tree.get_children(PN_ROOT):
            pnMap = self._get_prjNoteMapping(pnId)
            lines.append(template.safe_substitute(pnMap))
        return lines

    def _get_text(self):
        lines = self._get_fileHeader()
        lines.extend(self._get_chapters())
        lines.extend(self._get_characters())
        lines.extend(self._get_locations())
        lines.extend(self._get_items())
        lines.extend(self._get_plotlines())
        lines.extend(self._get_projectNotes())
        lines.extend(self._get_fileFooter())
        return ''.join(lines)



def odf_is_locked(filePath):
    prjPath, fileName = os.path.split(filePath)
    return os.path.isfile(f'{prjPath}/.~lock.{fileName}#')



class OdfFile(FileExport):
    _ODF_COMPONENTS = []
    _MIMETYPE = ''
    _MANIFEST_XML = ''
    _STYLES_XML = ''
    _META_XML = ''

    NAMESPACES = dict(
        office='urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        style='urn:oasis:names:tc:opendocument:xmlns:style:1.0',
        text='urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        table='urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        draw='urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
        fo='urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
        xlink='http://www.w3.org/1999/xlink',
        dc='http://purl.org/dc/elements/1.1/',
        meta='urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
        number='urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0',
        svg='urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
        chart='urn:oasis:names:tc:opendocument:xmlns:chart:1.0',
        dr3d='urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0',
        math='http://www.w3.org/1998/Math/MathML',
        form='urn:oasis:names:tc:opendocument:xmlns:form:1.0',
        script='urn:oasis:names:tc:opendocument:xmlns:script:1.0',
        ooo='http://openoffice.org/2004/office',
        ooow='http://openoffice.org/2004/writer',
        oooc='http://openoffice.org/2004/calc',
        dom='http://www.w3.org/2001/xml-events',
        rpt='http://openoffice.org/2005/report',
        of='urn:oasis:names:tc:opendocument:xmlns:of:1.2',
        xhtml='http://www.w3.org/1999/xhtml',
        grddl='http://www.w3.org/2003/g/data-view#',
        tableooo='http://openoffice.org/2009/table',
        loext=(
            'urn:org:documentfoundation:names:experimental:'
            'office:xmlns:loext:1.0'
        ),
    )

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self._tempDir = tempfile.mkdtemp(suffix='.tmp', prefix='odf_')
        self._originalPath = self._filePath

    def __del__(self):
        self._tear_down()

    def is_locked(self):
        return odf_is_locked(self.filePath)

    def write_content_xml(self):
        super().write()

    def write(self):

        self._set_up()

        self._originalPath = self._filePath
        self._filePath = f'{self._tempDir}/content.xml'
        self.write_content_xml()
        self._filePath = self._originalPath

        workdir = os.getcwd()
        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise RuntimeError(
                    f'{_("Cannot overwrite file")}: '
                    f'"{norm_path(self.filePath)}".'
                )
            else:
                backedUp = True
        try:
            with zipfile.ZipFile(self.filePath, 'w') as odfTarget:
                os.chdir(self._tempDir)
                for file in self._ODF_COMPONENTS:
                    odfTarget.write(file, compress_type=zipfile.ZIP_DEFLATED)
        except:
            os.chdir(workdir)
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise RuntimeError(
                f'{_("Cannot create file")}: '
                f'"{norm_path(self.filePath)}".'
            )

        os.chdir(workdir)
        self._tear_down()
        return f'{_("File written")}: "{norm_path(self.filePath)}".'

    def _escape(self, text):
        try:
            return sax.saxutils.escape(text)

        except AttributeError:
            return text

    def _get_styles_xml_str(self):
        self.novel.check_locale()
        localeMapping = dict(
            Language=self.novel.languageCode,
            Country=self.novel.countryCode or 'none',
        )
        template = Template(self._STYLES_XML)
        stylesXmlStr = template.safe_substitute(localeMapping)
        return stylesXmlStr

    def _set_up(self):

        try:
            self._tear_down()
            os.mkdir(self._tempDir)
            os.mkdir(f'{self._tempDir}/META-INF')
        except:
            raise RuntimeError(
                f'{_("Cannot create directory")}: '
                f'"{norm_path(self._tempDir)}".'
            )
        try:
            with open(
                f'{self._tempDir}/mimetype',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(self._MIMETYPE)
        except:
            raise RuntimeError(f'{_("Cannot write file")}: "mimetype"')

        try:
            with open(
                f'{self._tempDir}/META-INF/manifest.xml',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(self._MANIFEST_XML)
        except:
            raise RuntimeError(f'{_("Cannot write file")}: "manifest.xml"')

        stylesXmlStr = self._get_styles_xml_str()
        try:
            with open(
                f'{self._tempDir}/styles.xml',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(stylesXmlStr)
        except:
            raise RuntimeError(f'{_("Cannot write file")}: "styles.xml"')

        metaMapping = dict(
            Author=self._escape(self.novel.authorName),
            Title=self._escape(self.novel.title),
            Summary=self._escape(self.novel.desc),
            Datetime=datetime.today().replace(microsecond=0).isoformat(),
        )
        template = Template(self._META_XML)
        stylesXmlStr = template.safe_substitute(metaMapping)
        try:
            with open(
                f'{self._tempDir}/meta.xml',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(stylesXmlStr)
        except:
            raise RuntimeError(f'{_("Cannot write file")}: "meta.xml".')

    def _tear_down(self):
        try:
            rmtree(self._tempDir)
        except:
            pass

from xml import sax



class NovxToOdt(sax.ContentHandler):

    def __init__(self):
        super().__init__()
        self.odtLines = None
        self._languages = None
        self._indentParagraph = None
        self._note = None
        self._comment = None
        self._quotations = None
        self._firstParagraphInChapter = None
        self._spanLevel = None

    def feed(
        self,
        xmlString,
        languages,
        append,
        firstInChapter,
        isEpigraph,
    ):
        self._languages = languages
        self._firstParagraphInChapter = firstInChapter
        self._indentParagraph = append and not isEpigraph
        self._isEpigraph = isEpigraph
        self._quotations = False
        self._note = None
        self._spanLevel = 0
        self._comment = False
        self.odtLines = []
        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        content = sax.saxutils.escape(content)
        self.odtLines.append(content)
        self._indentParagraph = not self._quotations

    def endElement(self, name):
        if name == 'p':
            while self._spanLevel > 0:
                self._spanLevel -= 1
                self.odtLines.append('</text:span>')
            self.odtLines.append('</text:p>')
            self._quotations = False
            return

        if name in ('em', 'strong', 'span'):
            self.odtLines.append('</text:span>')
            return

        if name == 'creator':
            self.odtLines.append('</dc:creator>')
            return

        if name == 'date':
            self.odtLines.append('</dc:date>')
            return

        if name == 'note-citation':
            self.odtLines.append(
                '</text:note-citation><text:note-body>'
            )
            return
        if name == 'comment':
            self.odtLines.append('</office:annotation>')
            self._comment = False
            return

        if name == 'note':
            self._note = None
            self.odtLines.append('</text:note-body></text:note>')

        if name in (
            'h5',
            'h6',
            'h7',
            'h8',
            'h9',
        ):
            while self._spanLevel > 0:
                self._spanLevel -= 1
                self.odtLines.append('</text:span>')
            self.odtLines.append('</text:p>')
            self._indentParagraph = False
            return

        if name == 'li':
            self.odtLines.append('</text:list-item>')
            return

        if name == 'ul':
            self._list = False
            self._indentParagraph = False
            self.odtLines.append('</text:list>')
            return

    def startElement(self, name, attrs):
        xmlAttributes = {}
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            xmlAttributes[attrKey] = attrValue

        if name == 'p':
            if xmlAttributes.get('style', None) == 'quotations':
                self.odtLines.append(
                    '<text:p text:style-name="Quotations">'
                )
                self._quotations = True
            elif self._note:
                self.odtLines.append(
                    f'<text:p text:style-name="{self._note.title()}">'
                )
            elif self._comment:
                self.odtLines.append('<text:p>')
            elif self._firstParagraphInChapter:
                self.odtLines.append(
                    f'<text:p text:style-name="{_("Chapter_20_beginning")}">'
                )
            elif self._isEpigraph:
                self.odtLines.append(
                    f'<text:p text:style-name="{_("Epigraph")}">'
                )
            elif self._indentParagraph:
                self.odtLines.append(
                    '<text:p text:style-name="First_20_line_20_indent">'
                )
            else:
                self.odtLines.append(
                    '<text:p text:style-name="Text_20_body">'
                )
            if not self._isEpigraph:
                self._firstParagraphInChapter = False
                self._indentParagraph = False

            language = xmlAttributes.get('xml:lang', None)
            if language:
                i = self._languages.index(language) + 1
                self.odtLines.append(
                    f'<text:span text:style-name="T{i}">'
                )
                self._spanLevel += 1
            return

        if name == 'em':
            self.odtLines.append(
                '<text:span text:style-name="Emphasis">'
            )
            return

        if name == 'strong':
            self.odtLines.append(
                '<text:span text:style-name="Strong_20_Emphasis">'
            )
            return

        if name == 'span':
            language = xmlAttributes.get('xml:lang', None)
            if language:
                i = self._languages.index(language) + 1
                self.odtLines.append(
                    f'<text:span text:style-name="T{i}">'
                )
            return

        if name == 'comment':
            self._comment = True
            self.odtLines.append('<office:annotation>')
            return

        if name == 'note':
            self._note = xmlAttributes.get('class', 'footnote')
            self.odtLines.append(
                f'<text:note text:note-class="{self._note}">'
            )
            return

        if name == 'creator':
            self.odtLines.append('<dc:creator>')
            return

        if name == 'date':
            self.odtLines.append('<dc:date>')
            return

        if name == 'note-citation':
            self.odtLines.append('<text:note-citation>')
            return

        if name in (
            'h5',
            'h6',
            'h7',
            'h8',
            'h9',
        ):
            level = name[-1]
            self.odtLines.append(
                f'<text:p text:style-name="Heading_20_{level}">'
            )
            language = xmlAttributes.get('xml:lang', None)
            if language:
                i = self._languages.index(language) + 1
                self.odtLines.append(
                    f'<text:span text:style-name="T{i}">'
                )
                self._spanLevel += 1
            return

        if name == 'ul':
            self._list = True
            self.odtLines.append('<text:list>')
            return

        if name == 'li':
            self.odtLines.append('<text:list-item>')


class OdtWriter(OdfFile):

    EXTENSION = '.odt'

    _ODF_COMPONENTS = [
        'manifest.rdf',
        'META-INF',
        'content.xml',
        'meta.xml',
        'mimetype',
        'styles.xml',
        'META-INF/manifest.xml',
    ]

    _CONTENT_XML_HEADER = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<office:document-content '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
        'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
        'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
        'xmlns:fo="urn:oasis:names:tc:opendocument:'
        'xmlns:xsl-fo-compatible:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" '
        'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
        'xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" '
        'xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" '
        'xmlns:math="http://www.w3.org/1998/Math/MathML" '
        'xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" '
        'xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:ooow="http://openoffice.org/2004/writer" '
        'xmlns:oooc="http://openoffice.org/2004/calc" '
        'xmlns:dom="http://www.w3.org/2001/xml-events" '
        'xmlns:xforms="http://www.w3.org/2002/xforms" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:rpt="http://openoffice.org/2005/report" '
        'xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'xmlns:tableooo="http://openoffice.org/2009/table" '
        'xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:'
        'xmlns:field:1.0" office:version="1.2">\n'
        ' <office:scripts/>\n'
        ' <office:font-face-decls>\n'
        '  <style:font-face style:name="StarSymbol" '
        'svg:font-family="StarSymbol" style:font-charset="x-symbol"/>\n'
        '  <style:font-face style:name="Consolas" svg:font-family="Consolas" '
        'style:font-adornments="Standard" '
        'style:font-family-generic="modern" '
        'style:font-pitch="fixed"/>\n'
        '  <style:font-face style:name="Courier New" '
        'svg:font-family="&apos;Courier New&apos;" '
        'style:font-adornments="Standard" style:font-family-generic="modern" '
        'style:font-pitch="fixed"/>\n'
        ' </office:font-face-decls>\n'
        ' <office:automatic-styles/>\n'
        ' <office:body>\n'
        '  <office:text text:use-soft-page-breaks="true">\n\n'
    )
    _CONTENT_XML_FOOTER = (
        '  </office:text>\n'
        ' </office:body>\n'
        '</office:document-content>\n'
    )
    _META_XML = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:'
        'xmlns:office:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'office:version="1.2">\n'
        '  <office:meta>\n'
        '    <meta:generator>novelibre</meta:generator>\n'
        '    <dc:title>$Title</dc:title>\n'
        '    <dc:description>$Summary</dc:description>\n'
        '    <dc:subject></dc:subject>\n'
        '    <meta:keyword></meta:keyword>\n'
        '    <meta:initial-creator>$Author</meta:initial-creator>\n'
        '    <dc:creator></dc:creator>\n'
        '    <meta:creation-date>${Datetime}Z</meta:creation-date>\n'
        '    <dc:date></dc:date>\n'
        '  </office:meta>\n'
        '</office:document-meta>\n'
    )
    _MANIFEST_XML = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<manifest:manifest '
        'xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" '
        'manifest:version="1.2">\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/vnd.oasis.opendocument.text" '
        'manifest:full-path="/" />\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/xml" '
        'manifest:full-path="content.xml" manifest:version="1.2" />\n'
        '  <manifest:file-entry manifest:media-type="application/rdf+xml" '
        'manifest:full-path="manifest.rdf" manifest:version="1.2" />\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/xml" manifest:full-path="styles.xml" '
        'manifest:version="1.2" />\n'
        '  <manifest:file-entry '
        'manifest:media-type="application/xml" manifest:full-path="meta.xml" '
        'manifest:version="1.2" />\n'
        '  <manifest:file-entry manifest:media-type="application/xml" '
        'manifest:full-path="settings.xml" manifest:version="1.2" />\n'
        '</manifest:manifest>\n'
    )
    _MANIFEST_RDF = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '  <rdf:Description rdf:about="styles.xml">\n'
        '    <rdf:type rdf:resource='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/odf#StylesFile"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="">\n'
        '    <ns0:hasPart xmlns:ns0='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" '
        'rdf:resource="styles.xml"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="content.xml">\n'
        '    <rdf:type rdf:resource='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="">\n'
        '    <ns0:hasPart '
        'xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" '
        'rdf:resource="content.xml"/>\n'
        '  </rdf:Description>\n'
        '  <rdf:Description rdf:about="">\n'
        '    <rdf:type rdf:resource='
        '"http://docs.oasis-open.org/ns/office/1.2/meta/pkg#Document"/>\n'
        '  </rdf:Description>\n'
        '</rdf:RDF>\n'
    )
    _STYLES_XML = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<office:document-styles '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
        'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
        'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
        'xmlns:fo="urn:oasis:names:tc:opendocument:'
        'xmlns:xsl-fo-compatible:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" '
        'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
        'xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" '
        'xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" '
        'xmlns:math="http://www.w3.org/1998/Math/MathML" '
        'xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" '
        'xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:ooow="http://openoffice.org/2004/writer" '
        'xmlns:oooc="http://openoffice.org/2004/calc" '
        'xmlns:dom="http://www.w3.org/2001/xml-events" '
        'xmlns:rpt="http://openoffice.org/2005/report" '
        'xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'xmlns:tableooo="http://openoffice.org/2009/table" '
        'xmlns:loext="urn:org:documentfoundation:names:experimental:'
        'office:xmlns:loext:1.0">\n'
        ' <office:font-face-decls>\n'
        '  <style:font-face style:name="StarSymbol" '
        'svg:font-family="StarSymbol" style:font-charset="x-symbol"/>\n'
        '  <style:font-face style:name="Calibri" '
        'svg:font-family="&apos;Calibri&apos;"/>\n'
        '  <style:font-face style:name="Courier New" '
        'svg:font-family="&apos;Courier New&apos;" '
        'style:font-adornments="Standard" style:font-family-generic="modern" '
        'style:font-pitch="fixed"/>\n'
        '  <style:font-face style:name="Consolas" '
        'svg:font-family="Consolas" style:font-adornments="Standard" '
        'style:font-family-generic="modern" style:font-pitch="fixed"/>\n'
        '  </office:font-face-decls>\n'
        ' <office:styles>\n'
        '  <style:default-style style:family="graphic">\n'
        '   <style:graphic-properties svg:stroke-color="#3465a4" '
        'draw:fill-color="#729fcf" fo:wrap-option="no-wrap" '
        'draw:shadow-offset-x="0.3cm" draw:shadow-offset-y="0.3cm" '
        'draw:start-line-spacing-horizontal="0.283cm" '
        'draw:start-line-spacing-vertical="0.283cm" '
        'draw:end-line-spacing-horizontal="0.283cm" '
        'draw:end-line-spacing-vertical="0.283cm" '
        'style:flow-with-text="true"/>\n'
        '   <style:paragraph-properties '
        'style:text-autospace="ideograph-alpha" style:line-break="strict" '
        'style:writing-mode="lr-tb" '
        'style:font-independent-line-spacing="false">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:color="#000000" '
        'fo:font-size="10pt" '
        'fo:language="$Language" fo:country="$Country" '
        'style:font-size-asian="10pt" style:language-asian="zxx" '
        'style:country-asian="none" style:font-size-complex="1pt" '
        'style:language-complex="zxx" style:country-complex="none"/>\n'
        '  </style:default-style>\n'
        '  <style:default-style style:family="paragraph">\n'
        '   <style:paragraph-properties '
        'fo:hyphenation-ladder-count="no-limit" '
        'style:text-autospace="ideograph-alpha" '
        'style:punctuation-wrap="hanging" style:line-break="strict" '
        'style:tab-stop-distance="1.251cm" style:writing-mode="lr-tb"/>\n'
        '   <style:text-properties fo:color="#000000" '
        'style:font-name="Calibri" fo:font-size="10.5pt" '
        'fo:language="$Language" fo:country="$Country" '
        'style:font-name-asian="Calibri" style:font-size-asian="10pt" '
        'style:language-asian="zxx" style:country-asian="none" '
        'style:font-name-complex="Segoe UI" style:font-size-complex="1pt" '
        'style:language-complex="zxx" style:country-complex="none" '
        'fo:hyphenate="false" fo:hyphenation-remain-char-count="2" '
        'fo:hyphenation-push-char-count="2"/>\n'
        '  </style:default-style>\n'
        '  <style:style style:name="Standard" style:family="paragraph" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties fo:line-height="0.73cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties style:font-name="Courier New" '
        'fo:font-size="12pt" fo:font-weight="normal"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Text_20_body" '
        'style:display-name="Text body" style:family="paragraph" '
        'style:parent-style-name="Standard" '
        'style:next-style-name="First_20_line_20_indent" style:class="text" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties style:page-number="auto">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="First_20_line_20_indent" '
        'style:display-name="First line indent" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0.499cm" '
        'style:auto-text-indent="false" style:page-number="auto"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Hanging_20_indent" '
        'style:display-name="Hanging indent" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" style:class="text">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="1cm" fo:margin-right="0cm" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="-0.499cm" '
        'style:auto-text-indent="false">\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="0cm"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Text_20_body_20_indent" '
        'style:display-name="Text body indent" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" style:class="text">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" '
        'style:auto-text-indent="false"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading" style:family="paragraph" '
        'style:parent-style-name="Standard" '
        'style:next-style-name="Text_20_body" style:class="text" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties fo:line-height="0.73cm" '
        'fo:text-align="center" style:justify-single-word="false" '
        'style:page-number="auto" fo:keep-with-next="always">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_1" '
        'style:display-name="Heading 1" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="1" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="1.461cm" fo:margin-bottom="0.73cm" '
        'style:page-number="auto">\n'
        '    <style:tab-stops/>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:text-transform="uppercase" '
        'fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_2" '
        'style:display-name="Heading 2" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="2" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="1.461cm" fo:margin-bottom="0.73cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_3" '
        'style:display-name="Heading 3" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="3" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="0.73cm" fo:margin-bottom="0.73cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties fo:font-style="italic"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_4" '
        'style:display-name="Heading 4" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties fo:margin-top="0.73cm" '
        'fo:margin-bottom="0.73cm" style:page-number="auto"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_5" '
        'style:display-name="Heading 5" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="" style:list-style-name="" '
        'style:class="text" style:master-page-name="">\n'
        '   <style:paragraph-properties style:page-number="auto"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_20_6" '
        'style:display-name="Heading 6" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_7" '
        'style:display-name="Heading 7" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_8" '
        'style:display-name="Heading 8" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_9" '
        'style:display-name="Heading 9" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" style:default-outline-level="" '
        'style:list-style-name="" style:class="text"/>\n'
        '  <style:style style:name="Heading_20_10" '
        'style:display-name="Heading 10" style:family="paragraph" '
        'style:parent-style-name="Heading" '
        'style:next-style-name="Text_20_body" '
        'style:default-outline-level="10" style:list-style-name="" '
        'style:class="text">\n'
        '   <style:text-properties fo:font-size="75%" fo:font-weight="bold"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Header" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties fo:text-align="end" '
        'style:justify-single-word="false" style:page-number="auto" '
        'fo:padding="0.049cm" fo:border-left="none" fo:border-right="none" '
        'fo:border-top="none" fo:border-bottom="0.002cm solid #000000" '
        'style:shadow="none">\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" '
        'style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:font-variant="normal" '
        'fo:text-transform="none" fo:font-style="italic"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Header_20_left" '
        'style:display-name="Header left" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Header_20_right" '
        'style:display-name="Header right" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Footer" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties fo:text-align="center" '
        'style:justify-single-word="false" style:page-number="auto" '
        'text:number-lines="false" text:line-number="0">\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:font-size="11pt"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Footer_20_left" '
        'style:display-name="Footer left" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Footer_20_right" '
        'style:display-name="Footer right" style:family="paragraph" '
        'style:parent-style-name="Standard" style:class="extra">\n'
        '   <style:paragraph-properties>\n'
        '    <style:tab-stops>\n'
        '     <style:tab-stop style:position="8.5cm" style:type="center"/>\n'
        '     <style:tab-stop style:position="17.002cm" '
        'style:type="right"/>\n'
        '    </style:tab-stops>\n'
        '   </style:paragraph-properties>\n'
        '  </style:style>\n'
        '  <style:style style:name="Title" style:family="paragraph" '
        'style:parent-style-name="Standard" style:next-style-name="Subtitle" '
        'style:class="chapter" style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin="100%" fo:margin-left="0cm" '
        'fo:margin-right="0cm" fo:margin-top="0.000cm" '
        'fo:margin-bottom="0cm" fo:line-height="200%" '
        'fo:text-align="center" style:justify-single-word="false" '
        'fo:text-indent="0cm" style:auto-text-indent="false" '
        'style:page-number="auto" fo:background-color="transparent" '
        'fo:padding="0cm" fo:border="none" text:number-lines="false" '
        'text:line-number="0">\n'
        '    <style:tab-stops/>\n'
        '    <style:background-image/>\n'
        '   </style:paragraph-properties>\n'
        '   <style:text-properties fo:text-transform="uppercase" '
        'fo:font-weight="normal" style:letter-kerning="false"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Subtitle" style:family="paragraph" '
        'style:parent-style-name="Title" style:class="chapter" '
        'style:master-page-name="">\n'
        '   <style:paragraph-properties loext:contextual-spacing="false" '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" '
        'style:page-number="auto"/>\n'
        '   <style:text-properties fo:font-variant="normal" '
        'fo:text-transform="none" fo:letter-spacing="normal" '
        'fo:font-style="italic" fo:font-weight="normal"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Quotations" style:family="paragraph" '
        'style:parent-style-name="Text_20_body" style:class="html">\n'
        '   <style:paragraph-properties fo:margin="100%" '
        'fo:margin-left="1cm" fo:margin-right="0cm" fo:margin-top="0cm" '
        'fo:margin-bottom="0cm" fo:text-indent="0cm" '
        'style:auto-text-indent="false"/>\n'
        '   <style:text-properties style:font-name="Consolas"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Emphasis" style:family="text">\n'
        '   <style:text-properties fo:font-style="italic" '
        'fo:background-color="transparent"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Strong_20_Emphasis" '
        'style:display-name="Strong Emphasis" style:family="text">\n'
        '   <style:text-properties fo:text-transform="uppercase"/>\n'
        '  </style:style>\n'
        ' </office:styles>\n'
        ' <office:automatic-styles>\n'
        '  <style:page-layout style:name="Mpm1">\n'
        '   <style:page-layout-properties fo:page-width="21.001cm" '
        'fo:page-height="29.7cm" style:num-format="1" '
        'style:paper-tray-name="[From printer settings]" '
        'style:print-orientation="portrait" fo:margin-top="3.2cm" '
        'fo:margin-bottom="2.499cm" fo:margin-left="2.701cm" '
        'fo:margin-right="3cm" style:writing-mode="lr-tb" '
        'style:layout-grid-color="#c0c0c0" style:layout-grid-lines="20" '
        'style:layout-grid-base-height="0.706cm" '
        'style:layout-grid-ruby-height="0.353cm" '
        'style:layout-grid-mode="none" style:layout-grid-ruby-below="false" '
        'style:layout-grid-print="false" style:layout-grid-display="false" '
        'style:footnote-max-height="0cm">\n'
        '    <style:columns fo:column-count="1" fo:column-gap="0cm"/>\n'
        '    <style:footnote-sep style:width="0.018cm" '
        'style:distance-before-sep="0.101cm" '
        'style:distance-after-sep="0.101cm" style:adjustment="left" '
        'style:rel-width="25%" style:color="#000000"/>\n'
        '   </style:page-layout-properties>\n'
        '   <style:header-style/>\n'
        '   <style:footer-style>\n'
        '    <style:header-footer-properties fo:min-height="1.699cm" '
        'fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="1.199cm" '
        'style:shadow="none" style:dynamic-spacing="false"/>\n'
        '   </style:footer-style>\n'
        '  </style:page-layout>\n'
        ' </office:automatic-styles>\n'
        ' <office:master-styles>\n'
        '  <style:master-page style:name="Standard" '
        'style:page-layout-name="Mpm1">\n'
        '   <style:footer>\n'
        '    <text:p text:style-name="Footer"><text:page-number '
        'text:select-page="current"/></text:p>\n'
        '   </style:footer>\n'
        '  </style:master-page>\n'
        ' </office:master-styles>\n'
        '</office:document-styles>\n'
    )
    _NOVELIBRE_STYLES = (
        f'  <style:style style:name="{_("Chapter_20_beginning")}" '
        f'style:display-name="{_("Chapter beginning")}" '
        'style:family="paragraph" style:parent-style-name="Text_20_body" '
        'style:next-style-name="First_20_line_20_indent" '
        'style:class="text">\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Epigraph")}" '
        f'style:display-name="{_("Epigraph")}" '
        'style:family="paragraph" style:parent-style-name="Quotations" '
        f'style:next-style-name="{_("Epigraph source")}" style:class="text">\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Epigraph_20_source")}" '
        f'style:display-name="{_("Epigraph source")}" '
        f'style:family="paragraph" style:parent-style-name="{_("Epigraph")}" '
        'style:next-style-name="Text_20_body" style:class="text">\n'
        '  <style:paragraph-properties fo:margin-top="0cm" '
        'fo:margin-bottom="1.46cm" fo:text-align="center"/>\n'
        '  <style:text-properties fo:language="zxx" fo:country="none" fo:font-style="italic"/>\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Section_20_mark")}" '
        f'style:display-name="{_("Section mark")}" '
        'style:family="paragraph" style:parent-style-name="Standard" '
        'style:next-style-name="Text_20_body" style:class="text">\n'
        '   <style:text-properties fo:color="#008000" '
        'fo:font-size="10pt" fo:language="zxx" fo:country="none"/>\n'
        '  </style:style>\n'
        f'  <style:style style:name="{_("Heading_20_3_20_invisible")}" '
        f'style:display-name="{_("Heading 3 invisible")}" '
        'style:family="paragraph" '
        'style:parent-style-name="Heading_20_3" style:class="text">\n'
        '   <style:paragraph-properties fo:margin-top="0cm" '
        'fo:margin-bottom="0cm" fo:line-height="100%"/>\n'
        '   <style:text-properties text:display="none"/>\n'
        '  </style:style>'
    )
    _NOVELIBRE_STYLE_NAMES = (
        _('Chapter_20_beginning'),
        _('Epigraph'),
        _('Epigraph_20_source'),
        _('Section_20_mark'),
        _('Heading_20_3_20_invisible'),
    )

    _MIMETYPE = 'application/vnd.oasis.opendocument.text'

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self._contentParser = NovxToOdt()

        self.userStylesXml = None

    @classmethod
    def add_novelibre_styles(cls, stylesXmlStr):
        success = False
        lines = stylesXmlStr.split('\n')
        newlines = []
        for line in lines:
            if '</office:styles>' in line:
                newlines.append(cls._NOVELIBRE_STYLES)
                success = True
            newlines.append(line)
        if not success:
            raise ValueError('Invalid XML Styles data')

        return '\n'.join(newlines)

    @classmethod
    def remove_novelibre_styles(cls, stylesXmlStr):
        for prefix in cls.NAMESPACES:
            ET.register_namespace(prefix, cls.NAMESPACES[prefix])
        root = ET.fromstring(stylesXmlStr)
        officeStyles = root.find('office:styles', cls.NAMESPACES)
        stylesToDiscard = []
        for officeStyle in officeStyles.iterfind(
            'style:style', cls.NAMESPACES
        ):
            officeStyleName = (
                officeStyle.attrib[f"{{{cls.NAMESPACES['style']}}}name"]
            )
            if officeStyleName in cls._NOVELIBRE_STYLE_NAMES:
                stylesToDiscard.append(officeStyle)
        for officeStyle in stylesToDiscard:
            officeStyles.remove(officeStyle)
        stylesXmlStr = ET.tostring(
            root,
            encoding='utf-8',
            xml_declaration=True
        ).decode('utf-8')
        return stylesXmlStr

    def write(self):
        if self.novel.languages is None:
            self.novel.get_languages()
        return super().write()

    def _convert_from_novx(
        self,
        text,
        quick=False,
        append=False,
        firstInChapter=False,
        xml=False,
        linebreaks=False,
        isEpigraph=False,
    ):
        if not text and not linebreaks and not isEpigraph:
            return ''

        if quick:
            return sax.saxutils.escape(text)

        if xml:
            self._contentParser.feed(
                text,
                self.novel.languages,
                append,
                firstInChapter,
                isEpigraph,
            )
            return ''.join(self._contentParser.odtLines)

        lines = sax.saxutils.escape(text).split('\n')
        if linebreaks:
            text = '<text:line-break/>'.join(lines)
        else:
            text = (
                '</text:p><text:p text:style-name="Text_20_body">'
            ).join(lines)

        if isEpigraph:
            firstParagraphStyle = _('Epigraph_20_source')
        else:
            firstParagraphStyle = "Text_20_body"
        return (
            f'<text:p text:style-name="{firstParagraphStyle}">{text}</text:p>'
        )

    def _get_fileHeaderMapping(self):
        fileHeaderMapping = super()._get_fileHeaderMapping()
        filterMessage = fileHeaderMapping['Filters']
        if filterMessage:
            fileHeaderMapping['Filters'] = filterMessage.replace(
                'First_20_line_20_indent', 'Text_20_body'
            ).replace('<text:p', '\n<text:p')
        return fileHeaderMapping

    def _get_sectionMapping(
            self,
            scId,
            sectionNumber,
            wordsTotal=None,
            isEpigraph=None,
            **kwargs,
    ):
        sectionMapping = super()._get_sectionMapping(
            scId,
            sectionNumber,
            wordsTotal=wordsTotal,
            isEpigraph=isEpigraph,
            **kwargs
        )
        sectionMapping['sectionTitle'] = _('Section')
        return sectionMapping

    def _get_styles_xml_str(self):
        if self.userStylesXml:
            try:
                with open(self.userStylesXml, 'r', encoding='utf-8') as f:
                    stylesXmlStr = f.read()
                stylesXmlStr = self._set_document_language(stylesXmlStr)
                stylesXmlStr = self.add_novelibre_styles(stylesXmlStr)
                return stylesXmlStr

            except:
                pass
        stylesXmlStr = super()._get_styles_xml_str()
        stylesXmlStr = self.add_novelibre_styles(stylesXmlStr)
        return stylesXmlStr

    def _set_document_language(self, stylesXmlStr):
        stylesXmlStr = re.sub(
            r'fo\:language=\".+?\"',
            f'fo:language="{self.novel.languageCode}"',
            stylesXmlStr
        )
        if self.novel.countryCode:
            countryCode = self.novel.countryCode
        else:
            countryCode = 'none'
        stylesXmlStr = re.sub(
            r'fo\:country=\".+?\"',
            f'fo:country="{countryCode}"',
            stylesXmlStr
        )
        return stylesXmlStr

    def _set_up(self):

        super()._set_up()

        try:
            with open(
                f'{self._tempDir}/manifest.rdf',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(self._MANIFEST_RDF)
        except:
            raise RuntimeError(f'{_("Cannot write file")}: "manifest.rdf"')



class OdtWFormatted(OdtWriter):
    _CONTENT_XML_HEADER = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<office:document-content '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
        'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
        'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
        'xmlns:fo="urn:oasis:names:tc:opendocument:'
        'xmlns:xsl-fo-compatible:1.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
        'xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" '
        'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
        'xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" '
        'xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" '
        'xmlns:math="http://www.w3.org/1998/Math/MathML" '
        'xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" '
        'xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" '
        'xmlns:ooo="http://openoffice.org/2004/office" '
        'xmlns:ooow="http://openoffice.org/2004/writer" '
        'xmlns:oooc="http://openoffice.org/2004/calc" '
        'xmlns:dom="http://www.w3.org/2001/xml-events" '
        'xmlns:xforms="http://www.w3.org/2002/xforms" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:rpt="http://openoffice.org/2005/report'
        '" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:grddl="http://www.w3.org/2003/g/data-view#" '
        'xmlns:tableooo="http://openoffice.org/2009/table" '
        'xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:'
        'xmlns:field:1.0" office:version="1.2">\n'
        ' <office:scripts/>\n'
        ' <office:font-face-decls>\n'
        '  <style:font-face style:name="StarSymbol" '
        'svg:font-family="StarSymbol" style:font-charset="x-symbol"/>\n'
        '  <style:font-face style:name="Consolas" svg:font-family="Consolas" '
        'style:font-adornments="Standard" style:font-family-generic="modern" '
        'style:font-pitch="fixed"/>\n'
        '  <style:font-face style:name="Courier New" '
        'svg:font-family="&apos;Courier New&apos;'
        '" style:font-adornments="Standard" style:font-family-generic='
        '"modern" style:font-pitch="fixed"/>\n'
        ' </office:font-face-decls>\n'
        ' $automaticStyles\n'
        ' <office:body>\n'
        '  <office:text text:use-soft-page-breaks="true">\n\n'
    )

    def _get_fileHeaderMapping(self):
        styleMapping = {}
        if self.novel.languages:
            lines = ['<office:automatic-styles>']
            for i, language in enumerate(self.novel.languages, 1):
                try:
                    lngCode, ctrCode = language.split('-')
                except:
                    lngCode = 'zxx'
                    ctrCode = 'none'
                lines.append(
                    (
                        f'  <style:style style:name="T{i}" '
                        'style:family="text">\n'
                        f'   <style:text-properties '
                        f'fo:language="{lngCode}" fo:country="{ctrCode}" '
                        f'style:language-asian="{lngCode}" '
                        f'style:country-asian="{ctrCode}" '
                        f'style:language-complex="{lngCode}" '
                        f'style:country-complex="{ctrCode}"/>\n'
                        '  </style:style>'
                    )
                )
            lines.append(' </office:automatic-styles>')
            styleMapping['automaticStyles'] = '\n'.join(lines)
        else:
            styleMapping['automaticStyles'] = '<office:automatic-styles/>'
        template = Template(self._CONTENT_XML_HEADER)
        projectTemplateMapping = super()._get_fileHeaderMapping()
        projectTemplateMapping['ContentHeader'] = template.safe_substitute(
            styleMapping
        )
        return projectTemplateMapping

    def _get_text(self):
        lines = self._get_fileHeader()
        lines.extend(self._get_chapters())
        lines.append(self._fileFooter)
        text = ''.join(lines)
        return text



class OdtWExport(OdtWFormatted):
    DESCRIPTION = _('manuscript')

    _fileHeader = (
        '$ContentHeader'
        '<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _partTemplate = (
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        '$Title</text:h>\n'
    )
    _chapterTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '$Title</text:h>\n'
    )
    _epigraphTemplate = '$SectionContent$Desc\n'
    _sectionTemplate = '$SectionContent\n'

    _sectionDivider = '<text:p text:style-name="Heading_20_4">* * *</text:p>\n'
    _fileFooter = OdtWFormatted._CONTENT_XML_FOOTER



class NvService(NovxService):

    def final_document_class(self):
        return OdtWExport

    def get_moon_phase_str(self, isoDate):
        return Moon.get_phase_string(isoDate)

    def new_configuration(self, **kwargs):
        return Configuration(**kwargs)

    def new_hovertip(self, anchor_widget, text):
        return Hovertip(anchor_widget, text)


from abc import ABC, abstractmethod


class FileFactory(ABC):

    def __init__(self, fileClasses):
        self._fileClasses = fileClasses

    @abstractmethod
    def new_file_objects(self, sourcePath, **kwargs):
        pass


class ExportSourceFactory(FileFactory):

    def new_file_objects(self, sourcePath, **kwargs):
        __, fileExtension = os.path.splitext(sourcePath)
        for fileClass in self._fileClasses:
            if fileClass.EXTENSION == fileExtension:
                sourceFile = fileClass(sourcePath, **kwargs)
                return sourceFile, None

        raise RuntimeError(
            f'{_("File type is not supported")}: "{norm_path(sourcePath)}".'
        )



class ExportTargetFactory(FileFactory):

    def new_file_objects(self, sourcePath, **kwargs):
        fileName, __ = os.path.splitext(sourcePath)
        suffix = kwargs['suffix']
        for fileClass in self._fileClasses:
            if fileClass.SUFFIX == suffix:
                if suffix is None:
                    suffix = ''
                targetFile = fileClass(
                    f'{fileName}{suffix}{fileClass.EXTENSION}',
                    **kwargs
                )
                return None, targetFile

        raise RuntimeError(
            f'{_("Export type is not supported")}: "{suffix}".'
        )


class ImportSourceFactory(FileFactory):

    def new_file_objects(self, sourcePath, **kwargs):
        for fileClass in self._fileClasses:
            if fileClass.SUFFIX is not None:
                if sourcePath.endswith(
                    f'{fileClass.SUFFIX }{fileClass.EXTENSION}'
                ):
                    sourceFile = fileClass(sourcePath, **kwargs)
                    return sourceFile, None

        raise RuntimeError(
            f'{_("This document is not meant to be written back")}.'
        )



class ImportTargetFactory(FileFactory):

    def new_file_objects(self, sourcePath, **kwargs):
        fileName, __ = os.path.splitext(sourcePath)
        sourceSuffix = kwargs['suffix']
        if sourceSuffix:
            e = fileName.split(sourceSuffix)
            if len(e) > 1:
                e.pop()
            ywPathBasis = ''.join(e)
        else:
            ywPathBasis = fileName

        for fileClass in self._fileClasses:
            if os.path.isfile(f'{ywPathBasis}{fileClass.EXTENSION}'):
                targetFile = fileClass(
                    f'{ywPathBasis}{fileClass.EXTENSION}',
                    **kwargs
                )
                return None, targetFile

        raise RuntimeError(f'{_("No novelibre project to write")}.')


class Ui:

    def __init__(self, title):
        self.infoWhatText = ''
        self.infoHowText = ''

    def ask_yes_no(self, message='', detail='', title=None):
        return True

    def set_info(self, message):
        self.infoWhatText = message

    def set_status(self, message):
        if message.startswith('!'):
            message = f'Error: {message.split("!", maxsplit=1)[1].strip()}'
        elif message.startswith('#'):
            message = (
            f'Notification: '
            f'{message.split("#", maxsplit=1)[1].strip()}'
        )
        self.infoHowText = message

    def show_warning(self, message='', detail='', title=None):
        pass

    def start(self):
        pass



class Converter:
    EXPORT_SOURCE_CLASSES = []
    EXPORT_TARGET_CLASSES = []
    IMPORT_SOURCE_CLASSES = []
    IMPORT_TARGET_CLASSES = []

    def __init__(self):
        self.ui = Ui('')
        self.newFile = None
        self.exportSourceFactory = ExportSourceFactory(
            self.EXPORT_SOURCE_CLASSES)
        self.exportTargetFactory = ExportTargetFactory(
            self.EXPORT_TARGET_CLASSES)
        self.importSourceFactory = ImportSourceFactory(
            self.IMPORT_SOURCE_CLASSES)
        self.importTargetFactory = ImportTargetFactory(
            self.IMPORT_TARGET_CLASSES)
        self.newProjectFactory = None

    def run(self, sourcePath, **kwargs):
        self.newFile = None
        if not os.path.isfile(sourcePath):
            self.ui.set_status(
                f'!{_("File not found")}: '
                f'"{norm_path(sourcePath)}".'
            )
            return

        try:
            source, __ = self.exportSourceFactory.new_file_objects(
                sourcePath,
                **kwargs
            )
        except RuntimeError:
            try:
                source, __ = self.importSourceFactory.new_file_objects(
                    sourcePath,
                    **kwargs
                )
            except RuntimeError:
                try:
                    (
                        source,
                        target
                    ) = self.newProjectFactory.new_file_objects(
                        sourcePath,
                        **kwargs
                    )
                except RuntimeError as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self._create_novx(source, target)
            else:
                kwargs['suffix'] = source.SUFFIX
                try:
                    (
                        __,
                        target
                    ) = self.importTargetFactory.new_file_objects(
                        sourcePath,
                        **kwargs
                    )
                except RuntimeError as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self._import_to_novx(source, target)
        else:
            try:
                (
                    __,
                    target
                ) = self.exportTargetFactory.new_file_objects(
                    sourcePath,
                    **kwargs
                )
            except RuntimeError as ex:
                self.ui.set_status(f'!{str(ex)}')
            else:
                self._export_from_novx(source, target)

    def _check(self, source, target):
        if source.filePath is None:
            raise RuntimeError(f'{_("File type is not supported")}.')

        if not os.path.isfile(source.filePath):
            raise RuntimeError(
                f'{_("File not found")}: "{norm_path(source.filePath)}".'
            )

        if source.is_locked():
            raise RuntimeError(f'{_("Please close the document first")}".')

        if target.is_locked():
            raise RuntimeError(f'{_("Please close the document first")}.')

        if target.filePath is None:
            raise RuntimeError(f'{_("File type is not supported")}.')

        if (
            os.path.isfile(target.filePath)
            and not self._confirm_overwrite(target.filePath)
        ):
            raise UserWarning(f'{_("Action canceled by user")}.')

    def _confirm_overwrite(self, filePath):
        return self.ui.ask_yes_no(
            message=_('Overwrite existing file?'),
            detail=norm_path(filePath)
            )

    def _create_novx(self, source, target):
        msg = _('Create a novelibre project file from {0}\nNew project: "{1}"')
        self.ui.set_info(
            msg.format(
                source.DESCRIPTION,
                norm_path(target.filePath)
            )
        )
        if os.path.isfile(target.filePath):
            self.ui.set_status(
                (
                    f'!{_("File already exists")}: '
                    f'"{norm_path(target.filePath)}".'
                )
        )
        else:
            statusMsg = ''
            try:
                self._check(source, target)
                source.novel = Novel(
                    tree=NvTree(),
                    noSceneField1=NO_SCENE_FIELD_1_DEFAULT,
                    noSceneField2=NO_SCENE_FIELD_2_DEFAULT,
                    noSceneField3=NO_SCENE_FIELD_3_DEFAULT,
                    otherSceneField1=OTHER_SCENE_FIELD_1_DEFAULT,
                    otherSceneField2=OTHER_SCENE_FIELD_2_DEFAULT,
                    otherSceneField3=OTHER_SCENE_FIELD_3_DEFAULT,
                    crField1=CR_FIELD_1_DEFAULT,
                    crField2=CR_FIELD_2_DEFAULT,
                )
                source.novel.check_locale()
                source.read()
                target.novel = source.novel
                target.write()
            except RuntimeError as ex:
                statusMsg = f'!{str(ex)}'
                self.newFile = None
            else:
                statusMsg = (
                    f'{_("File written")}: '
                    f'"{norm_path(target.filePath)}".'
                )
                self.newFile = target.filePath
            finally:
                self.ui.set_status(statusMsg)

    def _export_from_novx(self, source, target):
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(
                source.DESCRIPTION,
                norm_path(source.filePath),
                target.DESCRIPTION,
                norm_path(target.filePath)
            )
        )
        statusMsg = ''
        try:
            self._check(source, target)
            source.novel = Novel(
                tree=NvTree(),
                noSceneField1=NO_SCENE_FIELD_1_DEFAULT,
                noSceneField2=NO_SCENE_FIELD_2_DEFAULT,
                noSceneField3=NO_SCENE_FIELD_3_DEFAULT,
                otherSceneField1=OTHER_SCENE_FIELD_1_DEFAULT,
                otherSceneField2=OTHER_SCENE_FIELD_2_DEFAULT,
                otherSceneField3=OTHER_SCENE_FIELD_3_DEFAULT,
                crField1=CR_FIELD_1_DEFAULT,
                crField2=CR_FIELD_2_DEFAULT,
            )
            source.read()
            target.novel = source.novel
            target.write()
        except RuntimeError as ex:
            statusMsg = f'!{str(ex)}'
            self.newFile = None
        else:
            statusMsg = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
        finally:
            self.ui.set_status(statusMsg)

    def _import_to_novx(self, source, target):
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(
                source.DESCRIPTION,
                norm_path(source.filePath),
                target.DESCRIPTION,
                norm_path(target.filePath)
            )
        )
        self.newFile = None
        statusMsg = ''
        try:
            self._check(source, target)
            target.novel = Novel(
                tree=NvTree(),
                noSceneField1=NO_SCENE_FIELD_1_DEFAULT,
                noSceneField2=NO_SCENE_FIELD_2_DEFAULT,
                noSceneField3=NO_SCENE_FIELD_3_DEFAULT,
                otherSceneField1=OTHER_SCENE_FIELD_1_DEFAULT,
                otherSceneField2=OTHER_SCENE_FIELD_2_DEFAULT,
                otherSceneField3=OTHER_SCENE_FIELD_3_DEFAULT,
                crField1=CR_FIELD_1_DEFAULT,
                crField2=CR_FIELD_2_DEFAULT,
            )
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
        except Exception as ex:
            statusMsg = f'!{str(ex)}'
        else:
            statusMsg = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
            if source.projectStructureModified:
                os.replace(source.filePath, f'{source.filePath}.bak')
                statusMsg = f'{statusMsg} - {_("Source document deleted")}.'
        finally:
            self.ui.set_status(f'{statusMsg}')



class Aeon2Converter(Converter):

    def run(self, sourcePath, **kwargs):
        nvService = NvService()
        kwargs['nv_service'] = nvService
        if not os.path.isfile(sourcePath):
            self.ui.set_status(
                f'!{_("File not found")}: "{norm_path(sourcePath)}".'
            )
            return

        fileName, fileExtension = os.path.splitext(sourcePath)
        if fileExtension == JsonTimeline2.EXTENSION:
            sourceFile = JsonTimeline2(sourcePath, **kwargs)
            if os.path.isfile(
                f'{fileName}{nvService.get_novx_file_extension()}'
            ):
                targetFile = nvService.new_novx_file(
                    f'{fileName}{nvService.get_novx_file_extension()}',
                    **kwargs
                )
                self._import_to_novx(sourceFile, targetFile)
            else:
                targetFile = nvService.new_novx_file(
                    f'{fileName}{nvService.get_novx_file_extension()}',
                    **kwargs
                )
                self._create_novx(sourceFile, targetFile)
        elif fileExtension == nvService.get_novx_file_extension():
            sourceFile = nvService.new_novx_file(sourcePath, **kwargs)
            targetFile = JsonTimeline2(
                f'{fileName}{JsonTimeline2.EXTENSION}',
                **kwargs
            )
            self._export_from_novx(sourceFile, targetFile)
        else:
            self.ui.set_status(
                    f'!{_("File type is not supported")}: '
                    f'"{norm_path(sourcePath)}".'
            )

    def _export_from_novx(self, source, target):
        nvService = NvService()
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(
                source.DESCRIPTION,
                norm_path(source.filePath),
                target.DESCRIPTION,
                norm_path(target.filePath)
            )
        )
        statusMsg = ''
        try:
            self._check(source, target)
            source.novel = nvService.new_novel()
            target.novel = nvService.new_novel()
            source.read()
            try:
                target.read()
            except NarrativeMissing:
                pass
            target.write(source.novel)
        except RuntimeError as ex:
            statusMsg = f'!{str(ex)}'
            self.newFile = None
        else:
            statusMsg = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
        finally:
            self.ui.set_status(statusMsg)
from tkinter import messagebox



class UiFacade(Ui):

    def __init__(self, title):
        Ui.__init__(self, title)

    def ask_ok_cancel(self, message='', detail='', title=None, **options):
        if title is None:
            title = self.title
        return messagebox.askokcancel(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def ask_yes_no(self, message='', detail='', title=None, **options):
        if title is None:
            title = self.title
        return messagebox.askyesno(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def ask_yes_no_cancel(self, message='', detail='', title=None, **options):
        if title is None:
            title = self.title
        return messagebox.askyesnocancel(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def show_error(self, message='', detail='', title=None, **options):
        if title is None:
            title = self.title
        messagebox.showerror(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def show_info(self, message='', detail='', title=None, **options):
        if title is None:
            title = self.title
        messagebox.showinfo(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def show_warning(self, message='', detail='', title=None, **options):
        if title is None:
            title = self.title
        messagebox.showwarning(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )



class UiTk(UiFacade):

    def __init__(self, title):
        super().__init__(title)
        self.title = title
        self.root = tk.Tk()
        self.root.minsize(400, 150)
        self.root.resizable(width='false', height='false')
        self.root.title(title)
        self._appInfo = tk.Label(self.root, text='')
        self._appInfo.pack(padx=20, pady=5)
        self._processInfo = tk.Label(self.root, text='', padx=20)
        self._processInfo.pack(pady=20, fill='both')
        self.root.quitButton = tk.Button(text=_("Quit"), command=quit)
        self.root.quitButton.config(height=1, width=10)
        self.root.quitButton.pack(pady=10)

    def set_status(self, message):
        if message.startswith('!'):
            self._processInfo.config(bg='red')
            self._processInfo.config(fg='white')
            self.infoHowText = message.split('!', maxsplit=1)[1].strip()
        else:
            self._processInfo.config(bg='green')
            self._processInfo.config(fg='white')
            self.infoHowText = message
        self._processInfo.config(text=self.infoHowText)

    def set_info(self, message):
        self.infoWhatText = message
        self._appInfo.config(text=message)

    def show_open_button(self, open_cmd):
        self.root.openButton = tk.Button(text=_("Open"), command=open_cmd)
        self.root.openButton.config(height=1, width=10)
        self.root.openButton.pack(pady=10)

    def start(self):
        self.root.mainloop()



def set_icon(widget, icon='logo', path=None, default=True):
    if path is None:
        path = os.path.dirname(sys.argv[0])
        if not path:
            path = '.'
        path = f'{path}/icons'
    try:
        pic = tk.PhotoImage(file=f'{path}/{icon}.png')
        widget.iconphoto(default, pic)
    except:
        return False

    return True


SUFFIX = ''
APPNAME = 'nv_aeon2'
SETTINGS = dict(
    narrative_arc='Narrative',
    property_description='Description',
    property_notes='Notes',
    property_moonphase='Moon phase',
    type_arc='Arc',
    type_character='Character',
    type_location='Location',
    type_item='Item',
    role_arc='Arc',
    role_plotline='Storyline',
    role_character='Participant',
    role_item='Item',
    role_location='Location',
    color_section='Red',
    color_event='Yellow',

)
OPTIONS = dict(
    add_moonphase=False,
    lock_on_export=False,
)


def run(sourcePath, silentMode=True, configDir='.'):
    if silentMode:
        ui = Ui('')
    else:
        ui = UiTk(f'{_("Synchronize Aeon Timeline 2 and novelibre")} 5.9.3')
        set_icon(ui.root, icon='aLogo32')

    sourceDir = os.path.dirname(sourcePath)
    if not sourceDir:
        sourceDir = '.'
    iniFileName = f'{APPNAME}.ini'
    iniFiles = [
        f'{configDir}/{iniFileName}',
        f'{sourceDir}/{iniFileName}',
    ]
    configuration = Configuration(SETTINGS, OPTIONS)
    for iniFile in iniFiles:
        configuration.filePath = iniFile
        configuration.read()
    kwargs = {'suffix': SUFFIX}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)
    converter = Aeon2Converter()
    converter.ui = ui

    converter.run(sourcePath, **kwargs)
    ui.start()
    sys.stderr.write(ui.infoHowText)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Synchronize Aeon Timeline 2 and novelibre',
        epilog='')
    parser.add_argument(
        'sourcePath',
        metavar='Sourcefile',
        help='The path of the aeonzip or novx file.'
    )

    parser.add_argument(
        '--silent',
        action="store_true",
        help='suppress error messages and the request to confirm overwriting'
    )
    args = parser.parse_args()
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        configDir = f'{homeDir}/.novx/config'
    except:
        configDir = '.'
    run(args.sourcePath, args.silent, configDir)
