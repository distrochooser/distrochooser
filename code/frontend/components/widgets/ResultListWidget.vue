<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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
  <div>
    <div class="accordion mb-2" >
      <div class="accordion-item">
        <h2 class="accordion-header">
          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne"
            aria-expanded="false" aria-controls="collapseOne">
            <LanguageTranslation translation-key="SCORE_HEADER" />
          </button>
        </h2>
        <div id="collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
          <div class="accordion-body">
            <p>
              <LanguageTranslation translation-key="SCORE_TEXT" />
            </p>
            <div v-for="(value, key) in store.session.scoreMap" :key="key">
              <LanguageTranslation :translation-key="key"/> ({{ key }}): <span :class="'badge ' + (value < 0 ? 'text-bg-danger' : 'text-bg-success')">{{  value }}</span>
            </div>
            <br/>
            <p>
              <LanguageTranslation translation-key="SCORE_TEXT_Positions" />
            </p>
          </div>
        </div>
      </div>
    </div>
    <div v-for="(choosable, index) in orderedChoosables" :key="index">
      <RankedChoosable :choosable="choosable"
        :others="orderedChoosables.filter(c => c.catalogueId !== choosable.catalogueId)" />
    </div>
    <div class="alert alert-info" v-if="orderedChoosables.length == 0">
      <b>
        <LanguageTranslation translation-key="NO_RESULTS_TITLE" />
      </b>
      <p>
        <LanguageTranslation translation-key="NO_RESULTS_TEXT" />
      </p>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { Choosable, ResultListWidget } from "../../sdk";
import RankedChoosable from "./RankedChoosable.vue";
import { useSessionStore } from "../../states/session";
import { computed } from "vue";

interface WidgetProps {
  widget: ResultListWidget;
}

const props = defineProps<WidgetProps>();
const store = useSessionStore();

const orderedChoosables = computed(() => props.widget.choosables.sort(
  (a, b) => b.rank - a.rank
).filter(c => store.mustHaveAssignment ? c.assignments.length > 0 : true))

</script>