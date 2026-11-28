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
    <span class="badge pill text-bg-warning" v-if="clickRank.rank == 1">
        <Icon name="ion:flame" class="align-middle me-1" />
        <span class="align-middle">
            <LanguageTranslation translation-key="most_clicks_this_month" />
        </span>
    </span>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import type { RankedChoosable } from '../sdk';

interface WidgetProps {
    choosable: RankedChoosable;
    all: RankedChoosable[]
}

interface ClickRank {
    rank: number;
    clicks: number;
}
const props = defineProps<WidgetProps>();

const clickRank = computed((): ClickRank => {
    const sortedClicks = props.all.sort((a, b) => b.clicksThisMonth - a.clicksThisMonth)

    return {
        rank: sortedClicks.indexOf(props.choosable) + 1,
        clicks: props.choosable.clicksThisMonth
    }
})
</script>