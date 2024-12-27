import { defineStore } from "pinia";
import { Configuration, SessionApi, type Category, type Facette, type FacetteBehaviour, type FacetteSelection, type InitialSession, type MetaWidget, type Page, type Session, type Widget } from "~/sdk"

interface SessionState {
    session: Session | null;
    categories: Category[];
    pages: Page[],
    currentPage: Page | null;
    facetteSelections: FacetteSelection[];
    currentWidgets: MetaWidget[];
    answeredPages: number[],
    facetteBehaviours: FacetteBehaviour[]
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
        facetteSelections: [],
        currentWidgets: [],
        answeredPages: [],
        facetteBehaviours: []
    }),
    actions: {
        __i(key: string) {
            return this.session.languageValues[key];
        },
        async updateFacetteSelections(currentPageId: number, id: number, weight: number, add: boolean, reset: string) {

            if (add) {
                await sessionApi.sessionFacetteselectionCreate({
                    sessionPk: this.session.resultId,
                    facetteSelection: {
                        weight: weight,
                        facette: id
                    },
                    reset: reset
                });
                if (this.answeredPages.indexOf(currentPageId) == -1){
                    this.answeredPages.push(currentPageId)
                }
            } else {
                await this.deleteFacetteSelection(id, currentPageId);
            }
            this.facetteSelections = await sessionApi.sessionFacetteselectionList({
                sessionPk: this.session.resultId
            })
        },
        async deleteFacetteSelection(facetteId: number, currentPageId: number) {
            const selection = this.facetteSelections.filter(f => f.facette == facetteId)[0]
            await sessionApi.sessionFacetteselectionDestroy({
                id: selection.id,
                sessionPk: this.session.resultId
            });
            this.answeredPages = this.answeredPages.filter(s => s != currentPageId)
        },
        async createSession(lang: string, resultId?: string) {
            this.session = await sessionApi.sessionCreate(
                {
                    resultId: resultId,
                    lang: lang
                }
            )
            if (this.session.resultId) {
                await this.updateCategoriesAndPages();
                /** Select the first available page, if any */
                this.selectPage(-1)
            }
        },
        async updateCategoriesAndPages() {
            this.categories = await sessionApi.sessionCategoryList({
                sessionPk: this.session.resultId,
                currentPage: this.currentPage?.catalogueId ?? undefined
            });
            this.pages = await sessionApi.sessionPageList({
                sessionPk: this.session.resultId
            })
            if (this.currentPage) {
                const oldPageNumber = this.currentPage.id;
                this.selectPage(oldPageNumber);
            }
        },
        async updateBehaviours() {
            this.facetteBehaviours = await sessionApi.sessionFacettebehaviourList({
                sessionPk: this.session.resultId
            });
        },
        async updateSession(sessionVersion: number)  {
            this.session = await sessionApi.sessionPartialUpdate({
                id: this.session.id,
                lang: this.session.languageCode,
                resultId: this.session.resultId,
                versionId: sessionVersion
            })
            await this.updateCategoriesAndPages()
        },
        async changeLanguage(language: string) {
            this.session = await sessionApi.sessionPartialUpdate({
                id: this.session.id,
                lang:language,
                resultId: this.session.resultId,
                versionId: this.session.version
            })
            await this.updateCategoriesAndPages()
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
            else if (matches.length == 0 && this.pages.length > 0) {
                this.currentPage = this.pages[0]
            }
            this.currentWidgets = await sessionApi.sessionPageWidgetList({
                sessionPk: this.session.resultId,
                pagePk: this.currentPage.id
            })
        }
    }
})
