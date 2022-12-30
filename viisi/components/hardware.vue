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
                        li {{ __i("windows-taskmgr-gpu-title") }}
                        li {{ __i("windows-taskmgr-gpu-directions") }}
                div.linux
                    h3 Linux
                    ol 
                        li {{ __i("linux-open-terminal") }}
                        li {{ __i("linux-execute") }} 
                            code bash -c 'echo CPU frequency in Ghz: $(($(cat /proc/cpuinfo | grep MHz | tail  -n 1 | grep -Eo "[0-9]+" | head  -n 1) / 1000)) && echo Memory in GB: $(($(grep MemTotal /proc/meminfo | grep -Eo "[0-9]+") / 1024 / 1024)) && echo Graphics card: $(lspci | grep VGA | cut -d ":" -f 3)'
            
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
            div.gpu.hardware-input
                label(for="gpu") {{  __i('hardware-gpu-title') }}
                input(name="gpu",  :placeholder="__i('hardware-gpu-placeholder')", v-model="gpu")
            h3 {{  __i("hardware-assumption-result") }}
            div.hardware-input(v-for="(result_value, result_key) in result", :key="result_key", :class="result_key")
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
            gpu: ""
        }
    },
    computed: {
        result: function () {
            return {
                "multi-core": this.cpuCores > 0,
                "cpu-64bit": navigator.userAgent.match(/(x64|Macintosh)/) != null,
                "mobile": this.gpu.match(/((R|G)TX \d{3,}M|M\d{2,})/) != null || this.gpu.match(/M1/),
                "touch": this.detectTouch(),
                "gpu-desktop": this.gpu.match(/((R|G)TX \d{3,}(!M)|M\d{2,})/) != null,
                "memory-limited": this.memory < 4
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
                this.getGraphicsCard()
            } else {
                this.cpuCores = 0
                this.memory = 0
                this.cpu = ""
                this.storage = 0
            }
        },
        /* see https://stackoverflow.com/questions/15464896/get-cpu-gpu-memory-information */
        getGraphicsCard: function() {
            const gl = document.createElement('canvas').getContext('webgl');
            if (!gl) {
                return {
                error: "no webgl",
                };
            }
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            this.gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
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
.multi-core i.w-icon-check-square-o,
.cpu-64bit i.w-icon-check-square-o,
.gpu-desktop i.w-icon-check-square-o  {
    color: darkgreen;
}

.memory-limited i.w-icon-check-square-o,
.cpu-64bit i.w-icon-close-square-o,
.gpu-desktop i.w-icon-close-square-o  {
    color: darkred;
}
</style>