<template>
  <span v-on:click="toggleEditing($event)"
    :class="{ 'needs-translation': sessionStore.isTranslating && isUntranslated, 'hover-translation': sessionStore.isTranslating }">
    <span class="me-4">{{ computedValue }}</span>
    <span class="fs-6 top-0 start-100 translate-middle badge rounded-pill bg-warning translation-tooltip" v-if="sessionStore.isTranslating && proposals.length >0">
      <Icon name="ion:chatbubbles-sharp"></Icon> {{proposals.length}}
    </span>
    <span class="fs-6 top-0 start-100 translate-middle badge rounded-pill bg-success translation-tooltip" v-if="sessionStore.isTranslating && isAdded">
      <Icon name="ion:cloud-done"></Icon>
    </span>
  </span>
  <div v-if="isEditing" style="z-index: 100000" class="card translation-window">
    <div class="card-body">
      <h5 class="card-title mb-3">
        Translation
      </h5>
      <div class="card-text">

        <ul class="list-group col">
          <li class="list-group-item fs-6"><span
              class="badge text-bg-light me-2">{{ sessionStore.session.defaultLanguage }}</span>{{
                sessionStore.session.defaultLanguageValues[props.translationKey] ?? props.translationKey }} </li>
          <li class="list-group-item text-center fs-3 pt-2">
            <Icon name="ion:arrow-down-sharp"></Icon>
          </li>
          <li class="list-group-item fs-6"><span class="badge text-bg-dark me-2">{{ sessionStore.session.languageCode
          }}</span> {{ computedValue }}</li>
        </ul>
        <form class="g-3 mt-3">
          <h5 class="card-title mb-3" v-if="proposals.length > 0">
            Other user suggestions
          </h5>
          <ul class="list-group list-group">
            <li v-for="(item, index) in proposals" :key="index"
              class="list-group-item d-flex justify-content-between align-items-start">
              <div class="ms-2 me-auto">
                <div class="fw-bold">
                  <LanguageTranslation translation-key="language-proposal" />#{{ item.id }}
                </div>
                {{ item.value }}
              </div>
              <span class="badge bg-success rounded-pill me-1 vote-button" v-on:click="vote(item.id, true)">
                {{item.votes.filter((l => l.isPositive)).length}}x <Icon name="ion:thumbs-up-outline" </Icon></span>

              <span class="badge bg-danger rounded-pill vote-button" v-on:click="vote(item.id, false)">
                {{item.votes.filter((l => !l.isPositive)).length}}x <Icon name="ion:thumbs-down-outline"></Icon></span>
            </li>
          </ul>
          <h5 class="card-title mb-3 mt-3">
            Your suggestions
          </h5>
          <textarea rows="2" class="form-control" v-on:click.prevent.stop="() => { }"
            v-on:change="provideFeedback">{{ computedValue }}</textarea>

        </form>
      </div>
    </div>
    <div class="card-footer">
      <a href="#" class="btn btn-primary" v-on:click.prevent.stop="closeEdit">
        <Icon name="ion:save-outline"></Icon> Save
      </a>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { computed, ref, watch } from 'vue';
import { useSessionStore } from '../states/session';

interface TranslationProps {
  translationKey: string;
}

const sessionStore = useSessionStore();
const props = defineProps<TranslationProps>();
const computedValue = computed(() => sessionStore.__i(props.translationKey))
const isEditing = ref(false);
const provideFeedback = async (e: Event) => {
  const newValue = (e.target as HTMLInputElement).value;
  await sessionStore.provideTranslation(props.translationKey, newValue);
}

const vote = (id: number, isPositive) => {
  sessionStore.voteForLanguageFeedback(id, isPositive)
}

const isAdded = computed(() => sessionStore.languageFeedback.filter(l => l.session == sessionStore.session.id && l.languageKey == props.translationKey).length != 0)


const proposals = computed(() => sessionStore.languageFeedback.filter(f => f.languageKey == props.translationKey && f.session != sessionStore.session.id))

const toggleEditing = (e: MouseEvent) => {
  if (sessionStore.isTranslating && sessionStore.session && !sessionStore.isTranslationOpen) {
    e.preventDefault()
    e.stopPropagation()
    e.stopImmediatePropagation()
    isEditing.value = !isEditing.value
    sessionStore.isTranslationOpen = true
  }
}

const closeEdit = () => {
  isEditing.value = false
  sessionStore.isTranslationOpen = false
}

const isUntranslated = computed(() => sessionStore.missingLanguageValues.indexOf(props.translationKey) !== -1 || typeof sessionStore.session.languageValues[props.translationKey] === "undefined");

watch(computedValue, value => {
  if (!sessionStore.session) {
    return
  }
  if (typeof sessionStore.session.languageValues[props.translationKey] != "undefined" && computedValue.value == props.translationKey && sessionStore.missingLanguageValues.indexOf(props.translationKey) == -1) {
    sessionStore.addMissingLanguageValue(props.translationKey)
  }
  if (computedValue.value != props.translationKey && sessionStore.missingLanguageValues.indexOf(props.translationKey) != -1) {
    sessionStore.removeMissingLanguageValue(props.translationKey)
  }
}, { deep: true, immediate: true })
</script>
<style lang="scss" scoped>
@import "../style/variables.scss";

.needs-translation {
  border-bottom: 1px dotted $missingLanguageColor;
}

.translation-window {
  position: fixed;
  top: 5%;
  left: 33%;
  width: 33%;
}

.hover-translation {
  cursor: crosshair;
}

.vote-button {
  cursor: pointer;
}
.translation-tooltip {
  font-size: small !important;
  display: inline-table;
}
</style>