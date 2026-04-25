import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from .wizardState import WizardState

logger = logging.getLogger(__name__)


class RecipeLoader:

    def __init__(self, dataDir: Path):
        self._recipes: List[Dict] = []
        self._load(dataDir / "recipes")

    def _load(self, recipesDir: Path) -> None:
        if not recipesDir.is_dir():
            logger.error(f"Recipes directory not found: {recipesDir}")
            return
        for jsonFile in sorted(recipesDir.glob("*.json")):
            try:
                with open(jsonFile, "r", encoding="utf-8") as f:
                    recipe = json.load(f)
                self._recipes.append(recipe)
            except Exception as e:
                logger.error(f"Failed to load recipe {jsonFile.name}: {e}")

    def allRecipes(self) -> List[Dict]:
        return list(self._recipes)

    def getById(self, recipeId: str) -> Optional[Dict]:
        for r in self._recipes:
            if r.get("id") == recipeId:
                return r
        return None

    def applyRecipe(self, recipeId: str, state: WizardState) -> bool:
        """Apply recipe fields to state. Returns True on success."""
        recipe = self.getById(recipeId)
        if recipe is None:
            logger.warning(f"Recipe '{recipeId}' not found")
            return False

        recipeState = recipe.get("state", {})
        partial = WizardState.fromDict(recipeState)

        # Apply each sub-state that was present in the recipe
        if recipeState.get("audience"):
            state.audience = partial.audience
        if recipeState.get("production"):
            state.production = partial.production
        if recipeState.get("trimBinding"):
            state.trimBinding = partial.trimBinding
        if recipeState.get("content"):
            state.content = partial.content
        if recipeState.get("peripherals"):
            state.peripherals = partial.peripherals
        if recipeState.get("layout"):
            state.layout = partial.layout

        state.recipeId = recipeId
        return True
