<template>
    <div class="fixed-top row">
        <div class="accordion fixed-bottom col-lg-1 col-xs-12" id="a11yacc">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse"
                        data-bs-target="#collapseA11y" aria-expanded="false" aria-controls="collapseA11y">
                        <LanguageTranslation translation-key="A11y" />
                    </button>
                </h2>
                <div id="collapseA11y" class="accordion-collapse collapse" data-bs-parent="#a11yacc">
                    <div class="accordion-body">
                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault"
                                v-model="store.isBWMode">
                            <label class="form-check-label" for="flexCheckDefault">
                                <LanguageTranslation translation-key="BLACKWHITE_MODE" />
                            </label>
                        </div>
                        <select class="form-select" v-model.number="store.fontSizeModifier">
                            <option value="1">1x Font</option>
                            <option value="5">5x Font</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>
<script setup lang="ts">
import { useSessionStore } from '../states/session';


const store = useSessionStore();
</script>