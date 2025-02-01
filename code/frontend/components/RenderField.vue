<!--
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

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
  <div v-if="store.currentPage">
    
    
    <h3 v-if="store.currentPage.text">
      {{ store.currentPage.text }} 
      <Icon role="button" class="align-middle ms-1" name="ion:bookmark" v-on:click="toggleMarking"></Icon>
      <br/>
      <small v-if="store.currentPage.help" class="text-body-secondary mt-3 d-block fs-5 fw-light">{{ store.currentPage.help }}</small>
    </h3>
    <div>
      <WidgetsWrapper v-for="row in 12" :key="row" class="row" :row="row" />
    </div>
  </div>
  <div v-else>
    <Loading />
  </div>
</template>
<script setup lang="ts">
import { useSessionStore } from "../states/session";

const store = useSessionStore();
const toggleMarking = async () => {
  store.toggleMarking()
}
</script>