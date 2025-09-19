"""Custom exceptions for the music application."""


class MusicBoardApplicationError(Exception):
    """Base exception for music application errors."""
    pass


class SoundPlaybackError(MusicBoardApplicationError):
    """Exception raised when sound playback fails."""
    pass


class FontLoadError(MusicBoardApplicationError):
    """Exception raised when font loading fails."""
    pass


class InvalidNotePositionError(MusicBoardApplicationError):
    """Exception raised when note position is invalid."""
    pass