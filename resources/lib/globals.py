# -*- coding: utf-8 -*-
"""
    Copyright (C) 2017 Sebastian Golasch (plugin.video.netflix)
    Copyright (C) 2018 Caphm (original implementation module)
    Global addon constants

    SPDX-License-Identifier: MIT
    See LICENSES/MIT.md for more information.
"""
# Everything that is to be globally accessible must be defined in this module
# and initialized in GlobalVariables.init_globals.
# When reusing Kodi languageInvokers, only the code in the main module
# (addon.py or service.py) will be run every time the addon is called.
# All other code executed on module level will only be executed once, when
# the module is first imported on the first addon invocation.
from __future__ import absolute_import, division, unicode_literals

import collections
import os
import sys

try:  # Python 3
    from urllib.parse import parse_qsl, unquote, urlparse
except ImportError:  # Python 2
    from urllib2 import unquote
    from urlparse import parse_qsl, urlparse

from future.utils import iteritems

import xbmc
import xbmcaddon

try:  # Python 2
    unicode
except NameError:  # Python 3
    unicode = str  # pylint: disable=redefined-builtin,invalid-name


class GlobalVariables(object):
    """Encapsulation for global variables to work around quirks with
    Kodi's reuseLanguageInvoker behavior"""
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=invalid-name, too-many-instance-attributes

    # Values in the variables VIEW_* stand for a partial menu id,
    # contained in the settings xml, example 'profiles' stand for id 'viewmodeprofiles'
    VIEW_PROFILES = 'profiles'
    VIEW_MAINMENU = 'mainmenu'
    VIEW_MYLIST = 'mylist'
    VIEW_FOLDER = 'folder'
    VIEW_MOVIE = 'movie'
    VIEW_SHOW = 'show'
    VIEW_SEASON = 'season'
    VIEW_EPISODE = 'episode'
    VIEW_SEARCH = 'search'
    VIEW_EXPORTED = 'exported'

    CONTENT_IMAGES = 'images'
    CONTENT_FOLDER = 'files'
    CONTENT_MOVIE = 'movies'
    CONTENT_SHOW = 'tvshows'
    CONTENT_SEASON = 'seasons'
    CONTENT_EPISODE = 'episodes'

    '''
    --Main Menu key infos--
    path                Passes information to the called method
                          generally structured as follows: [func. name, menu id, context id]
    loco_contexts       Contexts used to obtain the list of contents (use only one context when loco_known = True)
    loco_known          If True, keys label_id/description_id/icon are ignored, these values are obtained from LoCo list
    label_id            The ID for the menu title
    description_id      Description info text
    icon                Set a default image
    view                Override the default "partial menu id" of view
    content_type        Override the default content type (CONTENT_SHOW)
    has_show_setting    Means that the menu has the show/hide settings, by default is True
    has_sort_setting    Means that the menu has the sort settings, by default is False

    Explanation of function names in the 'path' key:
        video_list        Automatically gets the list_id by making a loco request,
                            the list_id search is made using the value specified on the loco_contexts key
        video_list_sorted To work must have a third argument on the path that is the context_id
                            or instead specified the key request_context_name
    '''
    MAIN_MENU_ITEMS = collections.OrderedDict([
        ('myList', {'path': ['video_list_sorted', 'myList'],
                    'loco_contexts': ['queue'],
                    'loco_known': True,
                    'request_context_name': 'mylist',
                    'view': VIEW_MYLIST,
                    'has_sort_setting': True}),
        ('continueWatching', {'path': ['video_list', 'continueWatching'],
                              'loco_contexts': ['continueWatching'],
                              'loco_known': True}),
        ('chosenForYou', {'path': ['video_list', 'chosenForYou'],
                          'loco_contexts': ['topTen'],
                          'loco_known': True}),
        ('recentlyAdded', {'path': ['video_list_sorted', 'recentlyAdded', '1592210'],
                           'loco_contexts': None,
                           'loco_known': False,
                           'request_context_name': 'genres',
                           'label_id': 30145,
                           'description_id': 30146,
                           'icon': 'DefaultRecentlyAddedMovies.png',
                           'has_sort_setting': True}),
        ('newRelease', {'path': ['video_list_sorted', 'newRelease'],
                        'loco_contexts': ['newRelease'],
                        'loco_known': True,
                        'request_context_name': 'newrelease',
                        'has_sort_setting': True}),
        ('currentTitles', {'path': ['video_list', 'currentTitles'],
                           'loco_contexts': ['trendingNow'],
                           'loco_known': True}),
        ('mostWatched', {'path': ['video_list', 'mostWatched'],  # Top 10 menu
                         'loco_contexts': ['mostWatched'],
                         'loco_known': True}),
        ('mostViewed', {'path': ['video_list', 'mostViewed'],
                        'loco_contexts': ['popularTitles'],
                        'loco_known': True}),
        ('netflixOriginals', {'path': ['video_list_sorted', 'netflixOriginals', '839338'],
                              'loco_contexts': ['netflixOriginals'],
                              'loco_known': True,
                              'request_context_name': 'genres',
                              'has_sort_setting': True}),
        ('assistiveAudio', {'path': ['video_list_sorted', 'assistiveAudio', 'None'],
                            'loco_contexts': None,
                            'loco_known': False,
                            'request_context_name': 'assistiveAudio',
                            'label_id': 30163,
                            'description_id': 30164,
                            'icon': 'DefaultTVShows.png',
                            'has_sort_setting': True}),
        ('recommendations', {'path': ['recommendations', 'recommendations'],
                             'loco_contexts': ['similars', 'becauseYouAdded', 'becauseYouLiked', 'watchAgain',
                                               'bigRow'],
                             'loco_known': False,
                             'label_id': 30001,
                             'description_id': 30094,
                             'icon': 'DefaultUser.png'}),
        ('tvshowsGenres', {'path': ['subgenres', 'tvshowsGenres', '83'],
                           'loco_contexts': None,
                           'loco_known': False,
                           'request_context_name': 'genres',  # Used for sub-menus
                           'label_id': 30174,
                           'description_id': None,
                           'icon': 'DefaultTVShows.png',
                           'has_sort_setting': True}),
        ('moviesGenres', {'path': ['subgenres', 'moviesGenres', '34399'],
                          'loco_contexts': None,
                          'loco_known': False,
                          'request_context_name': 'genres',  # Used for sub-menus
                          'label_id': 30175,
                          'description_id': None,
                          'icon': 'DefaultMovies.png',
                          'content_type': CONTENT_MOVIE,
                          'has_sort_setting': True}),
        # Todo: Disabled All tv shows/All movies loco menu due to website changes
        # ('tvshows', {'path': ['genres', 'tvshows', '83'],
        #              'loco_contexts': None,
        #              'loco_known': False,
        #              'request_context_name': 'genres',  # Used for sub-menus
        #              'label_id': 30095,
        #              'description_id': None,
        #              'icon': 'DefaultTVShows.png',
        #              'has_sort_setting': True}),
        # ('movies', {'path': ['genres', 'movies', '34399'],
        #             'loco_contexts': None,
        #             'loco_known': False,
        #             'request_context_name': 'genres',  # Used for sub-menus
        #             'label_id': 30096,
        #             'description_id': None,
        #             'icon': 'DefaultMovies.png',
        #             'content_type': CONTENT_MOVIE,
        #             'has_sort_setting': True}),
        ('genres', {'path': ['genres', 'genres'],
                    'loco_contexts': ['genre'],
                    'loco_known': False,
                    'request_context_name': 'genres',  # Used for sub-menus
                    'label_id': 30010,
                    'description_id': 30093,
                    'icon': 'DefaultGenre.png',
                    'has_sort_setting': True}),
        ('search', {'path': ['search', 'search'],
                    'loco_contexts': None,
                    'loco_known': False,
                    'label_id': 30400,
                    'description_id': 30092,
                    'icon': 'DefaultAddonsSearch.png',
                    'view': VIEW_SEARCH,
                    'has_sort_setting': True}),
        ('exported', {'path': ['exported', 'exported'],
                      'loco_contexts': None,
                      'loco_known': False,
                      'label_id': 30048,
                      'description_id': 30091,
                      'icon': 'DefaultHardDisk.png',
                      'view': VIEW_EXPORTED})
    ])

    MODE_DIRECTORY = 'directory'
    MODE_HUB = 'hub'
    MODE_ACTION = 'action'
    MODE_PLAY = 'play'
    MODE_PLAY_STRM = 'play_strm'
    MODE_LIBRARY = 'library'

    def __init__(self):
        """Do nothing on constructing the object"""
        # Define here any variables necessary for the correct loading of the modules
        self.IS_ADDON_FIRSTRUN = None
        self.ADDON = None
        self.ADDON_DATA_PATH = None
        self.DATA_PATH = None
        self.CACHE = None
        self.CACHE_MANAGEMENT = None
        self.CACHE_TTL = None
        self.CACHE_MYLIST_TTL = None
        self.CACHE_METADATA_TTL = None

    def init_globals(self, argv, reinitialize_database=False, reload_settings=False):
        """
        Initialized globally used module variables. Needs to be called at start of each plugin instance!
        This is an ugly hack because Kodi does not execute statements
        defined on module level if reusing a language invoker.
        """
        # IS_ADDON_FIRSTRUN specifies when the addon is at its first run (reuse language invoker is not yet used)
        self.IS_ADDON_FIRSTRUN = self.IS_ADDON_FIRSTRUN is None
        self.IS_ADDON_EXTERNAL_CALL = False
        self.PY_IS_VER2 = sys.version_info.major == 2
        self.ADDON = xbmcaddon.Addon()
        self.URL = urlparse(argv[0])
        self.REQUEST_PATH = g.py2_decode(unquote(self.URL[2][1:]))
        try:
            self.PARAM_STRING = argv[2][1:]
        except IndexError:
            self.PARAM_STRING = ''
        self.REQUEST_PARAMS = dict(parse_qsl(self.PARAM_STRING))
        if self.IS_ADDON_FIRSTRUN:
            self.ADDON_ID = self.py2_decode(self.ADDON.getAddonInfo('id'))
            self.PLUGIN = self.py2_decode(self.ADDON.getAddonInfo('name'))
            self.VERSION_RAW = self.py2_decode(self.ADDON.getAddonInfo('version'))
            self.VERSION = self.remove_ver_suffix(self.VERSION_RAW)
            self.ICON = self.py2_decode(self.ADDON.getAddonInfo('icon'))
            self.DEFAULT_FANART = self.py2_decode(self.ADDON.getAddonInfo('fanart'))
            self.ADDON_DATA_PATH = self.py2_decode(self.ADDON.getAddonInfo('path'))  # Add-on folder
            self.DATA_PATH = self.py2_decode(self.ADDON.getAddonInfo('profile'))  # Add-on user data folder
            self.CACHE_PATH = os.path.join(self.DATA_PATH, 'cache')
            self.COOKIE_PATH = os.path.join(self.DATA_PATH, 'COOKIE')
            try:
                self.PLUGIN_HANDLE = int(argv[1])
                self.IS_SERVICE = False
                self.BASE_URL = '{scheme}://{netloc}'.format(scheme=self.URL[0],
                                                             netloc=self.URL[1])
            except IndexError:
                self.PLUGIN_HANDLE = 0
                self.IS_SERVICE = True
                self.BASE_URL = '{scheme}://{netloc}'.format(scheme='plugin',
                                                             netloc=self.ADDON_ID)
        # Add absolute paths of embedded py modules to python system directory
        module_paths = [
            os.path.join(self.ADDON_DATA_PATH, 'modules', 'mysql-connector-python')
        ]
        # On PY2 sys.path list can contains values as unicode type and string type at same time,
        #   here we will add only unicode type so filter values by unicode.
        #   This fix comparing issues with use of "if path not in sys.path:"
        sys_path_filtered = [value for value in sys.path if isinstance(value, unicode)]

        for path in module_paths:  # module_paths has unicode type values
            path = g.py2_decode(xbmc.translatePath(path))
            if path not in sys_path_filtered:
                sys.path.insert(0, path)  # This add an unicode type

        self.reset_time_trace()
        self._init_database(self.IS_ADDON_FIRSTRUN or reinitialize_database)

        if self.IS_ADDON_FIRSTRUN or reload_settings:
            self.TIME_TRACE_ENABLED = self.ADDON.getSettingBool('enable_timing')
            self.IPC_OVER_HTTP = self.ADDON.getSettingBool('enable_ipc_over_http')
            # Initialize the cache
            self.CACHE_TTL = self.ADDON.getSettingInt('cache_ttl') * 60
            self.CACHE_MYLIST_TTL = self.ADDON.getSettingInt('cache_mylist_ttl') * 60
            self.CACHE_METADATA_TTL = self.ADDON.getSettingInt('cache_metadata_ttl') * 24 * 60 * 60
            if self.IS_SERVICE:
                from resources.lib.services.cache.cache_management import CacheManagement
                self.CACHE_MANAGEMENT = CacheManagement()
            from resources.lib.common.cache import Cache
            self.CACHE = Cache()
            from resources.lib.common.kodi_ops import GetKodiVersion
            self.KODI_VERSION = GetKodiVersion()
        self.settings_monitor_suspend(False)  # Reset the value in case of addon crash

    def _init_database(self, initialize):
        # Initialize local database
        if initialize:
            import resources.lib.database.db_local as db_local
            self.LOCAL_DB = db_local.NFLocalDatabase()
        # Initialize shared database
        use_mysql = g.ADDON.getSettingBool('use_mysql')
        if initialize or use_mysql:
            import resources.lib.database.db_shared as db_shared
            from resources.lib.database.db_exceptions import MySQLConnectionError, MySQLError
            try:
                shared_db_class = db_shared.get_shareddb_class(use_mysql=use_mysql)
                self.SHARED_DB = shared_db_class()
            except (MySQLConnectionError, MySQLError) as exc:
                import resources.lib.kodi.ui as ui
                if isinstance(exc, MySQLError):
                    # There is a problem with the database
                    ui.show_addon_error_info(exc)
                # The MySQL database cannot be reached, fallback to local SQLite database
                # When this code is called from addon, is needed apply the change also in the
                # service, so disabling it run the SettingsMonitor
                self.ADDON.setSettingBool('use_mysql', False)
                ui.show_notification(self.ADDON.getLocalizedString(30206), time=10000)
                shared_db_class = db_shared.get_shareddb_class()
                self.SHARED_DB = shared_db_class()

    def settings_monitor_suspend(self, is_suspended=True, at_first_change=False):
        """
        Suspends for the necessary time the settings monitor of the service
        that otherwise cause the reinitialization of global settings and possible consequent actions
        to settings changes or unnecessary checks when a setting will be changed.
        :param is_suspended: True/False - allows or denies the execution of the settings monitor
        :param at_first_change:
         True - monitor setting is automatically reactivated after the FIRST change to the settings
         False - monitor setting MUST BE REACTIVATED MANUALLY
        :return: None
        """
        if is_suspended and at_first_change:
            new_value = 'First'
        else:
            new_value = str(is_suspended)
        # Accepted values in string: First, True, False
        current_value = g.LOCAL_DB.get_value('suspend_settings_monitor', 'False')
        if new_value == current_value:
            return
        g.LOCAL_DB.set_value('suspend_settings_monitor', new_value)

    def settings_monitor_suspend_status(self):
        """
        Returns the suspend status of settings monitor
        """
        return g.LOCAL_DB.get_value('suspend_settings_monitor', 'False')

    def get_esn(self):
        """Get the generated esn or if set get the custom esn"""
        from resources.lib.database.db_utils import TABLE_SESSION
        custom_esn = g.ADDON.getSetting('esn')
        return custom_esn if custom_esn else g.LOCAL_DB.get_value('esn', '', table=TABLE_SESSION)

    def is_known_menu_context(self, context):
        """Return true if context are one of the menu with loco_known=True"""
        for menu_id, data in iteritems(self.MAIN_MENU_ITEMS):  # pylint: disable=unused-variable
            if data['loco_known']:
                if data['loco_contexts'][0] == context:
                    return True
        return False

    def flush_settings(self):
        """Reload the ADDON"""
        # pylint: disable=attribute-defined-outside-init
        self.ADDON = xbmcaddon.Addon()

    def reset_time_trace(self):
        """Reset current time trace info"""
        self.TIME_TRACE = []
        self.time_trace_level = -2

    def add_time_trace_level(self):
        """Add a level to the time trace"""
        self.time_trace_level += 2

    def remove_time_trace_level(self):
        """Remove a level from the time trace"""
        self.time_trace_level -= 2

    def py2_decode(self, value, encoding='utf-8'):
        """Decode text only on python 2"""
        # To remove when Kodi 18 support is over / Py2 dead
        if self.PY_IS_VER2:
            return value.decode(encoding)
        return value

    def py2_encode(self, value, encoding='utf-8'):
        """Encode text only on python 2"""
        # To remove when Kodi 18 support is over / Py2 dead
        if self.PY_IS_VER2:
            return value.encode(encoding)
        return value

    @staticmethod
    def remove_ver_suffix(version):
        """Remove the codename suffix from version value"""
        import re
        pattern = re.compile(r'\+\w+\.\d$')  # Example: +matrix.1
        return re.sub(pattern, '', version)


# pylint: disable=invalid-name
# This will have no effect most of the time, as it doesn't seem to be executed
# on subsequent addon invocations when reuseLanguageInvoker is being used.
# We initialize an empty instance so the instance is importable from run_addon.py
# and run_service.py, where g.init_globals(sys.argv) MUST be called before doing
# anything else (even BEFORE OTHER IMPORTS from this addon)
g = GlobalVariables()
