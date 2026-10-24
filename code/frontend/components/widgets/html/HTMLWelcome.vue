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
<script setup lang="ts">

</script>

<template>
    <p>
        <LanguageTranslation translation-key="DESCRIPTION_TEXT" />
    </p>
    <div class="mb-3">
        <Icon class="align-middle me-1 welcome-skip-questions" name="ion:skip-forward"></Icon>
        <LanguageTranslation translation-key="welcome-skip-questions" />
    </div>
    <div class="mb-3">
        <Icon class="align-middle me-1 welcome-get-result" name="ion:ios-arrow-dropright-circle"></Icon>
        <LanguageTranslation translation-key="welcome-get-result" />
    </div>
    <div class="mb-3">
        <Icon class="align-middle me-1" name="ion:swap-horizontal-outline"></Icon>
        <LanguageTranslation translation-key="welcome-question-order" />
    </div>
    <div class="mb-3">
        <Icon class="align-middle me-1 welcome-delete-order" name="ion:ios-remove-circle"></Icon>
        <LanguageTranslation translation-key="welcome-delete-order" />
    </div>
    <div class="mb-3">
        <Icon class="align-middle me-1 welcome-mark-important" name="ion:ribbon-outline"></Icon>
        <LanguageTranslation translation-key="welcome-mark-important" />
    </div>
    <div class="mb-3">
        <Icon class="align-middle me-1 welcome-mark-questions" name="i-ion:bookmark-outline"></Icon>
        <LanguageTranslation translation-key="welcome-mark-questions" />
    </div>
</template>

<style lang="scss" scoped>
@import "../../../style/variables.scss";

.welcome-skip-questions {
    color: grey;
}

.welcome-get-result {
    color: $primary;
}

.welcome-delete-order {
    color: $red;
}


.welcome-mark-important {
    color: $more-weight-color;
}

.welcome-mark-questions {
    color: $orange;
}
</style>