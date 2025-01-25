<template>
    <span>
      <a :href="props.website" @click="handleClick">{{ props.website }}</a>
    </span>
</template>


<script lang="ts" setup>
const basePath = useRuntimeConfig().public.basePath

interface FlagProps {
  website: string;
  id: number;
}

const props = defineProps<FlagProps>();
const handleClick = async (e: MouseEvent) => {
  e.preventDefault();
  const target = basePath +  "/out/" + props.id.toString() + "/WEBSITE/"
  console.log(target)
  await fetch(target)
  window.open(props.website, "_blank")
}
</script>