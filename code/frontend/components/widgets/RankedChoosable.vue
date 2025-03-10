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
  <div>
    <div class="card mb-4">
      <div
        class="card-body"
        :style="
          'background-color: ' +
          props.choosable.bgColor +
          '; ' +
          'color: ' +
          props.choosable.fgColor
        "
      >
        <h5 class="card-title">
          <LanguageTranslation :translation-key="props.choosable.displayName"/>
        </h5>
        <p class="card-text">
          <LanguageTranslation :translation-key="props.choosable.description"/>
        </p>
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <div class="row">
            <div
              class="col"
              v-for="(key, value, index) in props.choosable.meta"
              :key="index"
            >
              <ChoosableMeta :metaKey="key" :metaValue="value" :choosable="props.choosable"/>
            </div>
          </div>
        </li>
      </ul>
      <div class="card-body">
        <li class="list-group-item" v-for="(key, index) in props.choosable.assignments" :key="index">
          <Assignment :display-weigth="true" :assignment="key" :key="index" :query-choosables="false" :facette="null" :choosable="props.choosable"/>
        </li>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { RankedChoosable } from "../../sdk";
import ChoosableMeta from "./rankedchoosable/ChoosableMeta.vue";
import Assignment from "./facettes/Assignment.vue";
interface WidgetProps {
  choosable: RankedChoosable;
}

const props = defineProps<WidgetProps>();
</script>