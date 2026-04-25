import json
import logging
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class SectionStatus(str, Enum):
    notStarted = "notStarted"
    inProgress = "inProgress"
    complete = "complete"
    stale = "stale"
    hasWarnings = "hasWarnings"


@dataclass
class AudienceState:
    purpose: Optional[str] = None
    copyCount: Optional[int] = None
    ageGroup: Optional[str] = None
    eyesightConsideration: Optional[str] = None
    readingContext: Optional[str] = None
    literacyLevel: Optional[str] = None
    distributionModel: Optional[str] = None
    budgetLevel: Optional[str] = None


@dataclass
class ProductionState:
    method: Optional[str] = None
    podProvider: Optional[str] = None


@dataclass
class TrimBindingState:
    trimSize: Optional[str] = None
    bindingType: Optional[str] = None
    paperType: Optional[str] = None


@dataclass
class ContentState:
    scope: Optional[str] = None
    selectedBooks: List[str] = field(default_factory=list)
    isDiglot: bool = False
    isTriglot: bool = False
    secondaryProject: Optional[str] = None
    tertiaryProject: Optional[str] = None
    includeUnchecked: bool = False


@dataclass
class PeripheralsState:
    selected: List[str] = field(default_factory=list)


@dataclass
class LayoutState:
    columns: Optional[int] = None
    bodyFontSize: Optional[float] = None
    bodyLeading: Optional[float] = None
    bodyFont: Optional[str] = None
    marginPreset: Optional[str] = None


@dataclass
class WizardState:
    schemaVersion: int = 1
    recipeId: Optional[str] = None
    audience: AudienceState = field(default_factory=AudienceState)
    production: ProductionState = field(default_factory=ProductionState)
    trimBinding: TrimBindingState = field(default_factory=TrimBindingState)
    content: ContentState = field(default_factory=ContentState)
    peripherals: PeripheralsState = field(default_factory=PeripheralsState)
    layout: LayoutState = field(default_factory=LayoutState)
    sectionStatus: Dict[str, str] = field(default_factory=dict)

    def getFlat(self) -> Dict[str, Any]:
        """Return a flat dotted-key dict for rule evaluation."""
        result = {}
        for section, obj in [
            ("audience", self.audience),
            ("production", self.production),
            ("trimBinding", self.trimBinding),
            ("content", self.content),
            ("layout", self.layout),
        ]:
            for k, v in vars(obj).items():
                if v is not None:
                    result[f"{section}.{k}"] = v
        return result

    def toDict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def fromDict(cls, d: Dict[str, Any]) -> "WizardState":
        try:
            state = cls()
            state.schemaVersion = d.get("schemaVersion", 1)
            state.recipeId = d.get("recipeId")
            state.sectionStatus = d.get("sectionStatus", {})

            aud = d.get("audience", {})
            state.audience = AudienceState(**{k: v for k, v in aud.items()
                                              if k in AudienceState.__dataclass_fields__})

            prod = d.get("production", {})
            state.production = ProductionState(**{k: v for k, v in prod.items()
                                                  if k in ProductionState.__dataclass_fields__})

            trim = d.get("trimBinding", {})
            state.trimBinding = TrimBindingState(**{k: v for k, v in trim.items()
                                                    if k in TrimBindingState.__dataclass_fields__})

            cont = d.get("content", {})
            state.content = ContentState(**{k: v for k, v in cont.items()
                                            if k in ContentState.__dataclass_fields__})

            peri = d.get("peripherals", {})
            state.peripherals = PeripheralsState(**{k: v for k, v in peri.items()
                                                    if k in PeripheralsState.__dataclass_fields__})

            lay = d.get("layout", {})
            state.layout = LayoutState(**{k: v for k, v in lay.items()
                                          if k in LayoutState.__dataclass_fields__})
            return state
        except Exception as e:
            logger.error(f"Failed to deserialise WizardState: {e}")
            return cls()

    def saveToFile(self, path: str) -> None:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.toDict(), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save wizard state to {path}: {e}")

    @classmethod
    def loadFromFile(cls, path: str) -> Optional["WizardState"]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return cls.fromDict(json.load(f))
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Failed to load wizard state from {path}: {e}")
            return None
