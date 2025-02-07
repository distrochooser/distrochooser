<template>
  <span v-on:click.right.prevent="toggleEditing">
    {{ computedValue }}
  </span>
  <div v-if="isEditing" style="z-index: 100000" class="card position-fixed top-50 start-50 translate-middle"
    :title="computedValue">
    <div class="card-body">
      <h5 class="card-title">{{ computedValue }}</h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">{{ props.translationKey }}</h6>
      <div class="card-text">
        <form class="row g-3">
          <ul class="list-group list-group">
            <li v-for="(item, index) in proposals" :key="index" class="list-group-item d-flex justify-content-between align-items-start">
              <div class="ms-2 me-auto">
                <div class="fw-bold">
                  <LanguageTranslation translation-key="language-proposal"/>#{{ item.id }}
                  </div>
                  {{  item.value }}
              </div>
              <span class="badge bg-success rounded-pill me-1"  v-on:click="vote(item.id, true)">{{ item.votes.filter((l => l.isPositive)).length }}x <Icon 
                name="ion:thumbs-up-outline" </Icon></span>

                <span class="badge bg-danger rounded-pill" v-on:click="vote(item.id, false)">  {{ item.votes.filter((l => !l.isPositive)).length }}x <Icon
                  name="ion:thumbs-down-outline"></Icon></span>
            </li>
          </ul>
          <textarea rows="8" class="form-control" v-on:click.prevent.stop="() => { }"
            v-on:change="provideFeedback">{{ computedValue }}</textarea>

          <a href="#" class="card-link" v-on:click.prevent.stop="closeEdit">
            <Icon name="ion:save-outline"></Icon>
          </a>
        </form>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { computed, ref } from 'vue';
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

const vote = (id: number, isPositive) => sessionStore.voteForLanguageFeedback(id, isPositive)

const proposals = computed(() => sessionStore.languageFeedback.filter(f => f.languageKey == props.translationKey && f.session != sessionStore.session.id))


const toggleEditing = () => {
  isEditing.value = !isEditing.value
}

const closeEdit = () => {
  isEditing.value = !isEditing.value
}


</script>