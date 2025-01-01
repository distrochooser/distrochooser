<template>
    <span>
      <a :href="props.website" @click="handleClick">{{ props.website }}</a>
    </span>
</template>


<script lang="ts" setup>
import { apiConfig } from '../../../../states/session';


interface FlagProps {
  website: string;
  id: number;
}

const props = defineProps<FlagProps>();
const handleClick = async (e: MouseEvent) => {
  e.preventDefault();
  const target = apiConfig.basePath +  "/out/" + props.id.toString() + "/WEBSITE/"
  console.log(target)
  await fetch(target)
  window.open(props.website, "_blank")
}
</script>