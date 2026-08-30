# Copyright (c) 2026 Martial Systems LLC


class GateError(RuntimeError):
    """Stage hard gate failed."""


class ClaimBanError(GateError):
    """Report text hit a banned claim."""


class FetchError(GateError):
    """GHCND SNOW or normals empty, or a refused substitute."""


class SplitError(GateError):
    """Temporal winter split leaked confirmation or shuffled rows."""


class FigureCapError(GateError):
    """This tree stops at two figures."""


class LeakError(GateError):
    """DJF weather appeared in the pre-season feature vector."""
