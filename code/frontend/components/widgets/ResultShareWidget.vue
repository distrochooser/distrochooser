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
  <div class="row">
    <div class="col-4">
    </div>
    <div class="col-4">

      <div class="row mb-2">
        <div class="col">
          <LanguageTranslation translation-key="SHARE_MY_RESULT" />
        </div>
      </div>
      <div class="row mb-2">
        <div class="col text-center">
          <a :href="'https://www.facebook.com/sharer/sharer.php?u=' + shareUrl"
            target="_blank">
            <Icon class="fs-3 facebook-icon" name="ion:logo-facebook"></Icon>
          </a>
        </div>
        <div class="col text-center">
          <a :href="'https://twitter.com/share?url=' + shareUrl + '&hashtags=distrochooser,linux&via=distrochooser'"
            target="_blank">
            <Icon class="fs-3 twitter-icon" name="ion:logo-twitter"></Icon>
          </a>
        </div>
        <div class="col text-center">
          <a :href="'http://reddit.com/submit?url=' + shareUrl + '&title=Distrochooser.de'"
            target="_blank">
            <Icon class="fs-3 reddit-icon" name="ion:logo-reddit"></Icon>
          </a>
        </div>
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text" id="share-link">
          <Icon name="ion:share-outline"></Icon>
        </span>
        <input type="text" class="form-control" :value="shareUrl" aria-label="Share URL"
          aria-describedby="share-link" />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import type { ResultShareWidget } from "../../sdk";
import { useSessionStore } from "../../states/session";

interface WidgetProps {
  widget: ResultShareWidget;
}

const props = defineProps<WidgetProps>();
const store = useSessionStore();
const { resultId, languageCode } = store.session;
const shareUrl = computed(
  () => store.session.baseUrl + "/" + languageCode + "/" + resultId
);
</script>
<style lang="css" scoped>
.facebook-icon {
  color: #4267b2;
}
.reddit-icon {
  color: #ff4500;
}
.twitter-icon {
  color: #1da1f2;
}
</style>