import type { Category, Facette, FacetteRadioSelectionWidget, FacetteSelection, FacetteSelectionWidget, Page } from "../../sdk/models";

export function isCategoryAnswered(category: Category, pages: Page[], selections: FacetteSelection[]): boolean {
    const targetPageId = category.targetPage
    const targetPages: Page[] = pages.filter(p => p.id == targetPageId)
    if (targetPages.length == 0) {
        return false
    }
    const targetPage = targetPages[0]
    const facetteSelections: FacetteSelection[] = selections
    if (!targetPage) {
        return false;
    }
    let allFacettesWithinPage: Facette[] = []
    targetPage.widgetList.filter(w => w.widgetType == "FacetteSelectionWidget" || w.widgetType == "FacetteRadioSelectionWidget").forEach((w: (FacetteSelectionWidget | FacetteRadioSelectionWidget)) => {
        allFacettesWithinPage = allFacettesWithinPage.concat(w.facettes)
    });
    const facettesWithinPage = facetteSelections.filter(s => allFacettesWithinPage.filter(f => f.id == s.facette).length != 0)
    return facettesWithinPage.length != 0
}