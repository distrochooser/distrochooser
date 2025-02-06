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
          <ul>
            <li v-for="(item, index) in proposals" :key="index">
              {{ item.value }}
              {{ item.votes.filter((l => l.isPositive)).length }}x <Icon name="ion:thumbs-up-outline" </Icon>

                {{ item.votes.filter((l => !l.isPositive)).length }}x <Icon name="ion:thumbs-down-outline"></Icon>
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

const proposals = computed(() => sessionStore.languageFeedback.filter(f => f.languageKey == props.translationKey))


const toggleEditing = () => {
  isEditing.value = !isEditing.value
}

const closeEdit = () => {
  isEditing.value = !isEditing.value
}


</script>