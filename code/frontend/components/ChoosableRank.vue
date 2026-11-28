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
    <span class="badge align-middle me-1 badge-left-flat" :style="props.styling">
        <span class="align-middle">
            {{ getPoints(props.choosable.assignments) }}P
        </span>
        <span class="align-middle">
            <LanguageTranslation translation-key="points_out_of" /> {{ maxPoints }}P
        </span>
    </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { FacetteAssignment, RankedChoosable } from '../sdk';
import { useSessionStore } from '../states/session';



interface ChoosableRankProps {
    choosable: RankedChoosable;
    all: RankedChoosable[];
    styling: string;
}

const props = defineProps<ChoosableRankProps>();

const store = useSessionStore()
const getPoints = (assignments: FacetteAssignment[]) => Math.round(assignments.map(a => store.session.scoreMap[a.assignmentType]).reduce((sum, num) => sum + num, 0) * 100) / 100
const maxPoints = computed(() => Math.max(...props.all.map((c) => getPoints(c.assignments))))
</script>