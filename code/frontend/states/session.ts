import { defineStore } from "pinia";
import { Configuration, SessionApi, type Category, type InitialSession, type Page } from "~/sdk"

interface SessionState {
    session: InitialSession | null;
    categories: Category[];
    pages: Page[],
    currentPage: Page | null;
}

// TODO: Move this out of this sourcecode
const apiConfig = new Configuration({
    basePath: "http://localhost:8000",
    headers: {
        "accept": "application/json"
    }
})
const sessionApi = new SessionApi(apiConfig)

export const useSessionStore = defineStore('websiteStore', {
    state: (): SessionState => ({
        session: null,
        categories: [],
        pages: [],
        currentPage: null,
    }),
    actions: {
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
        selectPage(id: number) {
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
