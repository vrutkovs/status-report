#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Comfortably generate reports - Local Snippets """

import os

from status_report.base import Stats, StatsGroup
from status_report.utils import Config, item, log, pretty


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Snippets Repository
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class SnippetRepo(object):
    """ Snippets repository reader """
    def __init__(self, path):
        """ Initialize the path. """
        self.path = path

    def snippets(self, user, options):
        """ List snippets for given user. """
        # Prepare the command
        log.info(u"Checking snippets in {0}".format(self.path))
        command = ''
        log.debug(pretty(command))

        return ['testing']


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Snippet Commits
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class SnippetCommits(Stats):
    """ Snippet commits """
    def __init__(self, option, name=None, parent=None, path=None):
        self.repo = SnippetRepo(path)
        Stats.__init__(self, option, name, parent)

    def fetch(self):
        self.stats = self.repo.snippets(self.user, self.options)

    def header(self):
        """ Show summary header. """
        item(
            "{0}: {1} snippet{2}".format(
                self.name, len(self.stats),
                "" if len(self.stats) == 1 else "s"),
            level=0, options=self.options)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Snippet Stats
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SnippetStats(StatsGroup):
    """ Snippet stats group """

    # Default order
    order = 300

    def __init__(self, option, name=None, parent=None):
        name = "Work on {0}".format(option)
        StatsGroup.__init__(self, option, name, parent)
        for repo, path in Config().section(option):
            if path.endswith('/*'):
                for repo_dir in sorted(os.listdir(path[:-1])):
                    repo_path = path.replace('*', repo_dir)
                    self.stats.append(SnippetCommits(
                        option="{0}-{1}".format(repo, repo_dir),
                        parent=self, path=repo_path,
                        name="Work on {0}/{1}".format(repo, repo_dir)))
            else:
                self.stats.append(SnippetCommits(
                    option=repo, parent=self, path=path,
                    name="Work on {0}".format(repo)))
