import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Text area (width_mm, height_mm) per trim size at standard margins
TRIM_TEXT_AREAS: Dict[str, tuple] = {
    "a4":         (155, 242),
    "a5":         (115, 182),
    "a6":         (88,  135),
    "letter":     (152, 228),
    "halfLetter": (106, 174),
    "fiveByEight": (92, 165),
    "sixByNine":  (117, 196),
    "sevenByTen": (142, 222),
}

# Margin preset multiplier on text area (tight < standard < generous)
MARGIN_SCALE: Dict[str, float] = {
    "tight":     1.08,
    "standard":  1.00,
    "generous":  0.88,
}

# Reference: ~300 words/page at 10pt leading 12pt on A5 single column
BASE_WORDS_PER_PAGE = 300.0
BASE_FONT_SIZE      = 10.0
BASE_LEADING_PT     = 12.0
BASE_TEXT_AREA      = TRIM_TEXT_AREAS["a5"]  # (115, 182)


class PageCountEstimator:

    def estimate(self, state, peripheralCatalogue: Optional[List] = None) -> int:
        """
        Estimate page count from WizardState.
        Returns an integer; documented as approximate ±15%.
        """
        # TODO(integrate): replace with real word count from PTXprint project
        totalWords = self._getWordCount(state)
        if totalWords <= 0:
            return 0

        trimSize   = (state.trimBinding.trimSize or "a5")
        fontSize   = (state.layout.bodyFontSize or BASE_FONT_SIZE)
        leading    = (state.layout.bodyLeading or (fontSize * 1.2))
        columns    = (state.layout.columns or 1)
        margin     = (state.layout.marginPreset or "standard")

        textW, textH = TRIM_TEXT_AREAS.get(trimSize, BASE_TEXT_AREA)
        marginScale  = MARGIN_SCALE.get(margin, 1.0)
        textW *= marginScale
        textH *= marginScale

        # Scale words-per-page by font size (quadratic — smaller font = more words)
        fontScale = (BASE_FONT_SIZE / fontSize) ** 2

        # Scale by text area relative to reference
        areaScale = (textW * textH) / (BASE_TEXT_AREA[0] * BASE_TEXT_AREA[1])

        # Columns: 2-col is ~1.8× more words per page (narrower hyphenation gain)
        columnScale = 1.0 if columns == 1 else 1.8

        wordsPerPage = BASE_WORDS_PER_PAGE * fontScale * areaScale * columnScale
        if wordsPerPage <= 0:
            wordsPerPage = 1.0

        bodyPages = int(totalWords / wordsPerPage) + 1

        peripheralPages = self._peripheralPages(state, peripheralCatalogue)

        return bodyPages + peripheralPages

    def _getWordCount(self, state) -> int:
        # TODO(integrate): call PTXprint's word-count function for state.content.selectedBooks
        # Fallback: rough heuristic by scope
        scope = state.content.scope or ""
        if scope == "wholeBible":
            return 789_000
        elif scope == "newTestament":
            return 180_000
        elif scope == "oldTestament":
            return 609_000
        elif scope in ("portion", "custom"):
            books = state.content.selectedBooks
            if books:
                return len(books) * 18_000  # rough avg words per book
            return 18_000
        return 180_000

    def _peripheralPages(self, state, catalogue: Optional[List]) -> int:
        selected = set(state.peripherals.selected)
        if not selected or not catalogue:
            return 0

        total = 0
        for category in catalogue:
            for item in category.get("items", []):
                itemId = item.get("id")
                if itemId not in selected:
                    continue
                if "estimatedPages" in item:
                    total += item["estimatedPages"]
                elif "estimatedPagesPerBook" in item:
                    books = state.content.selectedBooks
                    scope = state.content.scope or ""
                    if scope == "wholeBible":
                        bookCount = 66
                    elif scope == "newTestament":
                        bookCount = 27
                    elif scope == "oldTestament":
                        bookCount = 39
                    else:
                        bookCount = max(1, len(books))
                    total += item["estimatedPagesPerBook"] * bookCount
        return total

    def spineWidthMm(self, pageCount: int, paperType: Optional[str] = None) -> Optional[float]:
        """Estimate spine width in mm.  Returns None if not applicable."""
        # Approximate paper thickness by type (mm per sheet, i.e. per 2 pages)
        thicknessPerSheet = {
            "standard":    0.100,
            "cream":       0.105,
            "biblePaper28": 0.060,
            "biblePaper36": 0.075,
        }.get(paperType or "standard", 0.100)

        sheets = pageCount / 2.0
        return round(sheets * thicknessPerSheet, 1)
