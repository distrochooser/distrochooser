<template lang="pug">
    div.hardware
        div.hardware-values
            h2 {{ __i("hardware-title") }}
            p {{ __i("hardware-text") }}
            div.help 
                div.windows
                    h3 Windows
                    ol 
                        li {{ __i("windows-x-hint") }}
                        li {{ __i("windows-choose-system") }}
                div.mac
                    h3 Mac
                    ul 
                        li {{ __i("no-mac-distros") }} 
                div.linux
                    h3 Linux
                    ol 
                        li {{ __i("linux-open-terminal") }}
                        li {{ __i("linux-execute") }} 
                            code bash -c 'echo CPU frequency in Ghz: $(($(cat /proc/cpuinfo | grep MHz | tail  -n 1 | grep -Eo "[0-9]+" | head  -n 1) / 1000)) && echo Memory in GB: $(($(grep MemTotal /proc/meminfo | grep -Eo "[0-9]+") / 1024 / 1024))'
            
            div.hardware-input.identify
                label(for="this-computer") {{  __i('hardware-this-computer') }}
                input(name="this-computer", type="checkbox", v-model="thisComputer", v-on:change="detectSpecs") 
            div.cpu.hardware-input.cores
                label(for="cpu-cores") {{  __i('hardware-cpu-cores-title') }}
                input(name="cpu-cores", type="number", :placeholder="__i('hardware-cpu-cores-placeholder')", v-model="cpuCores")
            div.cpu.hardware-input.frequency
                label(for="cpu-frequency") {{  __i('hardware-cpu-frequency-title') }}
                input(name="cpu-frequency", :placeholder="__i('hardware-cpu-frequency-placeholder')",v-model="cpuFrequency")
            div.memory.hardware-input
                label(for="memory") {{  __i('hardware-memory-title') }}
                input(name="memory", type="number", :placeholder="__i('hardware-memory-placeholder')", v-model="memory")
            div.storage.hardware-input
                label(for="storage") {{  __i('hardware-storage-title') }}
                input(name="storage", type="number", :placeholder="__i('hardware-storage-placeholder')", v-model="storage")
            div.touch.hardware-input
                label(for="touch") {{  __i('hardware-touch-title') }}
                input(name="touch",  type="checkbox", v-model="touch")
            div.mobile.hardware-input
                label(for="mobile") {{  __i('hardware-mobile-title') }}
                input(name="mobile",  type="checkbox", v-model="mobile")
            div(v-if="filledOut")
                h3 {{  __i("hardware-assumption-result") }}
                div.hardware-input(v-for="(result_value, result_key) in result", :key="result_key", :class="result_key", v-if="result_value")
                    label {{ __i(result_key) }}
                    i(v-bind:class="{'w-icon-check-square-o': result_value, 'w-icon-close-square-o': !result_value}") 
            
        div.actions
            button.skip-step.step(@click="startTestFunc") {{  __i("skip-question") }}
            button.start-test-button.next-step.step(@click="startTestFuncWithStoredHardware") {{ __i("start-test") }}
</template>
<script> 
import i18n from '~/mixins/i18n'
export default {
mixins: [i18n],
    props: {
        language: {
            type: String,
            required: true,
            default: 'en'
        },
        startTestFunc: {
            type: Function,
            required: true,
            default:  null
        }
    },
    data: function() {
        return {
            thisComputer: false,
            cpuCores: 0,
            cpuFrequency: 0,
            memory: 0,
            storage: 0,
            touch: false,
            mobile: false
        }
    },
    computed: {
        filledOut: function () {
            return this.cpuCores != 0 && this.cpuFrequency != 0 && this.memory != 0 && this.storage != 0
        },
        result: function () {
            return {
                "multi-core": this.cpuCores > 1,
                "cpu-64bit": navigator.userAgent.match(/(WOW64|x64|Macintosh)/i) != null && this.cpuCores > 1, 
                "mobile": this.mobile,
                "touch": this.touch,
                "memory-limited": this.memory < 8,
                "storage-limited": this.memory < 20,
                "cpu-limited": this.cpuCores <= 2 || this.cpuFrequency <= 2
            }
        }
    },
    methods: {
        startTestFuncWithStoredHardware: function () {
            console.log("save data")
            this.startTestFunc()
        }, 
        /* https://stackoverflow.com/questions/4817029/whats-the-best-way-to-detect-a-touch-screen-device-using-javascript*/
        detectTouch: function () {
            return (('ontouchstart' in window) ||
                (navigator.maxTouchPoints > 0) ||
                (navigator.msMaxTouchPoints > 0));
        },
        detectSpecs: function () {
            if (this.thisComputer) {
                this.cpuCores = navigator.hardwareConcurrency
                this.memory = navigator.deviceMemory /* Not on all browsers */
                if (!this.memory) {
                    this.memory = 0
                }
                this.touch = this.detectTouch()
            } else {
                this.cpuCores = 0
                this.memory = 0
                this.cpu = ""
                this.storage = 0
                this.touch = false
                this.mobile = false
            }
        }
    }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
.hardware-values {
    width: 75%;
    margin-left: 15%;
    h2 {
        padding-top: 1em;
    }
}
.hardware-input {
    display: table;
    width: 100%;
    table-layout: fixed;
    margin-top: 1em;
    margin-bottom: 1em;
    label {
        display: table-cell;
    }
    input,
    i {
        display: table-cell;
    }
}
code {
    font-family: Monospace;
    background: gray;
    display: block;
    color: white;
    padding: 1em;
    margin-top: 0.5em;
}



.actions {
  display: flex;
  justify-content: flex-end;
  padding-bottom: 1em;
  background: $questionBackground;
  padding-right: 1em;
}
.step {
  color: black;
  padding: 0.4rem 0.8rem;
  border: 1px solid $nextButtonBackground;
  margin-left: 1rem;
  cursor: pointer;
  font-family: 'Open Sans';
  font-size: 12pt;
}
.skip-step {
  border: 1px solid $skipButtonColor;
}
.next-step {
  background: $lightColor;
  color: white;
  border: 1px solid $nextButtonBackground;
}
.skip-step {
  border: 1px solid $skipButtonColor;
}

.memory-limited i.w-icon-close-square-o,
.storage-limited i.w-icon-close-square-o,
.multi-core i.w-icon-check-square-o,
.cpu-64bit i.w-icon-check-square-o,
.gpu-desktop i.w-icon-check-square-o  {
    color: darkgreen;
}

.memory-limited i.w-icon-check-square-o,
.storage-limited i.w-icon-check-square-o,
.cpu-64bit i.w-icon-close-square-o,
.gpu-desktop i.w-icon-close-square-o  {
    color: darkred;
}
</style>