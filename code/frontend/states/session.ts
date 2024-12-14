import { defineStore } from "pinia";
import { Configuration, SessionApi, type InitialSession } from "~/sdk"

interface SessionState {
    session: InitialSession | null;
}

// TODO: Move this out of this sourcecode
const sessionApi = new SessionApi(new Configuration({
    basePath: "http://localhost:8000",
    headers: {
        "accept": "application/json"
    }
}))

export const useSessionStore = defineStore('websiteStore', {
    state: (): SessionState => ({
        session: null
    }),
    actions: {
        async createSession(lang: string, resultId?: string) {
            this.session = await sessionApi.sessionCreate(
                {
                    resultId: resultId,
                    lang: lang
                }
            )
        }
    }
})
