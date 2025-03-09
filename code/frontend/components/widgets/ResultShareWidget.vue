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
    <div class="col-xl-4 d-none d-sm-block">
    </div>
    <div class="col-xl-4 col-sm-12">
      <div class="row mb-2">
        <div class="col">
          <div class="card">
            <div class="card-header">
              <LanguageTranslation translation-key="SHARE_MY_RESULT" />
            </div>
            <ul class="list-group list-group-flush mt-2">
              <li class="list-group-item">
                <div class="row">
                  <div class="col text-center">
                    <a :href="'https://www.facebook.com/sharer/sharer.php?u=' + shareUrl" target="_blank">
                      <Icon class="icon facebook-icon" name="ion:logo-facebook"></Icon>
                    </a>
                  </div>
                  <div class="col text-center">
                    <a :href="'https://bsky.app/intent/compose?text=' + shareUrl" target="_blank">
                      <!-- https://en.m.wikipedia.org/wiki/File:Bluesky_Logo.svg -->
                      <svg class="svg-icon" fill="#0886fe" viewBox="0 0 600 530"
                        xmlns="http://www.w3.org/2000/svg">
                        <path
                          d="m135.72 44.03c66.496 49.921 138.02 151.14 164.28 205.46 26.262-54.316 97.782-155.54 164.28-205.46 47.98-36.021 125.72-63.892 125.72 24.795 0 17.712-10.155 148.79-16.111 170.07-20.703 73.984-96.144 92.854-163.25 81.433 117.3 19.964 147.14 86.092 82.697 152.22-122.39 125.59-175.91-31.511-189.63-71.766-2.514-7.3797-3.6904-10.832-3.7077-7.8964-0.0174-2.9357-1.1937 0.51669-3.7077 7.8964-13.714 40.255-67.233 197.36-189.63 71.766-64.444-66.128-34.605-132.26 82.697-152.22-67.108 11.421-142.55-7.4491-163.25-81.433-5.9562-21.282-16.111-152.36-16.111-170.07 0-88.687 77.742-60.816 125.72-24.795z" />
                      </svg>
                    </a>
                  </div>
                  <div class="col text-center">
                    <a :href="'https://twitter.com/share?url=' + shareUrl + '&hashtags=distrochooser,linux&via=distrochooser'"
                      target="_blank">
                      <Icon class="icon twitter-icon" name="ion:logo-twitter"></Icon>
                    </a>
                  </div>
                  <div class="col text-center">
                    <a :href="'http://reddit.com/submit?url=' + shareUrl + '&title=Distrochooser.de'" target="_blank">
                      <Icon class="icon reddit-icon" name="ion:logo-reddit"></Icon>
                    </a>
                  </div>
                </div>
              </li>
              <li class="list-group-item">
                <div class="input-group">
                  <span class="input-group-text" id="share-link">
                    <Icon name="ion:share-outline"></Icon>
                  </span>
                  <input type="text" class="form-control" :value="shareUrl" aria-label="Share URL"
                    onfocus="this.select();" onmouseup="return false;" aria-describedby="share-link" />
                </div>
              </li>
            </ul>
          </div>
        </div>

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
.icon {
  font-size: 1.5em;
}
.svg-icon {
  height: 1.5em;
}
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