<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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
    <p class="d-inline-flex gap-1" v-if="sessionStore.missingLanguageValues.length > 0">
        <a class="btn btn-primary" data-bs-toggle="collapse" href="#missingLanguageList" role="button" aria-expanded="false"
            aria-controls="missingLanguageList">
            
            <Icon class="me-1" name="ion:language"></Icon>
            <LanguageTranslation translation-key="SUPPORT_LANGUAGE_MISSING"/>
        </a>
    </p>
    <div class="collapse" id="missingLanguageList">
        <div class="card card-body">
            
    <MissingLanguageList />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSessionStore } from '../../../states/session';
import MissingLanguageList from '../../MissingLanguageList.vue';

// TODO: Decide to migrate this widget into a "real" widget rather than a HTML widget
const sessionStore = useSessionStore();

</script>