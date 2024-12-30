/*
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import { defineStore } from "pinia";
import { Configuration, SessionApi, type Category, type Choosable, type Facette, type FacetteBehaviour, type FacetteSelection, type InitialSession, type MetaWidget, type Page, type Session, type Widget } from "~/sdk"

interface SessionState {
    session: Session | null;
    categories: Category[];
    pages: Page[],
    currentPage: Page | null;
    facetteSelections: FacetteSelection[];
    currentWidgets: MetaWidget[];
    facetteBehaviours: FacetteBehaviour[];
    choosables: Choosable[]
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
        facetteBehaviours: [],
        choosables: []
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
        },
        async createSession(lang: string, resultId?: string) {
            this.session = await sessionApi.sessionCreate(
                {
                    resultId: resultId,
                    lang: lang
                }
            )
            if (this.session.resultId) {
                this.choosables = await sessionApi.sessionChoosableList({
                    sessionPk: this.session.resultId
                })
                await this.updateCategoriesAndPages();
                /** Select the first available page, if any */
                this.selectPage(-1)
            }
            // if there was a resultId given -> update selections from it
            if (resultId) {
                this.facetteSelections = await sessionApi.sessionFacetteselectionList({
                    sessionPk: this.session.resultId
                })
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
