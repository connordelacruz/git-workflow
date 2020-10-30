"""Base class for workflow scripts."""
from abc import ABC, abstractmethod

class WorkflowBase(ABC):

    def __init__(self, repo, min_git_version_met):
        self.repo = repo
        self.min_git_version_met = min_git_version_met

    @abstractmethod
    def run(self):
        pass
