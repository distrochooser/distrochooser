import { defineStore } from "pinia";
import { Configuration, SessionApi, type Category, type Facette, type FacetteSelection, type InitialSession, type Page } from "~/sdk"

interface SessionState {
    session: InitialSession | null;
    categories: Category[];
    pages: Page[],
    currentPage: Page | null;
    facetteSelections: FacetteSelection[]
}

// TODO: Move this out of this sourcecode
export const apiConfig = new Configuration({
    basePath: "http://localhost:8000",
    headers: {
        "accept": "application/json"
    }
});
const sessionApi = new SessionApi(apiConfig)

export const useSessionStore = defineStore('websiteStore', {
    state: (): SessionState => ({
        session: null,
        categories: [],
        pages: [],
        currentPage: null,
        facetteSelections: []
    }),
    actions: {
        async updateFacetteSelections(id: number, weight: number, add: boolean, reset: string) {

            if (add) {
                await sessionApi.sessionFacetteselectionCreate({
                    sessionPk: this.session.resultId,
                    facetteSelection: {
                        weight: weight,
                        facette: id
                    },
                    reset: reset
                });
            } else {
                await this.deleteFacetteSelection(id);
            }
            this.facetteSelections = await sessionApi.sessionFacetteselectionList({
                sessionPk: this.session.resultId
            })
        },
        async deleteFacetteSelection(facetteId: number){
            const selection = this.facetteSelections.filter(f => f.facette == facetteId)[0]
            await sessionApi.sessionFacetteselectionDestroy({
                id: selection.id,
                sessionPk: this.session.resultId
            });
        },
        async createSession(lang: string, resultId?: string) {
            this.session = await sessionApi.sessionCreate(
                {
                    resultId: resultId,
                    lang: lang
                }
            )
            if (this.session.resultId) {
                this.categories = await sessionApi.sessionCategoryList({
                    sessionPk: this.session.resultId,
                    currentPage: this.currentPage?.catalogueId ?? undefined
                });
                this.pages = await sessionApi.sessionPageList({
                    sessionPk: this.session.resultId
                })
                /** Select the first available page, if any */
                this.selectPage(-1)
            }
        },
        async acknowledgeSession() {
            if (this.session?.id && 
                this.session.languageCode && 
                this.session.resultId) {
                await sessionApi.sessionPartialUpdate({
                    id: this.session.id,
                    lang: this.session.languageCode,
                    resultId: this.session.resultId,
                    versionId: this.session.version ?? undefined
                })
            }
        },
        async selectPage(id: number) {
            const matches = this.pages.filter(l => l.id == id)
            if (matches.length == 1) {
                this.currentPage = matches[0];
            }
            else if (matches.length == 0 && this.pages.length > 0){
                this.currentPage = this.pages[0]
            }
        }
    }
})
