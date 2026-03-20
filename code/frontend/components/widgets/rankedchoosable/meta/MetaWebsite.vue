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
    <span>
      <a :href="url.toString()" target="_blank">{{ props.website }}</a>
    </span>
</template>


<script lang="ts" setup>
import { useSessionStore } from '../../../../states/session';
import { getExternalLink } from '../../../../util/links';


interface FlagProps {
  website: string;
  id: number;
}

const props = defineProps<FlagProps>();
const store = useSessionStore();
const url = getExternalLink(store.session.baseUrl, store.session.languageCode, "noprefix", props.website, true) + "/" + props.id
</script>