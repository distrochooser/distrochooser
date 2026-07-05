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
  <div
    :class="'row ' + (choosableToCompare != null ? 'row border border-info rounded-end rounded-start pt-4 ps-1 pb-0 mb-2 pe-1' : '')">
    <div class="col">
      <div class="card mb-4">
        <div class="card-body choosable-body" :style="'background-color: ' +
          props.choosable.bgColor +
          '; ' +
          'color: ' +
          props.choosable.fgColor
          ">

          <div class="card-text">
            <div class="row">
              <div class="col-8">
                <span class="choosable-position badge  me-1" :style="'background-color: ' +
                  props.choosable.fgColor +
                  '; ' +
                  'color: ' +
                  props.choosable.bgColor
                  ">{{ props.choosable.position }}.</span>
                <b class="me-1">{{ props.choosable.name }}</b>
                <LanguageTranslation :translation-key="props.choosable.catalogueId + '-description'" />
              </div>
              <div class="col-4" v-if="others.length > 0">
                <select class="form-control" v-model="choosableToCompare">
                  <option selected :value="null">
                    <LanguageTranslation translation-key="compare-with" />
                  </option>
                  <option v-for="(choosable, key) in props.others" :key="key" :value="choosable">{{ choosable.name }}
                  </option>
                </select>
              </div>
              <div class="col-4 text-end" v-else>
                <button type="button" class="btn btn-danger" v-on:click.prevent="props.onComparisonClose">
                  <LanguageTranslation translation-key="hide" />
                </button>
              </div>
            </div>
          </div>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <div class="row">
              <div class="col" v-for="(key, value, index) in props.choosable.meta" :key="index">
                <ChoosableMeta :metaKey="key" :metaValue="value" :choosable="props.choosable" />
              </div>
            </div>
          </li>
        </ul>
        <div class="card-body">
          <li class="list-group-item" v-for="(key, index) in props.choosable.assignments" :key="index">
            <Assignment :display-weigth="true" :assignment="key" :key="index" :query-choosables="false" :facette="null"
              :choosable="props.choosable" />
          </li>
        </div>
      </div>
    </div>
    <div class="col" v-if="choosableToCompare">
      <RankedChoosable v-if="choosableToCompare" :choosable="choosableToCompare" :others="[]"
        :on-comparison-close="onComparisonClose" />
    </div>
  </div>

</template>
<script setup lang="ts">
import type { RankedChoosable } from "../../sdk";
import ChoosableMeta from "./rankedchoosable/ChoosableMeta.vue";
import Assignment from "./facettes/Assignment.vue";
import { ref } from "vue";
interface WidgetProps {
  choosable: RankedChoosable;
  others: RankedChoosable[];
  onComparisonClose?: () => void;
}

const props = defineProps<WidgetProps>();

const choosableToCompare = ref<RankedChoosable | null>(null)

const onComparisonClose = () => {
  choosableToCompare.value = null
}
</script>

<style lang="scss" scoped>
.choosable-position {
  display: inline-flex;
  vertical-align: center;
}

.choosable-body {
  z-index: 99999;
}
</style>