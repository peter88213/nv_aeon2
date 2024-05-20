"""Provide a class for Aeon Timeline 2 JSON representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2nv
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from datetime import timedelta

from novxlib.file.file import File
from novxlib.model.plot_line import PlotLine
from novxlib.model.chapter import Chapter
from novxlib.model.character import Character
from novxlib.model.id_generator import create_id
from novxlib.model.section import Section
from novxlib.model.world_element import WorldElement
from novxlib.novx_globals import PL_ROOT
from novxlib.novx_globals import PLOT_LINE_PREFIX
from novxlib.novx_globals import CHAPTER_PREFIX
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import Error
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import SECTION_PREFIX
from novxlib.novx_globals import _
from nvaeon2lib.aeon2_fop import open_timeline
from nvaeon2lib.aeon2_fop import save_timeline
from nvaeon2lib.moonphase import get_moon_phase_plus
from nvaeon2lib.uid_helper import get_uid


class JsonTimeline2(File):
    """File representation of an Aeon Timeline 2 project. 

    Public class constants:
        SCN_KWVAR -- List of the names of the section keyword variables.
        CRT_KWVAR -- List of the names of the character keyword variables.
    
    Represents the .aeonzip file containing 'timeline.json'.
    """
    EXTENSION = '.aeonzip'
    DESCRIPTION = _('Aeon Timeline 2 project')
    SUFFIX = ''
    VALUE_YES = '1'
    # JSON representation of "yes" in Aeon2 "yes/no" properties
    DATE_LIMIT = (datetime(1, 1, 1) - datetime.min).total_seconds()
    # Dates before 1-01-01 can not be displayed properly in novelibre

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            
        Required keyword arguments:
            narrative_arc: str -- name of the user-defined "Narrative" arc.
            property_description: str -- name of the user-defined section description property.
            property_notes: str -- name of the user-defined section notes property.
            property_moonphase: str -- name of the user-defined section notes property.
            role_location: str -- name of the user-defined role for section locations.
            role_item: str -- name of the user-defined role for items in a section.
            role_character: str -- name of the user-defined role for characters in a section.
            type_character: str -- name of the user-defined "Character" type.
            type_location: str -- name of the user-defined "Location" type.
            type_item: str -- name of the user-defined "Item" type.
            color_section: str -- color of new section events.
            color_event: str -- color of new non-section events.
            add_moonphase: bool -- add a moon phase property to each event.
        
        Extends the superclass constructor.
        """
        super().__init__(filePath, **kwargs)
        self._jsonData = None

        # JSON[entities][name]
        self._entityNarrative = kwargs['narrative_arc']

        # JSON[template][properties][name]
        self._propertyDesc = kwargs['property_description']
        self._propertyNotes = kwargs['property_notes']
        self._propertyMoonphase = kwargs['property_moonphase']

        # JSON[template][types][name][roles]
        self._roleLocation = kwargs['role_location']
        self._roleItem = kwargs['role_item']
        self._roleCharacter = kwargs['role_character']

        # JSON[template][types][name]
        self._typeCharacter = kwargs['type_character']
        self._typeLocation = kwargs['type_location']
        self._typeItem = kwargs['type_item']

        # GUIDs
        self._tplDateGuid = None
        self._typeArcGuid = None
        self._typeCharacterGuid = None
        self._typeLocationGuid = None
        self._typeItemGuid = None
        self._roleArcGuid = None
        self._roleStorylineGuid = None
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
        """Parse the file and get the instance variables.
        
        Read the JSON part of the Aeon Timeline 2 file located at filePath, 
        and build a novelibre novel structure.
        - Events marked as sections are converted to sections in one single chapter.
        - Other events are converted to "Notes" sections in another chapter.
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """
        self._set_reference_date()
        self._jsonData = open_timeline(self.filePath)

        #--- Fetch JSON template data that may also be needed for writing.
        self._r_fetch_color_definitions()
        self._r_fetch_date_definition()
        self._r_fetch_arc_type_and_roles_guid()
        self._r_fetch_character_type_and_roles_guid()
        self._r_fetch_location_type_and_roles_guid()
        self._r_fetch_item_type_and_roles_guid()
        self._r_fetch_property_moonphase_guid()
        self._r_fetch_property_notes_guid()
        self._r_fetch_property_desc_guid()

        # At the beginning, self.novel contains either
        # - the  target data (if syncronizing an existing project), or
        # - a newly instantiated Novel object (if creating a project).
        # This means, there may be already elements with IDs.
        # In order to reuse them, they are collected in the "target element ID by title" dictionaries.

        #--- Check the source entities and raise an exception if there are ambiguous titles.
        self._r_check_source_characters()
        self._r_check_source_locations()
        self._r_check_source_items()
        self._r_check_source_arcs()

        #--- Check the target model elements and raise an exception if there are ambiguous titles.
        #    Get local lookup dictionaries.
        targetScIdsByTitle = self._r_check_target_sections()
        targetCrIdsByTitle = self._r_check_target_characters()
        targetItIdsByTitle = self._r_check_target_items()
        targetLcIdsByTitle = self._r_check_target_locations()
        targetAcIdsByTitle = self._r_check_target_arcs()

        #--- List the JSON entities and create missing target model elements.
        #    Get local lookup dictionaries.
        crIdsByGuid = self._r_fetch_character_guids_by_id(targetCrIdsByTitle)
        lcIdsByGuid = self._r_fetch_location_guids_by_id(targetLcIdsByTitle)
        itIdsByGuid = self._r_fetch_item_guids_by_id(targetItIdsByTitle)
        acIdsByGuid = self._r_fetch_arc_guids_by_id(targetAcIdsByTitle)

        #--- Abort here if there is no Narrative arc.
        if not self._entityNarrativeGuid:
            return

        #--- Build target sections from the source events.
        #    Get local lookup dictionaries.
        narrativeEvents, scIdsByDate = self._r_update_or_create_sections(
            targetScIdsByTitle,
            crIdsByGuid,
            lcIdsByGuid,
            itIdsByGuid,
            acIdsByGuid
            )

        #--- Tidy up the target.
        self._r_make_sections_deleted_in_aeon_unused(narrativeEvents)
        self._r_put_new_sections_into_new_chapter(scIdsByDate)
        self._r_adjust_timestamp()

    def write(self, source):
        """Write instance variables to the file.
        
        Update instance variables from a source instance.              
        Update date/time/duration from the source, if the section title matches.
        Overrides the superclass method.
        """
        self._set_reference_date()

        #--- Merge first.

        # Get local lists of source model elements that are related to sections.
        relatedCharacters, relatedLocations, relatedItems, relatedArcs = self._w_get_related_elements(source)

        #--- Check the source for ambiguous titles.
        #    Ignore elements that are not related to a section.
        self._w_check_source_characters(source, relatedCharacters)
        self._w_check_source_locations(source, relatedLocations)
        self._w_check_source_items(source, relatedItems)
        self._w_check_source_arcs(source, relatedArcs)

        srcScnTitles = self._w_check_source_sections(source)
        self._w_collect_trashed_sections(srcScnTitles)

        #--- Check the target for ambiguous titles.
        #    Get local lookup dictionaries.
        scIdsByTitle = self._w_check_target_sections()
        crIdsByTitle = self._w_check_target_characters()
        lcIdsByTitle = self._w_check_target_locations()
        itIdsByTitle = self._w_check_target_items()
        acIdsByTitle = self._w_check_target_arcs()

        #--- Update JSON data from the source.
        #    Get local lookup dictionaries.
        crIdsBySrcId = self._w_update_characters_from_source(source,
            crIdsByTitle,
            relatedCharacters
            )
        lcIdsBySrcId = self._w_update_locations_from_source(source,
            lcIdsByTitle,
            relatedLocations
            )
        itIdsBySrcId = self._w_update_items_from_source(source,
            itIdsByTitle,
            relatedItems
            )
        acIdsBySrcId = self._w_update_arcs_from_source(source,
            acIdsByTitle,
            relatedArcs
            )
        self._w_update_sections_from_source(source,
            scIdsByTitle,
            crIdsBySrcId,
            lcIdsBySrcId,
            itIdsBySrcId,
            acIdsBySrcId
            )

        #--- Begin writing

        #--- Complete the JSON template if needed.
        self._w_create_json_type_character_if_missing()
        self._w_create_json_type_location_if_missing()
        self._w_create_json_type_item_if_missing()
        self._w_create_json_type_arc_if_missing()
        self._w_create_json_role_arc_if_missing()
        self._w_create_json_role_storyline_if_missing()
        self._w_create_json_property_notes_if_missing()
        self._w_create_json_property_desc_if_missing()
        self._w_create_json_property_moonphase_if_missing()

        #--- Update the target JSON timeline elements.
        self._w_create_json_narrative_arc_if_missing()
        self._w_update_json_events_from_sections(scIdsByTitle)
        self._w_delete_trashed_events(scIdsByTitle)

        save_timeline(self._jsonData, self.filePath)

    def _r_adjust_timestamp(self):
        if self._timestampMax == 0:
            self._timestampMax = (self.referenceDate - datetime.min).total_seconds()

    def _r_check_source_arcs(self):
        arcNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeArcGuid:
                continue

            # Check whether the arc title is unique.
            if entity['name'] in arcNames:
                raise Error(_('Ambiguous Aeon arc "{}".').format(entity['name']))

            arcNames.append(entity['name'])

    def _r_check_source_characters(self):
        characterNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeCharacterGuid:
                continue

            # Check whether the character title is unique.
            if entity['name'] in characterNames:
                raise Error(_('Ambiguous Aeon character "{}".').format(entity['name']))

            characterNames.append(entity['name'])

    def _r_check_source_items(self):
        itemNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeItemGuid:
                continue

            # Check whether the item title is unique.
            if entity['name'] in itemNames:
                raise Error(_('Ambiguous Aeon item "{}".').format(entity['name']))

            itemNames.append(entity['name'])

    def _r_check_source_locations(self):
        locationNames = []
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeLocationGuid:
                continue

            # Check whether the location title is unique.
            if entity['name'] in locationNames:
                raise Error(_('Ambiguous Aeon location "{}".').format(entity['name']))

            locationNames.append(entity['name'])

    def _r_check_target_arcs(self):
        targetAcIdsByTitle = {}
        for acId in self.novel.plotLines:
            title = self.novel.plotLines[acId].title
            if title:
                if title in targetAcIdsByTitle:
                    raise Error(_('Ambiguous novelibre arc "{}".').format(title))

                targetAcIdsByTitle[title] = acId
        return targetAcIdsByTitle

    def _r_check_target_characters(self):
        targetCrIdsByTitle = {}
        for crId in self.novel.characters:
            title = self.novel.characters[crId].title
            if title:
                if title in targetCrIdsByTitle:
                    raise Error(_('Ambiguous novelibre character "{}".').format(title))

                targetCrIdsByTitle[title] = crId
        return targetCrIdsByTitle

    def _r_check_target_items(self):
        targetItIdsByTitle = {}
        for itId in self.novel.items:
            title = self.novel.items[itId].title
            if title:
                if title in targetItIdsByTitle:
                    raise Error(_('Ambiguous novelibre item "{}".').format(title))

                targetItIdsByTitle[title] = itId
        return targetItIdsByTitle

    def _r_check_target_locations(self):
        targetLcIdsByTitle = {}
        for lcId in self.novel.locations:
            title = self.novel.locations[lcId].title
            if title:
                if title in targetLcIdsByTitle:
                    raise Error(_('Ambiguous novelibre location "{}".').format(title))

                targetLcIdsByTitle[title] = lcId
        return targetLcIdsByTitle

    def _r_check_target_sections(self):
        targetScIdsByTitle = {}
        for scId in self.novel.sections:
            title = self.novel.sections[scId].title
            if title:
                if title in targetScIdsByTitle:
                    raise Error(_('Ambiguous novelibre section title "{}".').format(title))

                targetScIdsByTitle[title] = scId
        return targetScIdsByTitle

    def _r_fetch_arc_guids_by_id(self, targetAcIdsByTitle):
        acIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeArcGuid:
                continue

            # Check whether there is already a plot line for the entity.
            if entity['name'] in targetAcIdsByTitle:
                plId = targetAcIdsByTitle[entity['name']]
            elif entity['name'] != self._entityNarrative:

                # Create a new plot line, if it's not the "Narrative" indicator.
                plId = create_id(self.novel.plotLines, prefix=PLOT_LINE_PREFIX)
                self.novel.plotLines[plId] = PlotLine(title=entity['name'], shortName=entity['name'])
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
            if tplTyp['name'] == 'Arc':
                self._typeArcGuid = tplTyp['guid']
                for tplTypRol in tplTyp['roles']:
                    if tplTypRol['name'] == 'Arc':
                        self._roleArcGuid = tplTypRol['guid']
                    elif tplTypRol['name'] == 'Storyline':
                        self._roleStorylineGuid = tplTypRol['guid']
                continue

    def _r_fetch_character_guids_by_id(self, targetCrIdsByTitle):
        crIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeCharacterGuid:
                continue

            # Check whether there is already a character for the entity.
            if entity['name'] in targetCrIdsByTitle:
                crId = targetCrIdsByTitle[entity['name']]
            else:
                # Create a new character.
                crId = create_id(self.novel.characters, prefix=CHARACTER_PREFIX)
                self.novel.characters[crId] = Character(title=entity['name'])
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
                    # Restrict date/time calculation to dates within novelibre's range
                    birthDate = datetime.min + timedelta(seconds=timestamp)
                    self.novel.characters[crId].birthDate = birthDate.isoformat().split('T')[0]
            destroyRangePosition = entity.get('destroyRangePosition', None)
            if destroyRangePosition:
                timestamp = destroyRangePosition['timestamp']
                if timestamp >= self.DATE_LIMIT:  # Restrict date/time calculation to dates within novelibre's range
                    deathDate = datetime.min + timedelta(seconds=timestamp)
                    self.novel.characters[crId].deathDate = deathDate.isoformat().split('T')[0]
        return crIdsByGuid

    def _r_fetch_character_type_and_roles_guid(self):
        for tplTyp in self._jsonData['template']['types']:
            if tplTyp['name'] == self._typeCharacter:
                self._typeCharacterGuid = tplTyp['guid']
                for tplTypRol in tplTyp['roles']:
                    if tplTypRol['name'] == self._roleCharacter:
                        self._roleCharacterGuid = tplTypRol['guid']
                        break
                continue

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
            raise Error(_('"AD" era is missing in the calendar.'))

    def _r_fetch_item_guids_by_id(self, targetItIdsByTitle):
        itIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeItemGuid:
                continue

            # Check whether there is already an item for the entity.
            if entity['name'] in targetItIdsByTitle:
                itId = targetItIdsByTitle[entity['name']]
            else:
                itId = create_id(self.novel.items, prefix=ITEM_PREFIX)
                self.novel.items[itId] = WorldElement()
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
                continue

    def _r_fetch_location_guids_by_id(self, targetLcIdsByTitle):
        lcIdsByGuid = {}
        for entity in self._jsonData['entities']:
            if entity['entityType'] != self._typeLocationGuid:
                continue

            # Check whether there is already a location for the entity.
            if entity['name'] in targetLcIdsByTitle:
                lcId = targetLcIdsByTitle[entity['name']]
            else:
                lcId = create_id(self.novel.locations, prefix=LOCATION_PREFIX)
                self.novel.locations[lcId] = WorldElement()
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
                continue

    def _r_fetch_property_desc_guid(self):
        for tplPrp in self._jsonData['template']['properties']:
            if tplPrp['name'] == self._propertyDesc:
                self._propertyDescGuid = tplPrp['guid']
                return

    def _r_fetch_property_moonphase_guid(self):
        for tplPrp in self._jsonData['template']['properties']:
            if tplPrp['name'] == self._propertyMoonphase:
                self._propertyMoonphaseGuid = tplPrp['guid']
                break

    def _r_fetch_property_notes_guid(self):
        for tplPrp in self._jsonData['template']['properties']:
            if tplPrp['name'] == self._propertyNotes:
                self._propertyNotesGuid = tplPrp['guid']
                return

    def _r_make_sections_deleted_in_aeon_unused(self, narrativeEvents):
        for scId in self.novel.sections:
            if scId in narrativeEvents:
                continue

            if self.novel.sections[scId].scType == 0:
                self.novel.sections[scId].scType = 1

    def _r_put_new_sections_into_new_chapter(self, scIdsByDate):
        sectionsInChapters = []
        # List all sections already assigned to a chapter.
        for chId in self.novel.tree.get_children(CH_ROOT):
            sectionsInChapters.extend(self.novel.tree.get_children(chId))

        # Create a chapter for new sections.
        newChapterId = create_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
        newChapter = Chapter(title=_('New sections'), chType=0)
        # Sort sections by date/time, then put the orphaned ones into the new chapter.
        srtSections = sorted(scIdsByDate.items())
        for __, scList in srtSections:
            for scId in scList:
                if not scId in sectionsInChapters:
                    if not newChapterId in self.novel.tree.get_children(CH_ROOT):
                        self.novel.chapters[newChapterId] = newChapter
                        self.novel.tree.append(CH_ROOT, newChapterId)
                    self.novel.tree.append(newChapterId, scId)

    def _r_update_or_create_sections(self, targetScIdsByTitle, crIdsByGuid, lcIdsByGuid, itIdsByGuid, acIdsByGuid):
        scIdsByDate = {}
        scnTitles = []
        narrativeEvents = []
        for event in self._jsonData['events']:

            # Find out whether the event is associated to a section:
            isNarrative = False
            for evtRel in event['relationships']:
                if evtRel['role'] == self._roleArcGuid:
                    if evtRel['entity'] == self._entityNarrativeGuid:
                        isNarrative = True
                        break

            # Check whether the section title is unique.
            eventTitle = event['title'].strip()
            if eventTitle in scnTitles:
                raise Error(f'Ambiguous Aeon event title "{event["title"]}".')

            scnTitles.append(eventTitle)

            # Check whether there is already a section for the event.
            if eventTitle in targetScIdsByTitle:
                scId = targetScIdsByTitle[eventTitle]
            elif isNarrative:
                # Create a new section.
                scId = create_id(self.novel.sections, prefix=SECTION_PREFIX)
                self.novel.sections[scId] = Section(
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

            #--- Evaluate properties.
            hasDescription = False
            hasNotes = False
            for evtVal in event['values']:

                # Get section description.
                if evtVal['property'] == self._propertyDescGuid:
                    hasDescription = True
                    if evtVal['value']:
                        self.novel.sections[scId].desc = evtVal['value']

                # Get section notes.
                elif evtVal['property'] == self._propertyNotesGuid:
                    hasNotes = True
                    if evtVal['value']:
                        self.novel.sections[scId].notes = evtVal['value']

            #--- Add description and section notes, if missing.
            if not hasDescription:
                event['values'].append({'property': self._propertyDescGuid, 'value': ''})
            if not hasNotes:
                event['values'].append({'property': self._propertyNotesGuid, 'value': ''})

            #--- Get section tags.
            if event['tags']:
                self.novel.sections[scId].tags = []
                for evtTag in event['tags']:
                    self.novel.sections[scId].tags.append(evtTag)

            #--- Get date/time/duration
            timestamp = 0
            for evtRgv in event['rangeValues']:
                if evtRgv['rangeProperty'] == self._tplDateGuid:
                    timestamp = evtRgv['position']['timestamp']
                    if timestamp >= self.DATE_LIMIT:
                        # Restrict date/time calculation to dates within novelibre's range
                        sectionStart = datetime.min + timedelta(seconds=timestamp)
                        startDateTime = sectionStart.isoformat().split('T')

                        # Has the source an unspecific date?
                        if self.novel.sections[scId].day is not None:
                            # Convert date to day.
                            sectionDelta = sectionStart - self.referenceDate
                            self.novel.sections[scId].day = str(sectionDelta.days)
                        elif (self.novel.sections[scId].time is not None) and (self.novel.sections[scId].date is None):
                            # Use the default date.
                            self.novel.sections[scId].day = '0'
                        else:
                            self.novel.sections[scId].date = startDateTime[0]
                        self.novel.sections[scId].time = startDateTime[1]

                        # Calculate duration
                        if 'years' in evtRgv['span'] or 'months' in evtRgv['span']:
                            endYear = sectionStart.year
                            endMonth = sectionStart.month
                            if 'years' in evtRgv['span']:
                                endYear += evtRgv['span']['years']
                            if 'months' in evtRgv['span']:
                                endMonth += evtRgv['span']['months']
                                while endMonth > 12:
                                    endMonth -= 12
                                    endYear += 1
                            sectionEnd = datetime(endYear, endMonth, sectionStart.day)
                            sectionDuration = sectionEnd - datetime(sectionStart.year, sectionStart.month, sectionStart.day)
                            lastsDays = sectionDuration.days
                            lastsHours = sectionDuration.seconds // 3600
                            lastsMinutes = (sectionDuration.seconds % 3600) // 60
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
                        self.novel.sections[scId].lastsDays = str(lastsDays)
                        self.novel.sections[scId].lastsHours = str(lastsHours)
                        self.novel.sections[scId].lastsMinutes = str(lastsMinutes)
                    break

            # Use the timestamp for chronological sorting.
            if not timestamp in scIdsByDate:
                scIdsByDate[timestamp] = []
            scIdsByDate[timestamp].append(scId)

            #--- Find sections and get characters, locations, items, and arcs.
            self.novel.sections[scId].scType = 1
            # type = "Unused"
            scCharacters = []
            scLocations = []
            scItems = []
            for evtRel in event['relationships']:

                # Make the section "Normal", if the event has a "Narrative" relationship.
                if evtRel['role'] == self._roleArcGuid:
                    if evtRel['entity'] == self._entityNarrativeGuid:
                        self.novel.sections[scId].scType = 0
                        if timestamp > self._timestampMax:
                            self._timestampMax = timestamp

                # Add character to the list, if the event has a character role relationship.
                elif evtRel['role'] == self._roleCharacterGuid:
                    crId = crIdsByGuid[evtRel['entity']]
                    scCharacters.append(crId)

                # Add location to the list, if the event has a location role relationship.
                elif evtRel['role'] == self._roleLocationGuid:
                    lcId = lcIdsByGuid[evtRel['entity']]
                    scLocations.append(lcId)

                # Add item to the list, if the event has an item role relationship.
                elif evtRel['role'] == self._roleItemGuid:
                    itId = itIdsByGuid[evtRel['entity']]
                    scItems.append(itId)

                # Add arc assignment to the section, if the event has a "Storyline" relationship.
                elif evtRel['role'] == self._roleStorylineGuid:
                    acId = acIdsByGuid[evtRel['entity']]
                    self.novel.sections[scId].scPlotLines.append(acId)
                    # adding arc reference to the section

                    # Add section reference to the arc.
                    acSections = self.novel.plotLines[acId].sections
                    if acSections is None:
                        acSections = []
                    acSections.append(scId)
                    self.novel.plotLines[acId].sections = acSections

            # Write the character/location/item lists to the section.
            if scCharacters:
                self.novel.sections[scId].characters = scCharacters
            if scLocations:
                self.novel.sections[scId].locations = scLocations
            if scItems:
                self.novel.sections[scId].items = scItems
        return narrativeEvents, scIdsByDate

    def _set_reference_date(self):
        self.referenceDate = datetime.today()
        if self.novel.referenceDate:
            defaultDateTime = f'{self.novel.referenceDate} 00:00:00'
            try:
                self.referenceDate = datetime.fromisoformat(defaultDateTime)
            except ValueError:
                pass

    def _w_check_source_arcs(self, source, relatedArcs):
        """Ignore elements that are not related to a section."""
        srcArcTitles = []
        for acId in source.plotLines:
            if not acId in relatedArcs:
                continue

            if source.plotLines[acId].title in srcArcTitles:
                raise Error(_('Ambiguous novelibre arc "{}".').format(source.plotLines[acId].title))

            srcArcTitles.append(source.plotLines[acId].title)

    def _w_check_source_characters(self, source, relatedCharacters):
        """Ignore elements that are not related to a section."""
        srcChrNames = []
        for crId in source.characters:
            if not crId in relatedCharacters:
                continue

            if source.characters[crId].title in srcChrNames:
                raise Error(_('Ambiguous novelibre character "{}".').format(source.characters[crId].title))

            srcChrNames.append(source.characters[crId].title)

    def _w_check_source_locations(self, source, relatedLocations):
        """Ignore elements that are not related to a section."""
        srcLocTitles = []
        for lcId in source.locations:
            if not lcId in relatedLocations:
                continue

            if source.locations[lcId].title in srcLocTitles:
                raise Error(_('Ambiguous novelibre location "{}".').format(source.locations[lcId].title))

            srcLocTitles.append(source.locations[lcId].title)

    def _w_check_source_items(self, source, relatedItems):
        """Ignore elements that are not related to a section."""
        srcItmTitles = []
        for itId in source.items:
            if not itId in relatedItems:
                continue

            if source.items[itId].title in srcItmTitles:
                raise Error(_('Ambiguous novelibre item "{}".').format(source.items[itId].title))

            srcItmTitles.append(source.items[itId].title)

    def _w_check_source_sections(self, source):
        srcScnTitles = []
        for chId in source.chapters:
            if source.chapters[chId].isTrash:
                continue

            for scId in source.tree.get_children(chId):
                if source.sections[scId].title in srcScnTitles:
                    raise Error(_('Ambiguous novelibre section title "{}".').format(source.sections[scId].title))

                srcScnTitles.append(source.sections[scId].title)
        return srcScnTitles

    def _w_check_target_arcs(self):
        acIdsByTitle = {}
        for acId in self.novel.plotLines:
            if self.novel.plotLines[acId].title in acIdsByTitle:
                raise Error(_('Ambiguous Aeon arc "{}".').format(self.novel.plotLines[acId].title))

            acIdsByTitle[self.novel.plotLines[acId].title] = acId
        return acIdsByTitle

    def _w_check_target_characters(self):
        crIdsByTitle = {}
        for crId in self.novel.characters:
            if self.novel.characters[crId].title in crIdsByTitle:
                raise Error(_('Ambiguous Aeon character "{}".').format(self.novel.characters[crId].title))

            crIdsByTitle[self.novel.characters[crId].title] = crId
        return crIdsByTitle

    def _w_check_target_items(self):
        itIdsByTitle = {}
        for itId in self.novel.items:
            if self.novel.items[itId].title in itIdsByTitle:
                raise Error(_('Ambiguous Aeon item "{}".').format(self.novel.items[itId].title))

            itIdsByTitle[self.novel.items[itId].title] = itId
        return itIdsByTitle

    def _w_check_target_locations(self):
        lcIdsByTitle = {}
        for lcId in self.novel.locations:
            if self.novel.locations[lcId].title in lcIdsByTitle:
                raise Error(_('Ambiguous Aeon location "{}".').format(self.novel.locations[lcId].title))

            lcIdsByTitle[self.novel.locations[lcId].title] = lcId
        return lcIdsByTitle

    def _w_check_target_sections(self):
        scIdsByTitle = {}
        for scId in self.novel.sections:
            if self.novel.sections[scId].title in scIdsByTitle:

                raise Error(_('Ambiguous Aeon event title "{}".').format(self.novel.sections[scId].title))
            scIdsByTitle[self.novel.sections[scId].title] = scId
        return scIdsByTitle

    def _w_collect_trashed_sections(self, srcScnTitles):
        """List non-section events."""
        for scId in self.novel.sections:
            if self.novel.sections[scId].title in srcScnTitles:
                continue

            if self.novel.sections[scId].scType == 1:
                continue

            self._trashEvents.append(scId)

    def _w_create_json_narrative_arc_if_missing(self):
        if self._entityNarrativeGuid is not None:
            return

        self._entityNarrativeGuid = get_uid('entityNarrativeGuid')
        self._jsonData['entities'].append({
                'entityType':self._typeArcGuid,
                'guid':self._entityNarrativeGuid,
                'icon':'book',
                'name':self._entityNarrative,
                'notes':'',
                'sortOrder':self._arcCount,
                'swatchColor':'orange'})
        self._arcCount += 1

    def _w_create_json_property_desc_if_missing(self):
        if self._propertyDescGuid is not None:
            return

            n = len(self._jsonData['template']['properties'])
            self._propertyDescGuid = get_uid('_propertyDescGuid')
            self._jsonData['template']['properties'].append({'calcMode':'default',
                    'calculate':False,
                    'fadeEvents':False,
                    'guid':self._propertyDescGuid,
                    'icon':'tag',
                    'isMandatory':False,
                    'name':self._propertyDesc,
                    'sortOrder':n,
                    'type':'multitext'})

    def _w_create_json_property_moonphase_if_missing(self):
        if self._propertyMoonphaseGuid is not None:
            return

        if not self._addMoonphase:
            return

        n = len(self._jsonData['template']['properties'])
        self._propertyMoonphaseGuid = get_uid('_propertyMoonphaseGuid')
        self._jsonData['template']['properties'].append({'calcMode':'default',
                'calculate':False,
                'fadeEvents':False,
                'guid':self._propertyMoonphaseGuid,
                'icon':'flag',
                'isMandatory':False,
                'name':self._propertyMoonphase,
                'sortOrder':n,
                'type':'text'})

    def _w_create_json_property_notes_if_missing(self):
        if self._propertyNotesGuid is not None:
            return

        for tplPrp in self._jsonData['template']['properties']:
            tplPrp['sortOrder'] += 1

        self._propertyNotesGuid = get_uid('_propertyNotesGuid')
        self._jsonData['template']['properties'].insert(0, {'calcMode':'default',
                'calculate':False,
                'fadeEvents':False,
                'guid':self._propertyNotesGuid,
                'icon':'tag',
                'isMandatory':False,
                'name':self._propertyNotes,
                'sortOrder':0,
                'type':'multitext'})

    def _w_create_json_role_arc_if_missing(self):
        if self._roleArcGuid is not None:
            return

        for entityType in self._jsonData['template']['types']:
            if entityType['name'] == 'Arc':
                self._roleArcGuid = get_uid('_roleArcGuid')
                entityType['roles'].append(
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleArcGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':'Arc',
                        'sortOrder':0})
                return

    def _w_create_json_role_storyline_if_missing(self):
        if self._roleStorylineGuid is not None:
            return

        for entityType in self._jsonData['template']['types']:
            if entityType['name'] == 'Arc':
                self._roleStorylineGuid = get_uid('_roleStorylineGuid')
                entityType['roles'].append(
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleStorylineGuid,
                        'icon':'circle filled text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':'Storyline',
                        'sortOrder':0})
                return

    def _w_create_json_type_arc_if_missing(self):
        if self._typeArcGuid is not None:
            return

        self._typeArcGuid = get_uid('typeArcGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append({
                'color':'iconYellow',
                'guid':self._typeArcGuid,
                'icon':'book',
                'name':'Arc',
                'persistent':True,
                'roles':[],
                'sortOrder':typeCount})

    def _w_create_json_type_character_if_missing(self):
        if self._typeCharacterGuid is not None:
            return

        self._typeCharacterGuid = get_uid('_typeCharacterGuid')
        self._roleCharacterGuid = get_uid('_roleCharacterGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append({
                'color':'iconRed',
                'guid':self._typeCharacterGuid,
                'icon':'person',
                'name':self._typeCharacter,
                'persistent':False,
                'roles':[
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleCharacterGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._roleCharacter,
                        'sortOrder':0}],
                'sortOrder':typeCount})

    def _w_create_json_type_item_if_missing(self):
        if self._typeItemGuid is not None:
            return

        self._typeItemGuid = get_uid('_typeItemGuid')
        self._roleItemGuid = get_uid('_roleItemGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append({
                'color':'iconPurple',
                'guid':self._typeItemGuid,
                'icon':'cube',
                'name':self._typeItem,
                'persistent':True,
                'roles':[
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleItemGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._roleItem,
                        'sortOrder':0}],
                'sortOrder':typeCount})

    def _w_create_json_type_location_if_missing(self):
        if self._typeLocationGuid is not None:
            return

        self._typeLocationGuid = get_uid('_typeLocationGuid')
        self._roleLocationGuid = get_uid('_roleLocationGuid')
        typeCount = len(self._jsonData['template']['types'])
        self._jsonData['template']['types'].append({
                'color':'iconOrange',
                'guid':self._typeLocationGuid,
                'icon':'map',
                'name':self._typeLocation,
                'persistent':True,
                'roles':[
                    {
                        'allowsMultipleForEntity':True,
                        'allowsMultipleForEvent':True,
                        'allowsPercentAllocated':False,
                        'guid':self._roleLocationGuid,
                        'icon':'circle text',
                        'mandatoryForEntity':False,
                        'mandatoryForEvent':False,
                        'name':self._roleLocation,
                        'sortOrder':0}],
                'sortOrder':typeCount})

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
        """Return the character's birth or death date, if any."""
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
        """Create a new event from a section."""
        event = {
            'attachments': [],
            'color': '',
            'displayId': self._w_get_display_id(),
            'guid': get_uid(f'section{section.title}'),
            'links': [],
            'locked': False,
            'priority': 500,
            'rangeValues': [{
                'minimumZoom':-1,
                'position': {
                    'precision': 'minute',
                    'timestamp': self.DATE_LIMIT
                    },
                'rangeProperty': self._tplDateGuid,
                'span': {},
                }],
            'relationships': [],
            'tags': [],
            'title': section.title,
            'values': [{
                'property': self._propertyNotesGuid,
                'value': ''
                },
                {
                'property': self._propertyDescGuid,
                'value': ''
                }],
            }
        if section.scType == 0:
            event['color'] = self._colors[self._sectionColor]
        else:
            event['color'] = self._colors[self._eventColor]
        return event

    def _w_get_related_elements(self, source):
        """Return lists of characters, locations, items, and arcs assigned to sections."""
        relatedCharacters = []
        relatedLocations = []
        relatedItems = []
        relatedArcs = []
        for chId in source.chapters:
            if source.chapters[chId].isTrash:
                continue

            for scId in source.tree.get_children(chId):
                if source.sections[scId].characters:
                    relatedCharacters = list(set(relatedCharacters + source.sections[scId].characters))
                if source.sections[scId].locations:
                    relatedLocations = list(set(relatedLocations + source.sections[scId].locations))
                if source.sections[scId].items:
                    relatedItems = list(set(relatedItems + source.sections[scId].items))
                if source.sections[scId].scPlotLines:
                    relatedArcs = list(set(relatedArcs + source.sections[scId].scPlotLines))
        return relatedCharacters, relatedLocations, relatedItems, relatedArcs

    def _w_get_span(self, section):
        """Return a time span dictionary from the section duration.
        
        Positional arguments:
            section -- Section instance
        """
        span = {}
        if section.lastsDays:
            span['days'] = int(section.lastsDays)
        if section.lastsHours:
            span['hours'] = int(section.lastsHours)
        if section.lastsMinutes:
            span['minutes'] = int(section.lastsMinutes)
        return span

    def _w_get_timestamp(self, section):
        """Return a timestamp integer from the section date.
        
        Positional arguments:
            section -- Section instance
        """
        self._timestampMax += 1
        timestamp = int(self._timestampMax)
        try:
            if section.date:
                isoDt = section.date
                if section.time:
                    isoDt = (f'{isoDt} {section.time}')
            timestamp = int((datetime.fromisoformat(isoDt) - datetime.min).total_seconds())
        except:
            pass
        return timestamp

    def _w_update_arcs_from_source(self, source, acIdsByTitle, linkedArcs):
        arcCount = len(self.novel.plotLines)
        acIdsBySrcId = {}
        for srcAcId in source.plotLines:
            if source.plotLines[srcAcId].title in acIdsByTitle:
                acIdsBySrcId[srcAcId] = acIdsByTitle[source.plotLines[srcAcId].title]
            elif srcAcId in linkedArcs:

                #--- Create a new Arc if it is assigned to at least one section.
                acId = create_id(self.novel.plotLines, prefix=PLOT_LINE_PREFIX)
                acIdsBySrcId[srcAcId] = acId
                self.novel.plotLines[acId] = source.plotLines[srcAcId]
                arcName = self.novel.plotLines[acId].title
                newGuid = get_uid(f'{acId}{arcName}')
                self._arcGuidsById[acId] = newGuid
                self._jsonData['entities'].append(
                    {
                        'entityType':self._typeArcGuid,
                        'guid':newGuid,
                        'icon':'book',
                        'name':arcName,
                        'notes':'',
                        'sortOrder':self._arcCount,
                        'swatchColor':'orange'})
                arcCount += 1
        return acIdsBySrcId

    def _w_update_characters_from_source(self, source, crIdsByTitle, linkedCharacters):
        chrCount = len(self.novel.characters)
        crIdsBySrcId = {}
        srcIdsbyCrId = {}
        for srcCrId in source.characters:
            if source.characters[srcCrId].title in crIdsByTitle:
                crId = crIdsByTitle[source.characters[srcCrId].title]
                crIdsBySrcId[srcCrId] = crId
                srcIdsbyCrId[crId] = srcCrId
            elif srcCrId in linkedCharacters:

                #--- Create a new character if it is assigned to at least one section.
                crId = create_id(self.novel.characters, prefix=CHARACTER_PREFIX)
                crIdsBySrcId[srcCrId] = crId
                srcIdsbyCrId[crId] = srcCrId
                self.novel.characters[crId] = source.characters[srcCrId]
                newGuid = get_uid(f'{crId}{self.novel.characters[crId].title}')
                self._characterGuidsById[crId] = newGuid
                jsonCharacter = {}
                birthDate = self.novel.characters[crId].birthDate
                if birthDate:
                    jsonCharacter['createRangePosition'] = self._w_get_json_character_date(birthDate)
                deathDate = self.novel.characters[crId].deathDate
                if deathDate:
                    jsonCharacter['destroyRangePosition'] = self._w_get_json_character_date(deathDate)
                jsonCharacter['entityType'] = self._typeCharacterGuid
                jsonCharacter['guid'] = newGuid
                jsonCharacter['icon'] = 'person'
                jsonCharacter['name'] = self.novel.characters[crId].title
                jsonCharacter['notes'] = ''
                jsonCharacter['sortOrder'] = chrCount
                jsonCharacter['swatchColor'] = 'darkPink'
                self._jsonData['entities'].append(jsonCharacter)
                chrCount += 1

        # Update birth/death date.
        for entity in self._jsonData['entities']:
            if not entity['entityType'] == self._typeCharacterGuid:
                continue

            if not entity['name'] in crIdsByTitle:
                continue

            # entity is a character.
            crId = crIdsByTitle[entity['name']]
            srcCrId = srcIdsbyCrId[crId]
            birthDate = source.characters[srcCrId].birthDate
            if birthDate:
                entity['createRangePosition'] = self._w_get_json_character_date(birthDate)
            elif 'createRangePosition' in entity:
                    del entity['createRangePosition']
            deathDate = source.characters[srcCrId].deathDate
            if deathDate:
                entity['destroyRangePosition'] = self._w_get_json_character_date(deathDate)
            elif 'destroyRangePosition' in entity:
                    del entity['destroyRangePosition']

        return crIdsBySrcId

    def _w_update_json_events_from_sections(self, scIdsByTitle):
        for jEvent in self._jsonData['events']:
            if not jEvent['title'] in scIdsByTitle:
                continue

            scId = scIdsByTitle[jEvent['title']]

            #--- Set event date/time/span.
            if jEvent['rangeValues'][0]['position']['timestamp'] >= self.DATE_LIMIT:
                jEvent['rangeValues'][0]['span'] = self._w_get_span(self.novel.sections[scId])
                jEvent['rangeValues'][0]['position']['timestamp'] = self._w_get_timestamp(self.novel.sections[scId])

            #--- Calculate moon phase.
            if self._propertyMoonphaseGuid is not None:
                eventMoonphase = get_moon_phase_plus(self.novel.sections[scId].date)
            else:
                eventMoonphase = ''

            #--- Set section description, notes, and moon phase.
            hasMoonphase = False
            for evtVal in jEvent['values']:

                # Set section description.
                if evtVal['property'] == self._propertyDescGuid:
                    if self.novel.sections[scId].desc:
                        evtVal['value'] = self.novel.sections[scId].desc

                # Set section notes.
                elif evtVal['property'] == self._propertyNotesGuid:
                    if self.novel.sections[scId].notes:
                        evtVal['value'] = self.novel.sections[scId].notes

                # Set moon phase.
                elif evtVal['property'] == self._propertyMoonphaseGuid:
                        evtVal['value'] = eventMoonphase
                        hasMoonphase = True

            #--- Add missing event properties.
            if not hasMoonphase and self._propertyMoonphaseGuid is not None:
                jEvent['values'].append({'property': self._propertyMoonphaseGuid, 'value': eventMoonphase})

            #--- Set section tags.
            if self.novel.sections[scId].tags:
                jEvent['tags'] = self.novel.sections[scId].tags

            #--- Update characters, locations, items, and arcs.

            # Delete assignments.
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

            # Add characters.
            if self.novel.sections[scId].characters:
                for crId in self.novel.sections[scId].characters:
                    newRel.append(
                        {
                        'entity': self._characterGuidsById[crId],
                        'percentAllocated': 1,
                        'role': self._roleCharacterGuid,
                        })

            # Add locations.
            if self.novel.sections[scId].locations:
                for lcId in self.novel.sections[scId].locations:
                    newRel.append(
                        {
                        'entity': self._locationGuidsById[lcId],
                        'percentAllocated': 1,
                        'role': self._roleLocationGuid,
                        })

            # Add items.
            if self.novel.sections[scId].items:
                for itId in self.novel.sections[scId].items:
                    newRel.append(
                        {
                        'entity': self._itemGuidsById[itId],
                        'percentAllocated': 1,
                        'role': self._roleItemGuid,
                        })

            # Add arcs.
            if self.novel.sections[scId].scType == 0:
                # Add "Narrative" arc.
                newRel.append(
                    {
                    'entity': self._entityNarrativeGuid,
                    'percentAllocated': 1,
                    'role': self._roleArcGuid,
                    })

                # Add storyline arcs.
                if self.novel.sections[scId].scPlotLines:
                    for acId in self.novel.sections[scId].scPlotLines:
                        newRel.append(
                            {
                            'entity': self._arcGuidsById[acId],
                            'percentAllocated': 1,
                            'role': self._roleStorylineGuid,
                            })

            jEvent['relationships'] = newRel

    def _w_update_items_from_source(self, source, itIdsByTitle, linkedItems):
        itmCount = len(self.novel.items)
        itIdsBySrcId = {}
        for srcItId in source.items:
            if source.items[srcItId].title in itIdsByTitle:
                itIdsBySrcId[srcItId] = itIdsByTitle[source.items[srcItId].title]
            elif srcItId in linkedItems:

                #--- Create a new Item if it is assigned to at least one section.
                itId = create_id(self.novel.items, prefix=ITEM_PREFIX)
                itIdsBySrcId[srcItId] = itId
                self.novel.items[itId] = source.items[srcItId]
                newGuid = get_uid(f'{itId}{self.novel.items[itId].title}')
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

    def _w_update_locations_from_source(self, source, lcIdsByTitle, linkedLocations):
        locCount = len(self.novel.locations)
        lcIdsBySrcId = {}
        for srcLcId in source.locations:
            if source.locations[srcLcId].title in lcIdsByTitle:
                lcIdsBySrcId[srcLcId] = lcIdsByTitle[source.locations[srcLcId].title]
            elif srcLcId in linkedLocations:

                #--- Create a new location if it is assigned to at least one section.
                lcId = create_id(self.novel.locations, prefix=LOCATION_PREFIX)
                lcIdsBySrcId[srcLcId] = lcId
                self.novel.locations[lcId] = source.locations[srcLcId]
                newGuid = get_uid(f'{lcId}{self.novel.locations[lcId].title}')
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

    def _w_update_sections_from_source(self, source, scIdsByTitle, crIdsBySrcId, lcIdsBySrcId, itIdsBySrcId, acIdsBySrcId):
        for srcId in source.sections:
            if source.sections[srcId].scType != 0:
                # Remove unused section from the "Narrative" arc.
                if source.sections[srcId].title in scIdsByTitle:
                    scId = scIdsByTitle[source.sections[srcId].title]
                    self.novel.sections[scId].scType = 1
                continue

            if source.sections[srcId].title in scIdsByTitle:
                scId = scIdsByTitle[source.sections[srcId].title]
            else:
                #--- Create a new section.
                scId = create_id(self.novel.sections, prefix=SECTION_PREFIX)
                self.novel.sections[scId] = Section(
                    title=source.sections[srcId].title,
                    scType=source.sections[srcId].scType,
                    scene=source.sections[srcId].scene
                    )
                scIdsByTitle[self.novel.sections[scId].title] = scId
                newEvent = self._w_get_new_json_event(self.novel.sections[scId])
                self._jsonData['events'].append(newEvent)
            self.novel.sections[scId].status = source.sections[srcId].status

            #--- Update section type.
            if source.sections[srcId].scType is not None:
                self.novel.sections[scId].scType = source.sections[srcId].scType

            #--- Update section tags.
            if source.sections[srcId].tags is not None:
                self.novel.sections[scId].tags = source.sections[srcId].tags

            #--- Update section description.
            if source.sections[srcId].desc is not None:
                self.novel.sections[scId].desc = source.sections[srcId].desc

            #--- Update section characters.
            if source.sections[srcId].characters is not None:
                scCharacters = []
                for crId in source.sections[srcId].characters:
                    if crId in crIdsBySrcId:
                        scCharacters.append(crIdsBySrcId[crId])
                self.novel.sections[scId].characters = scCharacters

            #--- Update section locations.
            if source.sections[srcId].locations is not None:
                scLocations = []
                for lcId in source.sections[srcId].locations:
                    if lcId in lcIdsBySrcId:
                        scLocations.append(lcIdsBySrcId[lcId])
                self.novel.sections[scId].locations = scLocations

            #--- Update section items.
            if source.sections[srcId].items is not None:
                scItems = []
                for itId in source.sections[srcId].items:
                    if itId in itIdsBySrcId:
                        scItems.append(itIdsBySrcId[itId])
                self.novel.sections[scId].items = scItems

            #--- Update section arcs.
            if source.sections[srcId].scPlotLines is not None:
                scArcs = []
                for acId in source.sections[srcId].scPlotLines:
                    if acId in acIdsBySrcId:
                        scArcs.append(acIdsBySrcId[acId])
                self.novel.sections[scId].scPlotLines = scArcs

            #--- Update section start date/time.
            if source.sections[srcId].time is not None:
                self.novel.sections[scId].time = source.sections[srcId].time

            #--- Calculate event date from unspecific section date, if any:
            if source.sections[srcId].day is not None:
                dayInt = int(source.sections[srcId].day)
                sectionDelta = timedelta(days=dayInt)
                self.novel.sections[scId].date = (self.referenceDate + sectionDelta).isoformat().split('T')[0]
            elif (source.sections[srcId].date is None) and (source.sections[srcId].time is not None):
                self.novel.sections[scId].date = self.referenceDate.isoformat().split('T')[0]
            else:
                self.novel.sections[scId].date = source.sections[srcId].date

            #--- Update section duration.
            if source.sections[srcId].lastsMinutes is not None:
                self.novel.sections[scId].lastsMinutes = source.sections[srcId].lastsMinutes
            if source.sections[srcId].lastsHours is not None:
                self.novel.sections[scId].lastsHours = source.sections[srcId].lastsHours
            if source.sections[srcId].lastsDays is not None:
                self.novel.sections[scId].lastsDays = source.sections[srcId].lastsDays

