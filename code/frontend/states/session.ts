/*
distrochooser
Copyright (C) 2014-2025 Christoph Müller  <mail@chmr.eu>

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
import { Configuration, SessionApi, type Category, type Choosable, type Facette, type FacetteAssignment, type FacetteBehaviour, type FacetteSelection, type Feedback, type InitialSession, type LanguageFeedback, type MetaWidget, type Page, type PageMarking, type Session, type Widget } from "../sdk"
import { useRuntimeConfig } from "nuxt/app";
import LanguageFeedback from "../components/LanguageFeedback.vue";
interface SessionState {
    session: Session | null;
    categories: Category[];
    pages: Page[],
    currentPage: Page | null;
    facetteSelections: FacetteSelection[];
    currentWidgets: MetaWidget[];
    facetteBehaviours: FacetteBehaviour[];
    choosables: Choosable[];
    assignmentFeedback: Feedback[];
    pageMarkings: PageMarking[];
    isTranslating: boolean;
    languageFeedback: LanguageFeedback[];
}
let sessionApi: SessionApi = null;

export const useSessionStore = defineStore('websiteStore', {
    state: (): SessionState => ({
        session: null,
        categories: [],
        pages: [],
        currentPage: null,
        facetteSelections: [],
        currentWidgets: [],
        facetteBehaviours: [],
        choosables: [],
        assignmentFeedback: [],
        pageMarkings: [], /* TODO: Implement and decide if these should persist */
        isTranslating: false,
        languageFeedback: []
    }),
    getters: {
        sessionApi(): SessionApi {
            if (sessionApi == null){
                const apiConfig = new Configuration({
                    basePath:  useRuntimeConfig().public.basePath,
                    headers: {
                        "accept": "application/json"
                    }
                });
                sessionApi = new SessionApi(apiConfig)
            }
            return sessionApi;
        }
    },
    actions: {
        async toggleTranslateFeedback() {
            this.isTranslating = !this.isTranslating
            if (this.isTranslating) {
                this.getTranslationFeedback();
            }
        },
        async getTranslationFeedback() {
            this.languageFeedback =  await this.sessionApi.sessionLanguageList({
                sessionPk: this.session.resultId
            })
        },
        async provideTranslation(key: string, value: string) {
            await this.sessionApi.sessionLanguageCreate({
                sessionPk: this.session.resultId,        
                createLanguageFeedback: {
                    languageKey: key,
                    value: value
                }
            })
            await this.getTranslationFeedback();
        },
        __i(key: string) {
            const providedFeedback = this.languageFeedback.filter(l => l.languageKey == key)
            if (providedFeedback.length > 0) {
                return providedFeedback[0].value
            }
            if (typeof this.session.languageValues[key] == "undefined") {
                return key
            }
            return this.session.languageValues[key];
        },
        async updateFacetteSelections(currentPageId: number, id: number, weight: number, add: boolean, reset: string) {

            if (add) {
                await this.sessionApi.sessionFacetteselectionCreate({
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
            this.facetteSelections = await this.sessionApi.sessionFacetteselectionList({
                sessionPk: this.session.resultId
            })
        },
        async deleteFacetteSelection(facetteId: number, currentPageId: number) {
            const selection = this.facetteSelections.filter(f => f.facette == facetteId)[0]
            // If there is no matching facette: Ignore
            if (selection) {
                await this.sessionApi.sessionFacetteselectionDestroy({
                    id: selection.id,
                    sessionPk: this.session.resultId
                });
            }
        },
        async createSession(lang: string, resultId?: string) {
            this.session = await this.sessionApi.sessionCreate(
                {
                    resultId: resultId,
                    lang: lang
                }
            )
            if (this.session.resultId) {
                this.choosables = await this.sessionApi.sessionChoosableList({
                    sessionPk: this.session.resultId
                })
                await this.updateCategoriesAndPages();
                /** Select the first available page, if any */
                this.selectPage(-1)
            }
            // if there was a resultId given -> update selections from it
            if (resultId) {
                this.facetteSelections = await this.sessionApi.sessionFacetteselectionList({
                    sessionPk: this.session.resultId
                })
            }
        },
        async updateCategoriesAndPages() {
            this.categories = await this.sessionApi.sessionCategoryList({
                sessionPk: this.session.resultId,
                currentPage: this.currentPage?.catalogueId ?? undefined
            });
            this.pages = await this.sessionApi.sessionPageList({
                sessionPk: this.session.resultId
            })
            if (this.currentPage) {
                const oldPageNumber = this.currentPage.id;
                this.selectPage(oldPageNumber);
            }
        },
        async updateBehaviours() {
            this.facetteBehaviours = await this.sessionApi.sessionFacettebehaviourList({
                sessionPk: this.session.resultId
            });
        },
        async updateSession(sessionVersion: number) {
            this.session = await this.sessionApi.sessionPartialUpdate({
                id: this.session.id,
                lang: this.session.languageCode,
                resultId: this.session.resultId,
                versionId: sessionVersion
            })
            await this.updateCategoriesAndPages()
        },
        async changeLanguage(language: string) {
            this.session = await this.sessionApi.sessionPartialUpdate({
                id: this.session.id,
                lang: language,
                resultId: this.session.resultId,
                versionId: this.session.version
            })
            await this.updateCategoriesAndPages()
            await this.getTranslationFeedback()
        },
        async acknowledgeSession() {
            if (this.session?.id &&
                this.session.languageCode &&
                this.session.resultId) {
                await this.sessionApi.sessionPartialUpdate({
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
            this.currentWidgets = await this.sessionApi.sessionPageWidgetList({
                sessionPk: this.session.resultId,
                pagePk: this.currentPage.id
            })
        },
        async giveFeedback(assignment: FacetteAssignment, choosable: Choosable, facette: Facette, isPositive: boolean) {
            this.assignmentFeedback = this.assignmentFeedback.filter(a => a.choosable != choosable.id && a.assignment != assignment.id)
            
            const got = await this.sessionApi.sessionFeedbackCreate({
                sessionPk: this.session.resultId,
                createFeedback: {
                    choosable: choosable.id,
                    assignment: assignment.id,
                    isPositive: isPositive
                }
            })
            this.assignmentFeedback.push(got)
        },
        async removeFeedback(assignment: FacetteAssignment, choosable: Choosable) {
            const toRemove = this.assignmentFeedback.filter(a => a.choosable == choosable.id && a.assignment == assignment.id)
            console.log(toRemove)
            this.assignmentFeedback = this.assignmentFeedback.filter(a => a.choosable != choosable.id && a.assignment != assignment.id)

            toRemove.forEach(l => {
                sessionApi.sessionFeedbackDestroy({
                    sessionPk: this.session.resultId,
                    id: l.id
                })
            })
        },
        async toggleMarking() {
            const isMarked = await sessionApi.sessionPageMarkingList({
                sessionPk: this.session.resultId,
                pagePk: this.currentPage.id.toString() /* TODO: this is disgusting. Please fix */
            })
            console.log(isMarked)
            if (isMarked.length == 0) {
                const got = await sessionApi.sessionPageMarkingCreate({
                    sessionPk: this.session.resultId,
                    pagePk: this.currentPage.id.toString()
                })
                this.pageMarkings.push(got)
            } else {
                await sessionApi.sessionPageMarkingDestroy({
                    id: isMarked[0].id,
                    sessionPk: this.session.resultId,
                    pagePk: this.currentPage.id.toString()
                })
                this.pageMarkings = this.pageMarkings.filter(l => l.id != isMarked[0].id)
            }
        }
    }
})
