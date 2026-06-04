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
    <div :id="props.widget.catalogueId">
      <HTMLWelcome v-if="props.widget.template == 'welcomeHTML'"/>
      <HTMLLanguage v-if="props.widget.template == 'languageHTML'"/>
      <HTMLA11y v-if="props.widget.template == 'a11yHTML'"/>
      <HTMLBanner v-if="props.widget.template == 'bannerHTML'" :catalogue-id="props.widget.catalogueId"/>
    </div>
</template>
<script setup lang="ts">
import type {HTMLWidget } from '../../sdk';
import HTMLWelcome from "../widgets/html/HTMLWelcome.vue";
import HTMLA11y from './html/HTMLA11y.vue';
import HTMLBanner from './html/HTMLBanner.vue';
import HTMLLanguage from './html/HTMLLanguage.vue';


// TODO: Naming for "templates" and documentation
// TODO: Mapping for child components
// TODO: Inject settings especially for HTMLBanner
interface WidgetProps {
  widget: HTMLWidget;
}

const props = defineProps<WidgetProps>();

</script>