<!--
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
-->
<template>
    <div class="fixed-bottom  row">
        <div class="accordion col-lg-2 col-xs-12" id="a11yacc">
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
                            <input class="form-check-input" type="checkbox" value="" id="bwMode"
                                v-model="store.isBWMode">
                            <label class="form-check-label" for="bwMode">
                                <LanguageTranslation translation-key="BLACKWHITE_MODE" />
                            </label>
                        </div>
                        <div class="form-check mb-3">
                            <input :key="store.isDarkMode ? 'dark-mode-render-trigger' : ''" class="form-check-input" type="checkbox"  id="darkMode"
                                v-model="store.isDarkMode" :checked="store.isDarkMode">
                            <label class="form-check-label" for="darkMode">
                                Dark Mode
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